#!/usr/bin/env python3

import subprocess
import re

# ANSI colors
RESET  = '\033[0m'
BOLD   = '\033[1m'
CYAN   = '\033[36m'
YELLOW = '\033[33m'
BLUE   = '\033[34m'
GREEN  = '\033[32m'
MAGENTA= '\033[35m'
RED    = '\033[31m'

def val_color(mb, low, high):
    """Green if below low threshold, yellow if below high, red if above."""
    if mb < low:
        return GREEN
    elif mb < high:
        return YELLOW
    else:
        return RED

def free_color(mb):
    """Green if plenty free, yellow if getting low, red if critical."""
    if mb > 2000:
        return GREEN
    elif mb > 500:
        return YELLOW
    else:
        return RED

# Get process info
ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()

# Iterate processes
processLines = ps.split('\n')
sep = re.compile(r'[\s]+')
rssTotal = 0 # kB
for row in range(1,len(processLines)):
    rowText = processLines[row].strip()
    rowElements = sep.split(rowText)
    try:
        rss = float(rowElements[0]) * 1024
    except:
        rss = 0 # ignore...
    rssTotal += rss

# Process vm_stat
vmLines = vm.split('\n')
sep = re.compile(r':[\s]+')
vmStats = {}
for row in range(1,len(vmLines)-2):
    rowText = vmLines[row].strip()
    rowElements = sep.split(rowText)
    vmStats[(rowElements[0])] = int(rowElements[1].strip('.')) * 4096

wired_mb    = vmStats["Pages wired down"] / 1024 / 1024
active_mb   = vmStats["Pages active"]     / 1024 / 1024
inactive_mb = vmStats["Pages inactive"]   / 1024 / 1024
free_mb     = vmStats["Pages free"]       / 1024 / 1024
total_mb    = rssTotal / 1024 / 1024

print('%sWired Memory:%s\t\t%s%d MB%s'    % (CYAN,    RESET, val_color(wired_mb,  2000, 6000), wired_mb,    RESET))
print('%sActive Memory:%s\t\t%s%d MB%s'   % (YELLOW,  RESET, val_color(active_mb, 4000, 8000), active_mb,   RESET))
print('%sInactive Memory:%s\t%s%d MB%s'   % (BLUE,    RESET, RESET,                            inactive_mb, RESET))
print('%sFree Memory:%s\t\t%s%d MB%s'     % (GREEN,   RESET, free_color(free_mb),              free_mb,     RESET))
print('%sReal Mem Total (ps):%s\t%s%.3f MB%s' % (MAGENTA, RESET, BOLD,                         total_mb,    RESET))
