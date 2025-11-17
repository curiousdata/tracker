#!/usr/bin/env python3
"""
MVP 0.2 - System Monitor with TUI Dashboard
Uses Rich library for colored bars and nice layout.
"""

import psutil
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table
from rich.live import Live
from rich import box


console = Console()


def get_battery_info():
    """Get battery percentage and status."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
        return None, None
    except Exception:
        return None, None


def create_progress_bar(value, color="green"):
    """Create a progress bar for a metric."""
    progress = Progress(
        BarColumn(bar_width=30),
        expand=False
    )
    task = progress.add_task("", total=100, completed=value)
    
    # Color based on value
    if value > 80:
        color = "red"
    elif value > 60:
        color = "yellow"
    else:
        color = "green"
    
    return progress


def create_dashboard():
    """Create the dashboard layout."""
    # Get system stats
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    ram_percent = memory.percent
    ram_used = memory.used / (1024 ** 3)
    ram_total = memory.total / (1024 ** 3)
    battery_percent, is_plugged = get_battery_info()
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Header
    layout["header"].update(
        Panel(
            "[bold cyan]SYSTEM MONITOR - MVP 0.2[/bold cyan]",
            style="bold white on blue",
            box=box.DOUBLE
        )
    )
    
    # Body with metrics
    table = Table(show_header=False, box=box.ROUNDED, expand=True)
    table.add_column("Metric", style="cyan bold", width=15)
    table.add_column("Value", style="white", width=10)
    table.add_column("Bar", ratio=1)
    
    # CPU
    cpu_color = "red" if cpu_percent > 80 else "yellow" if cpu_percent > 60 else "green"
    cpu_bar = f"[{cpu_color}]{'█' * int(cpu_percent / 2)}{'░' * (50 - int(cpu_percent / 2))}[/{cpu_color}]"
    table.add_row("CPU Usage", f"{cpu_percent:.1f}%", cpu_bar)
    
    # RAM
    ram_color = "red" if ram_percent > 80 else "yellow" if ram_percent > 60 else "green"
    ram_bar = f"[{ram_color}]{'█' * int(ram_percent / 2)}{'░' * (50 - int(ram_percent / 2))}[/{ram_color}]"
    table.add_row("RAM Usage", f"{ram_percent:.1f}%", ram_bar)
    table.add_row("", f"{ram_used:.2f}GB / {ram_total:.2f}GB", "")
    
    # Battery
    if battery_percent is not None:
        status = "⚡ Charging" if is_plugged else "🔋 Discharging"
        bat_color = "red" if battery_percent < 20 else "yellow" if battery_percent < 50 else "green"
        bat_bar = f"[{bat_color}]{'█' * int(battery_percent / 2)}{'░' * (50 - int(battery_percent / 2))}[/{bat_color}]"
        table.add_row("Battery", f"{battery_percent:.1f}%", bat_bar)
        table.add_row("", status, "")
    else:
        table.add_row("Battery", "N/A", "[dim]No battery detected[/dim]")
    
    layout["body"].update(Panel(table, title="[bold]System Metrics[/bold]", border_style="cyan"))
    
    # Footer
    layout["footer"].update(
        Panel(
            "[dim]Press Ctrl+C to exit[/dim]",
            style="dim white on black"
        )
    )
    
    return layout


def main():
    """Main loop to update dashboard."""
    console.print("[bold green]Starting System Monitor with TUI...[/bold green]")
    time.sleep(1)
    
    try:
        with Live(create_dashboard(), console=console, refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(create_dashboard())
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitor stopped.[/bold yellow]")


if __name__ == "__main__":
    main()
