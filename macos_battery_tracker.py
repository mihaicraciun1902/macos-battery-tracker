#!/usr/bin/env python3
import re
import subprocess
from datetime import datetime

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

# 1. Get current battery level and power status
batt_output = run_cmd("pmset -g batt")
curr_batt_match = re.search(r"(\d{1,3})%", batt_output)
current_batt = int(curr_batt_match.group(1)) if curr_batt_match else 0
on_batt = "Battery Power" in batt_output

# 2. If plugged into AC, stop here
if not on_batt:
    status_match = re.search(r";\s*([^;]+);", batt_output)
    charging_state = status_match.group(1).strip() if status_match else "connected"
    print("=" * 45)
    print(f"Power Source:    AC Power ({charging_state})")
    print(f"Current Battery: {current_batt}%")
    print("Unplug from charger to start a new battery session.")
    print("=" * 45)
    exit(0)

# 3. Read pmset logs to find the latest AC -> Battery transition
raw_log = run_cmd("pmset -g log")
unplug_time = None
start_charge = current_batt
last_state = None

time_regex = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
charge_regex = re.compile(r"Charge:\s*(\d+)")

for line in raw_log.splitlines():
    t_match = time_regex.match(line)
    if not t_match:
        continue
    
    timestamp = datetime.strptime(t_match.group(1), "%Y-%m-%d %H:%M:%S")

    if "Using AC" in line:
        last_state = "AC"
    elif "Using Batt" in line:
        if last_state == "AC":
            unplug_time = timestamp
            c_match = charge_regex.search(line)
            if c_match:
                start_charge = int(c_match.group(1))
        last_state = "Batt"

if not unplug_time:
    print("No recent unplug event found in logs.")
    exit(1)

# 4. Determine if the display was ALREADY on when unplugged
was_display_on_at_unplug = False
for line in raw_log.splitlines():
    t_match = time_regex.match(line)
    if not t_match:
        continue
    timestamp = datetime.strptime(t_match.group(1), "%Y-%m-%d %H:%M:%S")
    if timestamp <= unplug_time:
        if "Display is turned on" in line:
            was_display_on_at_unplug = True
        elif "Display is turned off" in line:
            was_display_on_at_unplug = False

# 5. Calculate active Screen-On Time since unplugging
screen_on_seconds = 0
display_on_since = unplug_time if was_display_on_at_unplug else None

for line in raw_log.splitlines():
    t_match = time_regex.match(line)
    if not t_match:
        continue
    
    timestamp = datetime.strptime(t_match.group(1), "%Y-%m-%d %H:%M:%S")
    if timestamp < unplug_time:
        continue

    if "Display is turned on" in line:
        # Avoid resetting timestamp on duplicate notifications
        if display_on_since is None:
            display_on_since = timestamp
    elif "Display is turned off" in line:
        if display_on_since:
            screen_on_seconds += (timestamp - display_on_since).total_seconds()
            display_on_since = None

# If display is currently on, add elapsed time up to right now
now = datetime.now()
if display_on_since and display_on_since <= now:
    screen_on_seconds += (now - display_on_since).total_seconds()

# 6. Math & Formatting
drain = start_charge - current_batt
total_wall_sec = (now - unplug_time).total_seconds()

wall_h, wall_m = int(total_wall_sec // 3600), int((total_wall_sec % 3600) // 60)
sot_m_total = int(screen_on_seconds // 60)
sot_h, sot_m = divmod(sot_m_total, 60)

print("=" * 45)
print(f"Unplugged at:        {unplug_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
print(f"Battery:             {start_charge}% -> {current_batt}% (-{drain}%)")
print(f"Time off charger:    {wall_h}h {wall_m}m")
print(f"Active Screen Time:  {sot_h}h {sot_m}m ({sot_m_total} active minutes)")

if drain > 0 and sot_m_total > 0:
    min_per_pct = round(sot_m_total / drain, 1)
    pct_per_hr = round((drain / sot_m_total) * 60, 1)
    print(f"Burn rate (Screen):  ~{min_per_pct} min per 1% ({pct_per_hr}% / hr)")
print("=" * 45)