#!/usr/bin/env python3
"""
MVP 0.1 - Barebones System Monitor (Text Only)
Displays CPU, RAM, and Battery usage, updating every second.
"""

import psutil
import time
import os


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def get_battery_info():
    """Get battery percentage and status."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
        return None, None
    except Exception:
        return None, None


def display_stats():
    """Display system statistics."""
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    
    # RAM Usage
    memory = psutil.virtual_memory()
    ram_percent = memory.percent
    ram_used = memory.used / (1024 ** 3)  # Convert to GB
    ram_total = memory.total / (1024 ** 3)
    
    # Battery Info
    battery_percent, is_plugged = get_battery_info()
    
    # Display
    print("=" * 50)
    print("         SYSTEM MONITOR - MVP 0.1")
    print("=" * 50)
    print()
    print(f"CPU Usage:  {cpu_percent:5.1f}%")
    print(f"RAM Usage:  {ram_percent:5.1f}% ({ram_used:.2f}GB / {ram_total:.2f}GB)")
    
    if battery_percent is not None:
        status = "Charging" if is_plugged else "Discharging"
        print(f"Battery:    {battery_percent:5.1f}% ({status})")
    else:
        print(f"Battery:    N/A (No battery detected)")
    
    print()
    print("=" * 50)
    print("Press Ctrl+C to exit")


def main():
    """Main loop to update stats every second."""
    print("Starting System Monitor...")
    time.sleep(1)
    
    try:
        while True:
            clear_screen()
            display_stats()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nMonitor stopped.")


if __name__ == "__main__":
    main()
