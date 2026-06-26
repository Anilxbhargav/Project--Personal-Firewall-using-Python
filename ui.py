import customtkinter as ctk
import queue
import tkinter as tk
from tkinter import messagebox
from firewall import FirewallEngine
from utils import is_valid_ip

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FirewallApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShieldX - Enterprise Python Firewall")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.ui_queue = queue.Queue()
        self.engine = FirewallEngine(self.ui_queue)

        self.setup_ui()
        self.check_queue()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="ShieldX Firewall", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Stopped", text_color="red", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=10)

        self.btn_start = ctk.CTkButton(self.sidebar, text="Start Engine", fg_color="green", hover_color="darkgreen", command=self.start_engine)
        self.btn_start.pack(pady=10, padx=20)

        self.btn_stop = ctk.CTkButton(self.sidebar, text="Stop Engine", fg_color="red", hover_color="darkred", command=self.stop_engine)
        self.btn_stop.pack(pady=10, padx=20)

        # Stats
        self.lbl_stats = ctk.CTkLabel(self.sidebar, text="Total: 0\nBlocked: 0\nAllowed: 0", justify="left")
        self.lbl_stats.pack(side="bottom", pady=20)

        # Main Content Area
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tab_dash = self.tabview.add("Dashboard")
        self.tab_traffic = self.tabview.add("Live Traffic")
        self.tab_rules = self.tabview.add("Rules & Config")

        self._build_dashboard()
        self._build_traffic_view()
        self._build_rules_view()

    def _build_dashboard(self):
        # System Logs
        lbl = ctk.CTkLabel(self.tab_dash, text="Security Events Log", font=ctk.CTkFont(weight="bold"))
        lbl.pack(pady=(10, 0), anchor="w")
        
        self.log_box = ctk.CTkTextbox(self.tab_dash, state="disabled")
        self.log_box.pack(fill="both", expand=True, pady=10)

        # Quick Block
        frame_block = ctk.CTkFrame(self.tab_dash)
        frame_block.pack(fill="x", pady=10)
        
        self.entry_ip = ctk.CTkEntry(frame_block, placeholder_text="Enter IP to block...")
        self.entry_ip.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        btn_block = ctk.CTkButton(frame_block, text="Block IP", command=self.manual_block)
        btn_block.pack(side="left", padx=5, pady=10)
        
        btn_unblock = ctk.CTkButton(frame_block, text="Unblock IP", fg_color="transparent", border_width=1, command=self.manual_unblock)
        btn_unblock.pack(side="right", padx=(5, 10), pady=10)

    def _build_traffic_view(self):
        self.traffic_box = ctk.CTkTextbox(self.tab_traffic, state="disabled", font=("Consolas", 11))
        self.traffic_box.pack(fill="both", expand=True, pady=10)

    def _build_rules_view(self):
        lbl = ctk.CTkLabel(self.tab_rules, text="Currently Blocked IPs (Blacklist)", font=ctk.CTkFont(weight="bold"))
        lbl.pack(pady=10, anchor="w")
        
        self.blacklist_box = ctk.CTkTextbox(self.tab_rules, state="disabled")
        self.blacklist_box.pack(fill="both", expand=True, pady=10)
        self.update_blacklist_view()

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()

    def manual_block(self):
        ip = self.entry_ip.get().strip()
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "Please enter a valid IPv4 or IPv6 address.")
            return
        if self.engine.block_ip(ip, "Manual Rule"):
            self.entry_ip.delete(0, tk.END)
            self.update_blacklist_view()
        else:
            messagebox.showinfo("Info", "IP is already blocked or whitelisted.")

    def manual_unblock(self):
        ip = self.entry_ip.get().strip()
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "Please enter a valid IPv4 or IPv6 address.")
            return
        if self.engine.unblock_ip(ip):
            self.entry_ip.delete(0, tk.END)
            self.update_blacklist_view()
        else:
            messagebox.showinfo("Info", "IP is not currently blocked.")

    def update_blacklist_view(self):
        self.blacklist_box.configure(state="normal")
        self.blacklist_box.delete("1.0", tk.END)
        for ip in self.engine.blacklist:
            self.blacklist_box.insert(tk.END, f"{ip}\n")
        self.blacklist_box.configure(state="disabled")

    def check_queue(self):
        """Processes messages from the background firewall thread."""
        while not self.ui_queue.empty():
            msg = self.ui_queue.get()
            m_type = msg["type"]
            data = msg["data"]

            if m_type == "status":
                self.status_label.configure(text=f"Status: {data}", text_color="green" if data == "Running" else "red")
            
            elif m_type == "log":
                self.log_box.configure(state="normal")
                self.log_box.insert(tk.END, f"{data}\n")
                self.log_box.see(tk.END)
                self.log_box.configure(state="disabled")
                self.update_blacklist_view()
                
            elif m_type == "monitor":
                self.traffic_box.configure(state="normal")
                self.traffic_box.insert(tk.END, f"{data}\n")
                # Prevent memory leak by keeping only last 500 lines
                if int(self.traffic_box.index('end-1c').split('.')[0]) > 500:
                    self.traffic_box.delete("1.0", "2.0")
                self.traffic_box.see(tk.END)
                self.traffic_box.configure(state="disabled")

        # Update stats counter safely
        s = self.engine.stats
        self.lbl_stats.configure(text=f"Total: {s['total_packets']}\nBlocked: {s['blocked_packets']}\nAllowed: {s['allowed_packets']}")
        
        # Loop every 100ms
        self.after(100, self.check_queue)

    def on_closing(self):
        if self.engine.running:
            self.engine.stop()
        self.destroy()
