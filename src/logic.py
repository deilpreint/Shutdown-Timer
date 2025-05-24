import subprocess

def convert_to_seconds(hours, minutes):
    return hours * 3600 + minutes * 60

def schedule_shutdown(hours, minutes):
    total_seconds = convert_to_seconds(hours, minutes)
    if total_seconds <= 0:
        raise ValueError("Время должно быть положительным")
    subprocess.run(["shutdown", "-s", "-t", str(total_seconds)])

def cancel_shutdown():
    subprocess.run(["shutdown", "-a"])
