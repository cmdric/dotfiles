#!/usr/bin/python
import time
import sys
from pathlib import Path
bootup = True

while True:
    fi0 = '/sys/class/power_supply/BAT0/status'
    fiP = Path(fi0)
    if fiP.is_file():
        fiOP = open('/sys/class/power_supply/BAT0/status')
        line0 = fiOP.readline()
        fiOP.close()
        if line0 != "Discharging\n":
            bootup = True
        else:
            f = open('/sys/class/power_supply/BAT0/current_now')
            line = f.readline()
            f.close()
            if bootup:
                fw = open('/home/potterat/.config/awesome/powercons.txt','w')
                bootup = False
            else:
                fw = open('/home/potterat/.config/awesome/powercons.txt','a')
                fw.write("%s" %line)
            sys.stdout.flush()
            fw.close()
    sys.stdout.flush()
    time.sleep(2)

