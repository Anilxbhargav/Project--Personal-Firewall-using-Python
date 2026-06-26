import threading
import time
import subprocess
import platform
from collections import defaultdict
from scapy.all import sniff, IP, TCP, UDP
from utils import setup_logger, is_valid_ip, load_config, save_config

class FirewallEngine:
    def __init__(self, ui_queue=None):
        self.os_type = platform.system()
        self.running = False
        self.ui_queue = ui_queue
        
        # Load Config
        self.config = load_config() or {"settings": {}, "whitelist": [], "blacklist": []}
        settings = self.config.get("settings", {})
        self.time_window = settings.get("time_window_seconds", 10)
        self.dos_threshold = settings.get("dos_threshold", 100)
        self.scan_threshold = settings.get("port_scan_threshold", 15)
        
        self.whitelist = set(self.config.get("whitelist", []))
        self.blacklist = set(self.config.get("blacklist", []))
        self.blocked_ips = set(self.blacklist)
        
        self.logger = setup_logger(settings.get("log_file", "firewall.log"))
        
        # Threat Detection States
        self.ip_packet_count = defaultdict(list)
        self.ip_ports_accessed = defaultdict(set)
        
        # Stats
        self.stats = {
            "total_packets": 0,
            "blocked_packets": 0,
            "allowed_packets": 0
        }

    def _send_to_ui(self, msg_type, data):
        """Thread-safe UI updates."""
        if self.ui_queue:
            self.ui_queue.put({"type": msg_type, "data": data})

    def execute_os_command(self, command):
        """Executes OS level commands safely."""
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command execution failed: {e}")
            return False

    def block_ip(self, ip, reason="Manual"):
        """Blocks an IP using OS-native firewalls."""
        if not is_valid_ip(ip) or ip in self.whitelist or ip in self.blocked_ips:
            return False

        success = False
        if self.os_type == "Windows":
            cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 
                   f"name=Block_{ip}", "dir=in", "action=block", f"remoteip={ip}"]
            success = self.execute_os_command(cmd)
        elif self.os_type == "Linux":
            cmd = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
            success = self.execute_os_command(cmd)

        if success:
            self.blocked_ips.add(ip)
            self.blacklist.add(ip)
            self._save_blacklist()
            self.logger.warning(f"BLOCKED: {ip} | Reason: {reason}")
            self._send_to_ui("log", f"[BLOCKED] {ip} ({reason})")
            return True
        return False

    def unblock_ip(self, ip):
        """Unblocks a previously blocked IP."""
        if ip not in self.blocked_ips:
            return False

        success = False
        if self.os_type == "Windows":
            cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", f"name=Block_{ip}"]
            success = self.execute_os_command(cmd)
        elif self.os_type == "Linux":
            cmd = ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
            success = self.execute_os_command(cmd)

        if success or self.os_type == "Windows": # Windows sometimes succeeds even if rule missing
            self.blocked_ips.discard(ip)
            self.blacklist.discard(ip)
            self._save_blacklist()
            self.logger.info(f"UNBLOCKED: {ip}")
            self._send_to_ui("log", f"[UNBLOCKED] {ip}")
            return True
        return False

    def _save_blacklist(self):
        self.config["blacklist"] = list(self.blacklist)
        save_config(self.config)

    def _analyze_threats(self, ip_src, dst_port, current_time):
        """Heuristic detection for DoS and Port Scanning."""
        # Clean up old timestamps
        self.ip_packet_count[ip_src] = [t for t in self.ip_packet_count[ip_src] if current_time - t < self.time_window]
        self.ip_packet_count[ip_src].append(current_time)
        
        if dst_port:
            self.ip_ports_accessed[ip_src].add(dst_port)

        # DoS Check
        if len(self.ip_packet_count[ip_src]) > self.dos_threshold:
            self.block_ip(ip_src, reason="DoS/Flood Detected")
            return True

        # Port Scan Check
        if len(self.ip_ports_accessed[ip_src]) > self.scan_threshold:
            self.block_ip(ip_src, reason="Port Scan Detected")
            self.ip_ports_accessed[ip_src].clear() # Reset after block
            return True
            
        return False

    def packet_callback(self, packet):
        """Scapy packet parsing and routing."""
        if not self.running:
            return

        if packet.haslayer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            protocol = packet[IP].proto
            size = len(packet)
            
            dst_port = None
            if packet.haslayer(TCP):
                dst_port = packet[TCP].dport
            elif packet.haslayer(UDP):
                dst_port = packet[UDP].dport

            self.stats["total_packets"] += 1

            if ip_src in self.blocked_ips:
                self.stats["blocked_packets"] += 1
                return # Drop further processing for blocked IPs

            self.stats["allowed_packets"] += 1
            
            # Send live monitor data
            pkt_data = f"{ip_src} -> {ip_dst} | Proto: {protocol} | Port: {dst_port} | Size: {size}B"
            self._send_to_ui("monitor", pkt_data)

            # Analyze for threats
            if ip_src not in self.whitelist:
                self._analyze_threats(ip_src, dst_port, time.time())

    def start(self):
        """Starts the packet sniffing thread."""
        if self.running: return
        self.running = True
        self.logger.info("Firewall Engine Started.")
        self._send_to_ui("status", "Running")
        
        self.sniff_thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.sniff_thread.start()

    def _sniff_loop(self):
        try:
            sniff(prn=self.packet_callback, store=0, stop_filter=lambda x: not self.running)
        except Exception as e:
            self.logger.error(f"Sniffer error: {e}")
            self._send_to_ui("log", f"[ERROR] Sniffer crashed: {e}. Check Admin/Root privileges.")
            self.running = False
            self._send_to_ui("status", "Stopped (Error)")

    def stop(self):
        """Stops the packet sniffing thread."""
        self.running = False
        self.logger.info("Firewall Engine Stopped.")
        self._send_to_ui("status", "Stopped")
