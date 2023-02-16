import os
from time import sleep
from win10toast import ToastNotifier
import socket
from datetime import datetime
print("hi. This little script will shut down your pc after a period of time (measured in seconds). Input the seconds below and your pc will get shut down after that period of time ends. Have fun ~ jtw")
print("Do you wanna set a specific time for the shut down or have a timer in seconds? (type 1 or 2)\n\n1. Choose a specific time (using the 24 hour format) - extremely early beta and could be somewhat inaccurate. I'd say it's accurate enough though\n2. Set a timer (in seconds)\n")
choice = input("Your choice (1 or 2): ")
def hours_calculation(hours, current_hours, current_minutes, minutes):
    all_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    current_hour_idx = all_hours.index(current_hours)
    counter = -1
    for i in all_hours[current_hour_idx::]:
        counter += 1
        if all_hours[i] == current_hours and current_minutes > minutes:
            continue
        if i == hours:
            return counter
        if i == 23:
            for a in all_hours[:current_hour_idx+1]:
                counter += 1
                if a == hours:
                    return counter
if choice == "1":
    try:
        specific_time = input("Specify the time (in the format of hh:mm:ss): ").split(":")
        hours, minutes, seconds = specific_time
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)
        seconds += minutes * 60
        current_time = str(datetime.now()).split(" ")[1].split(".")[0].split(":")
        current_hours, current_minutes, current_seconds = current_time
        current_hours, current_minutes, current_seconds = int(current_hours), int(current_minutes), int(current_seconds)
        current_seconds += current_minutes * 60
        difference = abs(current_seconds - seconds)
        seconds = difference + hours_calculation(hours, current_hours, current_minutes, minutes)*60*60
    except:
        raise Exception("Incorrect input.")
elif choice == "2":
    try:
        seconds = float(input("your number: "))
    except:
        raise ValueError("wrong input. It needs to be a number (float or int)")
else:
    raise Exception("incorrect input")

kill_chrome = False
if input("do you want to also close chrome before shutting down? (Y/N): ").lower() == "y":
    kill_chrome = True
    print("Chrome will be shut down.")
else:
    print("k your choice I guess. Don't blame me if you lose some tabs or smth.")

if seconds <= 10:
    raise Exception("Time needs to be more than 10 seconds!")
print(f"{socket.gethostname()} will shut down in {seconds} seconds or {(seconds / 60):.2f} minutes or {(seconds/60/60):.2f} hours")
notification = ToastNotifier()
notification.show_toast("Notification", "you will be notified 3 minutes before the shutdown (if you set the time to something less than 180 seconds you won't get notified though. \nBut oh well who cares.", duration=10)
if seconds > 180:
    sleep(float(seconds - 180))
    notification = ToastNotifier()
    notification.show_toast("Warning", "Your pc will shut down after 3 minutes (180 seconds).", duration = 5)
    sleep(180)
else:
    notification = ToastNotifier()
    notification.show_toast("Warning", f"Your pc will shut down after {(seconds / 60):.2f} minutes ({seconds} seconds).", duration=5)
    sleep(seconds)

print("Shutting down in:")
print("3")
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)
if kill_chrome:
    print("killing chrome")
    os.system("taskkill /im chrome.exe /f")
notification = ToastNotifier()
notification.show_toast("Shutting down", "shutting down", duration = 1)
print("Shutting down...")
os.system("shutdown /s /t 1")