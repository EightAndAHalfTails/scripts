#!/usr/bin/env python
import time
def getTimes(alarms):
    while(True):
        duration = eval(input("Enter time in minutes, 0 to exit: "))
        if(duration == 0):
            break
        name = input("Enter food name: ")
        alarms.append((name, duration))
    return

def setAlarms(alarms):
    total_time = max(alarm[1] for alarm in alarms)

    alarm_time = time.gmtime(time.time()+60*total_time)
    print(time.strftime("%H:%M", alarm_time) + ", take out.")

    for alarm in alarms:
        delay = total_time - alarm[1]
        alarm_time = time.gmtime(time.time()+60*delay)
        print(time.strftime("%H:%M", alarm_time) + ", put in " + alarm[0])
    return

alarms = []
getTimes(alarms)
setAlarms(alarms)
