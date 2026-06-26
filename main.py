import sys
from ui import FirewallApp

if __name__ == "__main__":
    try:
        app = FirewallApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        print(f"Fatal error initializing application: {e}")
        sys.exit(1)
