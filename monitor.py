#!/usr/bin/env python3
"""
System Monitor - Main Entry Point
Allows users to select which MVP version to run.
"""

import sys
import subprocess


def print_menu():
    """Display the menu for version selection."""
    print("\n" + "=" * 60)
    print("         SYSTEM MONITOR - Version Selector")
    print("=" * 60)
    print()
    print("Select a version to run:")
    print()
    print("  1. MVP 0.1 - Barebones text-only monitor")
    print("     Simple display of CPU, RAM, and Battery")
    print()
    print("  2. MVP 0.2 - TUI Dashboard")
    print("     Enhanced UI with colored bars and panels")
    print()
    print("  3. MVP 0.3 - Advanced Control Panel")
    print("     Full metrics with per-core CPU, disk, network, temps")
    print()
    print("  q. Quit")
    print()
    print("=" * 60)


def run_monitor(version):
    """Run the selected monitor version."""
    scripts = {
        '1': 'monitor_v0.1.py',
        '2': 'monitor_v0.2.py',
        '3': 'monitor_v0.3.py'
    }
    
    if version in scripts:
        try:
            subprocess.run([sys.executable, scripts[version]])
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
        return True
    return False


def main():
    """Main menu loop."""
    while True:
        print_menu()
        choice = input("Enter your choice (1-3 or q): ").strip().lower()
        
        if choice == 'q':
            print("\nGoodbye!")
            break
        elif choice in ['1', '2', '3']:
            run_monitor(choice)
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
