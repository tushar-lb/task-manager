
from subprocess import check_output
import time
from datetime import datetime
import subprocess
from time import sleep

TIMEOUT=50

def get_pid(name):
    return check_output(["pidof",name])

def take_jstack():
    status_ok = False
    time_check = 0
    count = 0
    while not status_ok:
        time_check = time_check + 5
        if time_check > TIMEOUT:
            status_ok = True
            break
        java_process_id=get_pid("java")
        current_date_time = time.strftime("%Y_%m_%d-%H_%M_%S")
        file_name="jstack_%s_%s.out" % (java_process_id, current_date_time)
        cmd = "jstack -l %s > %s " % (java_process_id, file_name)
        status, output = subprocess.getstatusoutput(cmd)
        if status == 0:
            print("File %s generated successfully." % file_name)
            count += 1
        sleep(5)
    print("Total jstack files: %s" % count)

take_jstack()