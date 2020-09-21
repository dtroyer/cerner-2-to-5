#!/usr/bin/env python
# logtime.py - Calculate runtime of reposync log files
# logtime.py <logfile-path>

# Reposync log files use an ISO-8601 formatted timestamp (including
# the timezone offset).  date(1) can't parse this before coreutils 8.21,
# RHEL 6 has coreutils 8.4 so that is out.
# This works on Python 2 with only the standard runtime.

from datetime import datetime
import sys

start_time = ""
end_time = ""
running = ""

with open(sys.argv[1]) as f:
    for line in f:
        if "loaded configuration file" in line:
            start_time = line.split(' ')[0]
        if "Sync completed successfully" in line:
            end_time = line.split(' ')[0]

# Major hack to handle the ISO-8601 timezone field that py2 doesn't do
# The day of year (%U) and day of week (%W) absorb the TZ offset
# and we'll ignore it.  The actual timezone doesn't matter as we
# are looking for delta times here and assume that the timestamps
# are all in the same timezone.
start_obj = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S-%U:%W")
if end_time != "":
    end_obj = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S-%U:%W")
else:
    end_obj = datetime.now()
    running = " (running)"

print("delta: {0:.2f}{1}".format(((end_obj - start_obj).seconds / 3600), running))

# cerner_2^5_2020
