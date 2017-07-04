import sys, time
from progressbar import *

total = 1000


progress = ProgressBar()
for i in progress(range(total)):
    print i
    time.sleep(0.01)

pbar = ProgressBar().start()
for i in range(1, 1000):
    print i
    pbar.update(int((i / (total - 1)) * 100))
    time.sleep(0.01)
pbar.finish()


widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')),
           ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
for i in range(1000000):
    # do something
    pbar.update(10 * i + 1)
    time.sleep(0.0001)
pbar.finish()