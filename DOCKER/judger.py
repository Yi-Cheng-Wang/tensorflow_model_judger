from evaluate import evaluate
import os
from time import sleep

if not os.path.exists('/evaluate/model.h5'):
    exit()

output = evaluate('/evaluate/model.h5')
print('<flag: score_appear_here>', end='')
print(output, end='')
