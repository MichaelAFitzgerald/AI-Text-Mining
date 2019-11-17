import pandas as pd
import matplotlib.pylab as plt
import clusters as c
import models.formClusters as f

# with open('data/sentences.txt', 'r', encoding='utf-8') as myfile:
#   data = myfile.read()
# s = v.tokenizer(data)
# s = v.punctRemover(s)
# s = v.numRemover(s)
# s = v.capsRemover(s)
# s = v.stopRemover(s)
# s = v.stemmer(s)
# s = v.concat(s)
# The number at the end of freqFinder is the cutoff point -- i.e., all columns that do not have at least 5 hits will be removed
# d = v.freqFinder(s, data, 5)
d = pd.read_csv('Project4TDM.csv', index_col=0)

x = f.formClusters(d, 100)
x = x.algorithm().sum(axis=1)
x.to_csv('FCAN.csv')

fcan = pd.read_csv("FCAN.csv")
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = d.index
y = list()
for ind in d.index:
    y.append(d.iloc[ind].sum() * fcan.iloc[ind].sum())
ax.scatter(x, y, alpha=0.8, c="red", edgecolors='none', s=30)
plt.title("FCAN Plot")
plt.xlabel("Indices")
plt.ylabel("Sum")
plt.savefig("FCANPlot.png")
plt.show()
# weights, sumMatrix, normalMatrix = c.WTA(d)
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# x = d.index
# y = d.sum(axis=1)
# ax.scatter(x, y, alpha=0.8, c="blue", edgecolors='none', s=30)
# plt.title("TDM Plot")
# plt.xlabel("Indices")
# plt.ylabel("Sum")
# plt.savefig("TDMPlot.png")
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# x = sumMatrix.index
# sum = list()
# weight = list()
# for ind in range(len(d)):
#     sum.append(d.iloc[ind].sum() * sumMatrix['Sum'].iloc[ind])
# for ind in range(len(d)):
#     weight.append(weights.iloc[ind].sum())
# ax.scatter(x, sum, alpha=0.8, c="red", edgecolors='none', s=30)
# plt.title("Weighted Matrix Plot")
# plt.xlabel("Indices")
# plt.ylabel("Sum")
# plt.savefig("WeightedPlot.png")
# plt.show()

