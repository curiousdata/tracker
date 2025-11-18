# System Monitor (tracker)

A Python-based system monitoring tool with three progressive versions, from a simple text-based monitor to an advanced TUI dashboard with ASCII gauges styled like an old control panel.

## Features

### MVP 0.1 - Barebones Text Monitor
Basic text-only system monitor that displays:
- CPU usage
- RAM usage (percentage and GB)
- Battery status and percentage
- Updates every second in the terminal

### MVP 0.2 - TUI Dashboard
Enhanced version with Rich library featuring:
- Professional layout with colored panels
- Progress bars with color-coding (green/yellow/red based on usage)
- Nice visual presentation
- Real-time updates

### MVP 0.3 - Advanced Control Panel
Full-featured system monitor with:
- **Per-core CPU load** monitoring (up to 8 cores displayed)
- **Disk usage** tracking
- **Network I/O** statistics (bytes sent/received)
- **CPU temperature** monitoring (if available)
- **Battery temperature** monitoring (if available)
- **ASCII gauges and dials** styled like an old control panel
- Two-column layout for organized metric display

## Installation

1. Clone the repository:
```bash
git clone https://github.com/curiousdata/tracker.git
cd tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Interactive Menu)
```bash
python3 monitor.py
```

This will display a menu where you can select which version to run.

### Run MVP 0.1 (Basic Text Monitor)
```bash
python3 monitor_v0.1.py
```

### Run MVP 0.2 (TUI Dashboard)
```bash
python3 monitor_v0.2.py
```

### Run MVP 0.3 (Advanced Control Panel)
```bash
python3 monitor_v0.3.py
```

Press `Ctrl+C` to exit any version.

## Requirements

- Python 3.7+
- psutil >= 5.9.0
- rich >= 13.0.0 (for MVP 0.2 and 0.3)

## System Compatibility

- **Linux**: Full support for all metrics including temperatures
- **macOS**: Full support with some temperature sensors
- **Windows**: Full support except for some temperature sensors

Note: Temperature monitoring availability depends on your system's hardware sensors. If sensors are not available, those metrics will show as "N/A".

## License

MIT License - see LICENSE file for details

## Screenshots

### MVP 0.1
Simple text-based output updating every second:
```
==================================================
         SYSTEM MONITOR - MVP 0.1
==================================================

CPU Usage:    5.2%
RAM Usage:   12.4% (1.93GB / 15.62GB)
Battery:    85.0% (Discharging)

==================================================
Press Ctrl+C to exit
```

### MVP 0.2
Professional TUI dashboard with colored bars and panels.

### MVP 0.3
Advanced control panel with per-core monitoring, network stats, and ASCII gauges styled like vintage control panels.