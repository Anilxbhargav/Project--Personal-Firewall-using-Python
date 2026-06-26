# 🛡️ Python Personal Firewall

A lightweight, GUI-driven **Personal Firewall** built with **Python** and **Tkinter**. This tool is designed to monitor, log, and block suspicious IP packets in real-time. By leveraging `scapy` for network analysis and `iptables` for traffic filtering, it automatically detects potential Denial of Service (DoS) attacks while offering manual overriding capabilities.

---

## ✨ Key Features

* **Real-Time Packet Sniffing:** Continuously analyzes incoming network traffic using Scapy.
* **Intelligent Auto-Detection:** Automatically identifies and mitigates potential DoS attacks based on traffic volume thresholds.
* **Manual Intervention:** User-friendly GUI allows for immediate manual blocking of specific, suspicious IP addresses.
* **Comprehensive Logging:** Maintains a detailed, timestamped record of all intercepted packets and blocked IPs.
* **Live Status Updates:** Real-time feedback and alerts displayed directly on the Tkinter interface.

---

## 🏗️ System Requirements

This project relies on Linux-specific network management tools.

* **Operating System:** Linux (Debian/Ubuntu, Arch, Fedora, etc.)
* **Core Dependency:** `iptables` (Must be installed and accessible)
* **Python Version:** Python 3.6+

### Dependencies

Install the required Python libraries using `pip`:

```bash
pip install scapy
```

---

## ⚙️ How It Works (Under the Hood)

1. **Continuous Monitoring:** The application listens to incoming network packets on the active network interface.
2. **Threshold Evaluation:** If a single IP address transmits **more than 50 packets within a 10-second window**, the firewall flags the behavior as a potential DoS attack.
3. **Automated Blocking:** Upon flagging, the script executes an `iptables` rule to drop further traffic from the malicious IP.
4. **Log Generation:** Both routine traffic and security events (blocks) are appended to `firewall_logs.txt` for post-incident analysis.

---

## 🖥️ Graphical User Interface (GUI)

The interface is built for simplicity and rapid response.

| UI Element          | Functionality                                                             |
| ------------------- | ------------------------------------------------------------------------- |
| **Start Firewall**  | Initializes the Scapy sniffer and begins monitoring traffic.              |
| **Stop Firewall**   | Halts packet sniffing and suspends firewall operations.                   |
| **IP Entry Box**    | Input field for specifying a custom IP address.                           |
| **Block IP Button** | Instantly executes an `iptables` drop rule for the entered IP.            |
| **Status Label**    | Displays real-time operational status, active alerts, and recent actions. |

---

## 📂 Execution & Usage

> **⚠️ CRITICAL:** This application requires **root/administrator privileges** to intercept network packets and modify `iptables` rules.

To launch the firewall, open your terminal and run:

```bash
sudo python3 personal_firewall.py
```

### Log File Output

Logs are automatically generated in the root directory as `firewall_logs.txt`.

*Example Output:*

```text
Sat Jun 22 20:35:45 2026: Packet: 192.168.1.5 --> 192.168.1.10
Sat Jun 22 20:35:50 2026: Blocked IP: 192.168.1.5
```

---

## 🚀 Future Roadmap

* [ ] **Windows Integration:** Implement `netsh` support to extend compatibility to Windows environments.
* [ ] **Dynamic Thresholding:** Allow users to customize the packet limit and time window directly from the GUI.
* [ ] **Integrated Log Viewer:** Build a tab within the Tkinter app to review logs without opening external text files.
* [ ] **Desktop Notifications:** Add system-level popup alerts when an IP is automatically blocked.

---

## 🤝 Contributing

Contributions, issues, and feature requests are highly welcome! Feel free to check the issues page or fork the repository and submit a Pull Request.

---
