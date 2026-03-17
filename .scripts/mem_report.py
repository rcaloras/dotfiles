#!/usr/bin/env python3

import subprocess
import re
import platform

# ANSI colors
RESET   = '\033[0m'
BOLD    = '\033[1m'
CYAN    = '\033[36m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
GREEN   = '\033[32m'
MAGENTA = '\033[35m'
WHITE   = '\033[37m'

def val_color(mb, low, high):
    """Green if below low threshold, yellow if below high, red if above."""
    if mb < low:
        return GREEN
    elif mb < high:
        return '\033[33m'  # yellow
    else:
        return '\033[31m'  # red

def free_color(mb):
    """Green if plenty free, yellow if getting low, red if critical."""
    if mb > 2000:
        return GREEN
    elif mb > 500:
        return YELLOW
    else:
        return '\033[31m'  # red

def report_macos():
    # Get process RSS total
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
    sep = re.compile(r'[\s]+')
    rssTotal = 0
    for row in ps.split('\n')[1:]:
        rowElements = sep.split(row.strip())
        try:
            rssTotal += float(rowElements[0]) * 1024
        except:
            pass

    # Get vm_stat
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()
    vmLines = vm.split('\n')

    # Parse page size from first line: "Mach Virtual Memory Statistics: (page size of 16384 bytes)"
    page_size_match = re.search(r'page size of (\d+) bytes', vmLines[0])
    page_size = int(page_size_match.group(1)) if page_size_match else 4096

    sep = re.compile(r':[\s]+')
    vmStats = {}
    for line in vmLines[1:]:
        line = line.strip()
        parts = sep.split(line)
        if len(parts) == 2:
            vmStats[parts[0].strip('"')] = int(parts[1].strip('.')) * page_size

    def mb(key):
        return vmStats.get(key, 0) / 1024 / 1024

    wired_mb      = mb("Pages wired down")
    active_mb     = mb("Pages active")
    inactive_mb   = mb("Pages inactive")
    free_mb       = mb("Pages free")
    compressed_mb = mb("Pages occupied by compressor")
    available_mb  = free_mb + inactive_mb
    total_mb      = rssTotal / 1024 / 1024

    print('%sWired Memory:%s\t\t%s%d MB%s'        % (CYAN,    RESET, val_color(wired_mb, 2000, 6000),      wired_mb,      RESET))
    print('%sActive Memory:%s\t\t%s%d MB%s'       % (YELLOW,  RESET, val_color(active_mb, 4000, 8000),     active_mb,     RESET))
    print('%sInactive Memory:%s\t%s%d MB%s'       % (BLUE,    RESET, RESET,                                inactive_mb,   RESET))
    print('%sCompressed Memory:%s\t%s%d MB%s'     % (WHITE,   RESET, val_color(compressed_mb, 2000, 6000), compressed_mb, RESET))
    print('%sFree Memory:%s\t\t%s%d MB%s'         % (GREEN,   RESET, free_color(free_mb),                  free_mb,       RESET))
    print('%sAvailable Memory:%s\t%s%d MB%s'      % (GREEN,   RESET, free_color(available_mb),             available_mb,  RESET))
    print('%sReal Mem Total (ps):%s\t%s%.3f MB%s' % (MAGENTA, RESET, BOLD,                                 total_mb,      RESET))

def report_linux():
    with open('/proc/meminfo', 'r') as f:
        meminfo = f.read()

    sep = re.compile(r':\s+')
    memStats = {}
    for line in meminfo.split('\n'):
        parts = sep.split(line.strip())
        if len(parts) == 2:
            memStats[parts[0]] = int(parts[1].split()[0]) * 1024  # kB -> bytes

    def mb(key):
        return memStats.get(key, 0) / 1024 / 1024

    total_mb     = mb("MemTotal")
    free_mb      = mb("MemFree")
    available_mb = mb("MemAvailable")
    buffers_mb   = mb("Buffers")
    cached_mb    = mb("Cached")
    used_mb      = total_mb - available_mb

    print('%sTotal Memory:%s\t\t%s%d MB%s'     % (CYAN,    RESET, BOLD,                                            total_mb,     RESET))
    print('%sUsed Memory:%s\t\t%s%d MB%s'      % (YELLOW,  RESET, val_color(used_mb, total_mb * 0.5, total_mb * 0.8), used_mb,   RESET))
    print('%sBuffers:%s\t\t%s%d MB%s'          % (BLUE,    RESET, RESET,                                           buffers_mb,   RESET))
    print('%sCached:%s\t\t\t%s%d MB%s'         % (BLUE,    RESET, RESET,                                           cached_mb,    RESET))
    print('%sFree Memory:%s\t\t%s%d MB%s'      % (GREEN,   RESET, free_color(free_mb),                             free_mb,      RESET))
    print('%sAvailable Memory:%s\t%s%d MB%s'   % (GREEN,   RESET, free_color(available_mb),                        available_mb, RESET))

if platform.system() == 'Darwin':
    report_macos()
else:
    report_linux()
