from matplotlib import pyplot as plt
from collections import Counter
import numpy as np
import sys

print_peak_deltas = False

def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        if (y_value > 1000):
            label = f"{(y_value // 1000)}k"
        else:
            label = str(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.


try:
    fname = sys.argv[1]
except IndexError:
    fname = 'switchtimes_rr.data'

print(f"Using data: {fname}")

with open(fname, 'r') as f:
    data = [*map(int, f.read().split())]

print(f"Mean: {np.mean(data)}\nStd. dev: {np.std(data)}\nMedian: {np.median(data)}")
print(f"{len(data)}")

if print_peak_deltas:
    old_n = 0

    for n, i in enumerate(data):
        if i > 13:
            print(n - old_n, i)
            old_n = n

c = Counter(data)

pairs = [*c.items()]
pairs.sort(key=lambda x: x[0])

xs, ys = zip(*pairs)

fig = plt.gcf()
plt1 = plt.gca()

fig.set_size_inches(10,6)

ticks = [*range(min(xs), max(xs) + 1)]
labels = map(str, ticks)

plt1.set_xticks(ticks)
plt1.set_xticklabels(labels)
plt1.bar(xs, ys, log=True, width=0.7, color='cornflowerblue')
plt1.set_xlabel('Task switch time (µs)')
plt1.set_ylabel('Number of task switches with given task switch time')

add_value_labels(plt1)

plt.tight_layout()

fig.savefig('task_switch_time.eps')
plt.show()
