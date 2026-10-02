# macos-battery-tracker

Lightweight, zero-dependency macOS CLI utility that calculates true Screen-On Time (SOT), battery drain, and discharge rates since disconnecting from the charger using `pmset` power logs.

---

### Output Example

```text
=============================================
Unplugged at:        2026-10-02 12:52:45 AM
Battery:             80% -> 31% (-49%)
Time off charger:    18h 17m
Active Screen Time:  4h 54m (294 active minutes)
Burn rate (Screen):  ~6.0 min per 1% (10.0% / hr)
=============================================