import subprocess, time



def countdown(seconds):
    while seconds > 0:
        subprocess.run('clear', shell=True)
        mins, secs = divmod(seconds, 60)
        print(f"{mins}:{secs} remaining to break")
        time.sleep(1)
        seconds-=1

countdown(90)