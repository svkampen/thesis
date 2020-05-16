from matplotlib import pyplot as plt
import code
from scipy import polyfit
import scipy.stats
import operator
import numpy as np
import glob

data = []

for f in glob.glob('*switchtimes.data'):
    n = int(f.split('switch')[0])
    data.append((n, [int(x) for x in open(f, 'r').read().split()]))

data.sort(key=operator.itemgetter(0))

xs, ys = zip(*data)

for x,y in data:
    print(f"{x}: {len(y)}")


means = [np.mean(y) for y in ys]

ar, br, r_value, p_value, std_err = scipy.stats.linregress(xs, means)

fig, ax = plt.subplots(figsize=(9,6))

ax.set_yscale('log', basey=10)
ax.set_xscale('log', basex=10)

ax.set_xticks([])
ax.set_xticks([], True)

data.sort(key=operator.itemgetter(0))

bx_artists = ax.boxplot([x[1] for x in data], positions=[x[0] for x in data], widths=[x[0]/10 for x in data], sym='+', showmeans=True, manage_ticks=True, flierprops={'markeredgewidth': 0.5})

yticks = [10, 100]
yticksmin = [20,30,40,50,60,70,80,90,120,140]
ax.set_yticks(yticks)
ax.set_yticks(yticksmin,True)
ax.set_yticklabels(yticks)
ax.set_yticklabels(yticksmin,minor=True)

reg_xs = np.linspace(min(xs)*0.95, max(xs)*1.05, 4000)

def f(reg_xs):
    return ar * reg_xs + br

line = ax.plot(reg_xs, f(reg_xs), linestyle='dotted')

ax.legend([bx_artists['means'][0], bx_artists['medians'][0], line[0]], ['Mean', 'Median', f'Linear fit to mean ($r^2$ = {r_value**2:.4f})'])

ax.set_xlabel('Number of priorities')
ax.set_ylabel('Task switch time (μs)')

fig.savefig('boxplot.eps')
plt.show()
