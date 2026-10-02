# macos-battery-tracker

A lightweight, zero-dependency CLI tool for macOS that tracks real **Screen-On Time (SOT)**, total drain, and discharge rates since disconnecting from your charger.

---

### Output

```text
============================================
Unplugged at:        2026-10-02 12:52:45 AM
Battery:             80% -> 31% (-49%)
Time off charger:    18h 17m
Active Screen Time:  4h 54m (294 active minutes)
Burn rate (Screen):  ~6.0 min per 1% (10.0% / hr)
============================================
```

---

### Why Use This?

macOS System Settings only tracks battery usage across fixed 24-hour or 10-day windows, mixing plugged-in usage with active battery drain.

This utility fixes that:
- **True Screen-On Time:** Counts only active display time and ignores clamshell sleep or idle standby in your bag.
- **Accurate Unplug Point:** Finds the exact second you detached the charger, ignoring background wake noise.
- **Burn Rate:** Calculates your active pace (minutes per 1% battery drop and % burned per hour).
- **Auto-Reset:** Automatically resets the counters every time you disconnect from power.
- **Zero Dependencies:** Runs on standard Python 3 already preinstalled on macOS.

---

### Installation & Usage

#### 1. Clone the repository
```bash
git clone https://github.com/mihaicraciun1902/macos-battery-tracker.git
cd macos-battery-tracker
chmod +x macos_battery_tracker.py
```

#### 2. Run it
```bash
python3 macos_battery_tracker.py
```

---

### Optional: Run It From Anywhere

To run it anytime as a simple command (like `mac-sot`):

```bash
sudo cp macos_battery_tracker.py /usr/local/bin/mac-sot
```

Now you can just type:
```bash
mac-sot
```

*Alternatively, add `alias sot="python3 /path/to/macos_battery_tracker.py"` to your `~/.zshrc`.*

---

### Requirements

- macOS (tested on Apple Silicon and Intel)
- Python 3 (standard on macOS)

---

### License

MIT