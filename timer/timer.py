import json
import os
import time
import subprocess

status_file = "/tmp/waybar_timer_status"
sequence = [50, 10, 40, 10, 30, 10, 20, 10, 10]

def send_notification(actual_phase):
    next_phase_idx = actual_phase + 1
    if next_phase_idx < len(sequence):
        next_type = "Break" if next_phase_idx % 2 != 0 else "Work"
        msg = f"Phase ended. Next: {next_type} ({sequence[next_phase_idx]} min)"
    else:
        msg = "All phases completed!"
        
    subprocess.Popen(["notify-send", "-u", "critical", "Timer", msg])
    subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"])

def load_status():
    if not os.path.exists(status_file):
        return {"phase_idx": 0, "remaining": sequence[0] * 60, "active": False, "target": None}
    with open(status_file, "r") as f:
        return json.load(f)

status = load_status()
now = time.time()
phase = "break" if status["phase_idx"] % 2 != 0 else "work"

if status["active"]:
    real_seconds = int(status["target"] - now)
    
    if real_seconds <= 0:
        
        old_phase = status["phase_idx"]
        status["phase_idx"] += 1

        send_notification(old_phase)
        
        if status["phase_idx"] < len(sequence):
            new_time = sequence[status["phase_idx"]] * 60
            status["remaining"] = new_time
            status["target"] = now + new_time
            real_seconds = new_time
        else:
            status["active"] = False
            status["phase_idx"] = 0
            status["remaining"] = sequence[0] * 60
            real_seconds = status["remaining"]
        
        with open(status_file, "w") as f:
            json.dump(status, f)

    else:
        status["remaining"] = real_seconds
else:
    real_seconds = status["remaining"]

mins, secs = divmod(real_seconds, 60)
time_text = f"{mins:02d}:{secs:02d}"

is_break = status["phase_idx"] % 2 != 0
icon = "󱫪" if is_break else "󱫠"
if not status["active"]: icon = "󱫞"

output = {
    "text": f"{icon} {time_text}",
    "class": "break" if is_break else "work",
    "tooltip": f"Phase: {sequence[status["phase_idx"]]} minutes {phase} \nClick to start/pause | Right-click to reset"
}

print(json.dumps(output))

with open(status_file, "w") as f:
    json.dump(status, f)