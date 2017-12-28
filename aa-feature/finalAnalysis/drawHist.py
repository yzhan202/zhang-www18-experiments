#!/usr/bin/env python
# import numpy as np
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
#
# mu, sigma = 100, 15
# x = mu + sigma*np.random.randn(10000)
#
# # the histogram of the data
# n, bins, patches = plt.hist(x, 10, normed=1, facecolor='green', alpha=0.75)
# print bins
#
# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# print y
# l = plt.plot(bins, y, 'r--', linewidth=1)
#
# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
# plt.grid(True)
#
# plt.show()



import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

x = [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100]
x = np.sort(x)
num_bins = 5
n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
plt.show()