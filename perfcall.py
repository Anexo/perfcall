#!/usr/bin/python

# Basic script to import CSV files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------

#Copyright (C) 2015 by Tomas Lopez-Fragoso Rumeu <https://github.com/Anexo>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>
#------------------------------------------

import subprocess
import sys
import json

# If user does not introduce args, they will be ask through prompt:
if len(sys.argv) == 1:
        #Questions to user:
        print ''
        core_ts_perf = raw_input(' Which core for taskset perf? --> ')
        core_perf = raw_input(' Which core for perf to poll and executing task? --> ')
        interval = raw_input(' Time interval (e.g. 500 for 500ms)? --> ')

        #Energy event selection:
        perf_event = raw_input(' Select perf energy event:\n  1:Energy-Cores\n  2:Energy-pkg\n  3:Energy-ram\n --> ')
        task = raw_input(' Task to execute? --> ')
else:
        core_ts_perf = int(sys.argv[1])
        core_perf = int(sys.argv[2])
        interval = int(sys.argv[3])
        perf_event = sys.argv[4]
        if len(sys.argv) >= 7:
                task = sys.argv[5] + ' ' + sys.argv[6]
        else:
                task = sys.argv[5]

#Selecting proper energy event:
if perf_event == '1':
        perf_event_text = "power/energy-cores/"
elif perf_event == '2':
        perf_event_text = "power/energy-pkg/"
else:
        perf_event_text = "power/energy-ram/"

#Final command:
cmd = 'sudo taskset -c %s perf stat -C %s -I %s -x , -e "%s" taskset -c %s %s' % (core_ts_perf, core_perf, interval, perf_event_text, core_perf, task)

#Print Execution:
print '\n Executing following task:'
print ' --> ' + cmd
print '\n Executing...\n'

final_cmd = cmd.split()
print final_cmd

#Output file:
with open('output.txt', 'w') as outfile:
        outfile.write('Command:\n---> ' + cmd + '\n\n')
        subprocess.Popen(final_cmd, stderr=outfile)
