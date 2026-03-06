import json
import os
import time
import subprocess

status_file = "/tmp/waybar_timer_status"
sequence = [50, 10, 40, 10, 30, 10, 20, 10, 10]

if not os.path.exists(status_file):
    status = {"phase_idx": 0, "remaining": sequence[0] * 60, "active": False, "target": None}
else:
    with open(status_file, "r") as f:
        status = json.load(f)

if status["active"]:
    status["remaining"] = int(status["target"] - time.time())
    status["active"] = False
    status["target"] = None
else:
    status["target"] = time.time() + status["remaining"]
    status["active"] = True

with open(status_file, "w") as f:
    json.dump(status, f)

subprocess.run(["pkill", "-RTMIN+1", "waybar"])