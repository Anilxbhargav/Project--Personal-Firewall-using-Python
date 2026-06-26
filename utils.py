import ipaddress
import logging
from logging.handlers import RotatingFileHandler
import json
import os

def setup_logger(log_file="firewall_events.log", max_bytes=5242880, backup_count=3):
    """Sets up a structured rotating logger."""
    logger = logging.getLogger("FirewallLogger")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

def is_valid_ip(ip_str):
    """Validates if a string is a proper IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def load_config(config_path="config.json"):
    """Loads JSON configuration."""
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def save_config(config_data, config_path="config.json"):
    """Saves data to JSON configuration."""
    try:
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
