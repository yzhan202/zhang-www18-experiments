import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
# y_pos = np.arange(len(objects))
# performance = [10, 8, 6, 4, 2, 1]
#
# plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.xticks(y_pos, objects)
# plt.ylabel('Usage')
# plt.title('Programming language usage')
#
# plt.show()

# Get current size
fig_size = plt.rcParams["figure.figsize"]
print "Current size:", fig_size
# Set figure width to 12 and height to 9
fig_size[0] = 15
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size


axes = plt.gca()
axes.set_ylim([0.6, 0.92])

for tick in axes.xaxis.get_major_ticks():
    tick.label.set_fontsize(24)
for tick in axes.yaxis.get_major_ticks():
    tick.label.set_fontsize(24)

plt.xlabel('', fontsize=28)
plt.ylabel('AUC-ROC', fontsize=28)

objects = ('PSL-Big', 'Linguistic-PSL', 'Psycho', 'WithoutLIWC')

y_pos = np.arange(len(objects))

performance = [0.9032, 0.8785, 0.7077, 0.6409]

plt.bar(y_pos, performance, align='center', facecolor='black', width=0.5)
plt.xticks(y_pos, objects)

# plt.show()

plt.savefig('auc-roc.eps', format='eps')
plt.savefig('auc-roc.pdf', format='pdf')