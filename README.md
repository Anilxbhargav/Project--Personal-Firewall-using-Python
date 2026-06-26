

```markdown
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/Security-IPS%20%2F%20IDS-red?style=for-the-badge&logo=security" alt="Security">
  <img src="https://img.shields.io/badge/UI-CustomTkinter-brightgreen?style=for-the-badge" alt="UI">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  
  <h1>🛡️ ShieldX - Advanced Python IPS & Firewall</h1>
  <p><b>Enterprise-Grade Intrusion Prevention System and Network Traffic Monitor</b></p>
</div>

---

## 📖 Project Overview

**ShieldX** is an advanced, cross-platform Personal Firewall and Intrusion Prevention System (IPS) built entirely in Python. Unlike standard firewalls that only rely on static rules, ShieldX actively sniffs network packets in real-time, analyzes traffic patterns using heuristic algorithms, and dynamically interfaces with the host operating system (`netsh` on Windows, `iptables` on Linux) to block malicious actors before they can compromise the system.

Built with a thread-safe architecture and a modern, asynchronous graphical interface using `CustomTkinter`, ShieldX is designed for performance, reliability, and ease of use.

---

## ✨ Key Features

* 🔬 **Deep Packet Inspection:** Utilizes `Scapy` to intercept and analyze raw TCP/UDP packets in real-time.
* 🧠 **Heuristic Threat Detection:** Automatically detects and mitigates:
  * **DoS (Denial of Service) & SYN Floods:** Analyzes packet flow rates to identify connection anomalies.
  * **Port Scanning:** Detects aggressive multi-port probing from single IPs.
* 🛡️ **Cross-Platform Kernel Blocking:**
  * **Windows:** Dynamically injects `netsh advfirewall` rules.
  * **Linux:** Dynamically writes `iptables` DROP policies.
* ⚡ **Asynchronous Thread-Safe GUI:** The UI never freezes. A robust Queue-based architecture separates the heavy packet-sniffing daemon from the presentation layer.
* ⚙️ **Dynamic Configuration:** Whitelists, blacklists, and threshold sensitivities are managed via a persistent `config.json` file.
* 📊 **Live Dashboard & Traffic Monitor:** View allowed/blocked packets, current rules, and security events in a beautiful Dark-Mode UI.
* 📝 **Professional Log Rotation:** Structured event logging with automatic log rotation to prevent disk space exhaustion.

---

## 📸 Application Screenshots

> *(Note: Add your actual screenshots here by uploading them to your GitHub repo and replacing the links)*

| Dashboard View | Live Traffic Monitor |
| :---: | :---: |
| <img src="https://via.placeholder.com/400x250.png?text=Dashboard+Screenshot" alt="Dashboard"> | <img src="https://via.placeholder.com/400x250.png?text=Live+Traffic+Screenshot" alt="Traffic"> |

---

## 🏗️ System Architecture

ShieldX follows a modular, object-oriented design pattern:

```text
ShieldX/
├── main.py               # Application entry point & crash handler
├── ui.py                 # CustomTkinter GUI & Queue Consumer
├── firewall.py           # Scapy Daemon, Threat Logic & OS Integration
├── utils.py              # I/O, Logging, and Validation utilities
├── config.json           # Dynamic settings and IP persistence
└── requirements.txt      # Python dependencies

```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.8+** installed on your system.
2. **Packet Capture Driver:**
* **Windows:** You must install [Npcap](https://npcap.com/) (Ensure "Install Npcap in WinPcap API-compatible Mode" is checked).
* **Linux:** Native support via `libpcap`.



### Installation Steps

1. **Clone the Repository:**
```bash
git clone [https://github.com/Anilxbhargav/Project--Personal-Firewall-using-Python.git](https://github.com/Anilxbhargav/Project--Personal-Firewall-using-Python.git)
cd Project--Personal-Firewall-using-Python

```


2. **Create a Virtual Environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate      # On Linux
venv\Scripts\activate         # On Windows

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Run the Application:**
> **⚠️ IMPORTANT:** ShieldX requires **Administrator/Root** privileges to intercept raw network packets and modify OS firewall rules.


* **Windows (Run CMD/PowerShell as Admin):**
```cmd
python main.py

```


* **Linux:**
```bash
sudo python3 main.py

```





---

## ⚙️ Configuration (`config.json`)

You can fine-tune ShieldX's behavior without editing the code. The system automatically creates a `config.json` file on the first run.

```json
{
    "settings": {
        "time_window_seconds": 10,
        "dos_threshold": 100,        // Packets per time_window to trigger DoS block
        "port_scan_threshold": 15,   // Unique ports accessed per time_window to trigger Scan block
        "log_file": "firewall_events.log"
    },
    "whitelist": [
        "127.0.0.1",
        "192.168.1.1",
        "8.8.8.8"
    ],
    "blacklist": []
}

```

---

## ⚠️ Disclaimer & Legal

**Educational & Authorized Use Only:** This tool is developed for cybersecurity research, academic demonstration, and authorized network defense. Do not use this tool on networks or systems you do not own or have explicit permission to monitor. The developer is not responsible for any misuse, network disruptions, or damage caused by this software.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you'd like to improve ShieldX, please fork the repository and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
