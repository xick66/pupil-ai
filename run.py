import subprocess
import os
import signal
import sys
import time
import psutil

subprocess.Popen(['poetry', 'run', 'flask', '--app',
                 'server', 'run'], shell=True)
subprocess.Popen(['npm', 'run', 'start'], shell=True)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    for process in psutil.process_iter():
        if "node" in process.name() or "flask" in process.name():
            os.kill(process.pid, signal.SIGTERM)

    sys.exit(0)
