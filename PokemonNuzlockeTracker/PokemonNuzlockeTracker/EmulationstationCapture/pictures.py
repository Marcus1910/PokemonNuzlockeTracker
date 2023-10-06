import os
import time

for i in range(15):
    # Use the scrot command to take a screenshot
    os.system(f'scrot {i}.png')

    # Wait for one second before taking the next screenshot
    time.sleep(1)