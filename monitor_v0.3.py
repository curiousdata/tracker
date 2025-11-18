#!/usr/bin/env python3
"""
MVP 0.3 - Advanced System Monitor with Extended Metrics
Features per-core CPU, disk, network, temperatures, and ASCII gauge styling.
"""

import psutil
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich import box
from datetime import datetime
import subprocess
import re
import platform


console = Console()


def create_ascii_gauge(value, width=20, label=""):
    """Create an ASCII gauge/dial for a metric."""
    filled = int((value / 100) * width)
    empty = width - filled
    
    # Color based on value
    if value > 80:
        color = "red"
    elif value > 60:
        color = "yellow"
    else:
        color = "green"
    
    bar = f"[{color}]{'▓' * filled}{'░' * empty}[/{color}]"
    return f"{bar} {value:5.1f}%"


def get_battery_info():
    """Get battery percentage and temperature if available."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
        return None, None
    except Exception:
        return None, None


def get_temperatures():
    """Get CPU and battery temperatures if available."""
    temps = {}
    try:
        temp_sensors = psutil.sensors_temperatures()
        
        # Try to find CPU temperature
        for name, entries in temp_sensors.items():
            if 'coretemp' in name.lower() or 'cpu' in name.lower():
                if entries:
                    temps['cpu'] = entries[0].current
                    break
        
        # Try to find battery temperature
        for name, entries in temp_sensors.items():
            if 'battery' in name.lower() or 'bat' in name.lower():
                if entries:
                    temps['battery'] = entries[0].current
                    break
    except Exception:
        pass
    
    return temps


def get_mac_temperatures():
    """Get CPU temperature on Mac using osx-cpu-temp."""
    temps = {}
    try:
        result = subprocess.run(
            ['osx-cpu-temp'],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        # Output is like: "61.8°C"
        match = re.search(r'(\d+\.\d+)', result.stdout)
        if match:
            temps['cpu'] = float(match.group(1))
        
    except Exception:
        pass
    
    return temps


def get_system_temperatures():
    """Get system temperatures based on the operating system."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return get_mac_temperatures()
    elif system == "Linux":
        return get_temperatures()
    elif system == "Windows":
        return get_temperatures()
    else:
        return {}


def get_network_stats():
    """Get network throughput stats."""
    try:
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent, net_io.bytes_recv
    except Exception:
        return 0, 0


def format_bytes(bytes_val):
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def create_control_panel():
    """Create the control panel layout with ASCII gauges."""
    # Get system stats
    cpu_percent = psutil.cpu_percent(interval=0.1)
    per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
    
    memory = psutil.virtual_memory()
    ram_percent = memory.percent
    ram_used = memory.used / (1024 ** 3)
    ram_total = memory.total / (1024 ** 3)
    
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used = disk.used / (1024 ** 3)
    disk_total = disk.total / (1024 ** 3)
    
    bytes_sent, bytes_recv = get_network_stats()
    
    battery_percent, is_plugged = get_battery_info()
    temps = get_system_temperatures()  # Use the OS-aware function
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Header with ASCII art
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_text = f"""[bold cyan]╔═══════════════════════════════════════════════════════════╗
║     SYSTEM CONTROL PANEL - MVP 0.3                    ║
║     {current_time}                        ║
╚═══════════════════════════════════════════════════════════╝[/bold cyan]"""
    
    layout["header"].update(Panel(header_text, style="bold white", box=box.SIMPLE))
    
    # LEFT PANEL - CPU and Memory
    left_table = Table(show_header=False, box=box.DOUBLE, expand=True, title="[bold cyan]⚙ PROCESSORS & MEMORY[/bold cyan]")
    left_table.add_column("Metric", style="cyan", width=20)
    left_table.add_column("Gauge", ratio=1)
    
    # Overall CPU
    left_table.add_row("[bold]CPU Overall[/bold]", create_ascii_gauge(cpu_percent))
    left_table.add_row("", "")
    
    # Per-core CPU
    for i, core_percent in enumerate(per_cpu[:8]):  # Show up to 8 cores
        left_table.add_row(f"  Core {i+1}", create_ascii_gauge(core_percent, width=15))
    
    if len(per_cpu) > 8:
        left_table.add_row("", f"[dim]... and {len(per_cpu) - 8} more cores[/dim]")
    
    left_table.add_row("", "")
    
    # Memory
    left_table.add_row("[bold]RAM Usage[/bold]", create_ascii_gauge(ram_percent))
    left_table.add_row("  Details", f"[white]{ram_used:.2f}GB / {ram_total:.2f}GB[/white]")
    
    # Disk
    left_table.add_row("", "")
    left_table.add_row("[bold]Disk Usage[/bold]", create_ascii_gauge(disk_percent))
    left_table.add_row("  Details", f"[white]{disk_used:.1f}GB / {disk_total:.1f}GB[/white]")
    
    # RIGHT PANEL - Network, Battery, Temperatures
    right_table = Table(show_header=False, box=box.DOUBLE, expand=True, title="[bold cyan]📡 NETWORK & POWER[/bold cyan]")
    right_table.add_column("Metric", style="cyan", width=20)
    right_table.add_column("Value", ratio=1)
    
    # Network
    right_table.add_row("[bold]Network I/O[/bold]", "")
    right_table.add_row("  Bytes Sent", f"[green]{format_bytes(bytes_sent)}[/green]")
    right_table.add_row("  Bytes Recv", f"[blue]{format_bytes(bytes_recv)}[/blue]")
    right_table.add_row("", "")
    
    # Battery
    if battery_percent is not None:
        status = "⚡ CHARGING" if is_plugged else "🔋 ON BATTERY"
        right_table.add_row("[bold]Battery[/bold]", "")
        right_table.add_row("  Level", create_ascii_gauge(battery_percent, width=15))
        right_table.add_row("  Status", f"[yellow]{status}[/yellow]")
    else:
        right_table.add_row("[bold]Battery[/bold]", "")
        right_table.add_row("  Status", "[dim]No battery detected[/dim]")
    
    right_table.add_row("", "")
    
    # Temperatures
    right_table.add_row("[bold]Temperatures[/bold]", "")
    if 'cpu' in temps:
        temp_color = "red" if temps['cpu'] > 80 else "yellow" if temps['cpu'] > 60 else "green"
        right_table.add_row("  CPU Temp", f"[{temp_color}]{temps['cpu']:.1f}°C[/{temp_color}]")
    else:
        right_table.add_row("  CPU Temp", "[dim]N/A[/dim]")
    
    if 'battery' in temps:
        temp_color = "red" if temps['battery'] > 45 else "yellow" if temps['battery'] > 35 else "green"
        right_table.add_row("  Battery Temp", f"[{temp_color}]{temps['battery']:.1f}°C[/{temp_color}]")
    else:
        right_table.add_row("  Battery Temp", "[dim]N/A[/dim]")
    
    # Body - split into sections
    layout["body"].split_row(
        Layout(Panel(left_table, border_style="cyan")),
        Layout(Panel(right_table, border_style="cyan"))
    )
    
    # Footer
    layout["footer"].update(
        Panel(
            "[bold cyan]◄◄[/bold cyan] [dim]System Monitor Active[/dim] [bold cyan]►►[/bold cyan] | Press [bold]Ctrl+C[/bold] to exit",
            style="dim white on black"
        )
    )
    
    return layout


def main():
    """Main loop to update control panel."""
    console.print("[bold green]⚡ Initializing System Control Panel...[/bold green]")
    time.sleep(1)
    
    try:
        with Live(create_control_panel(), console=console, refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(create_control_panel())
    except KeyboardInterrupt:
        console.print("\n[bold yellow]═══ Control Panel Shutdown ═══[/bold yellow]")


if __name__ == "__main__":
    main()
