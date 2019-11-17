import random, math
import pandas as pd


class formClusters:

    def __init__(self, TDM, cycles=150):
        self.TDM = TDM
        self.cycles = cycles

    def algorithm(self):
        m = []
        m.append(1)
        weights = pd.DataFrame(columns=self.TDM.columns)
        weights.loc[0] = self.TDM.loc[0]
        for k in range(self.cycles):
            r = k / 10
            m.__setitem__(0, 1)
            numClusters = 1
            for i in range(len(self.TDM.index)):
                threshold = 0
                for j in range(numClusters):
                    net = 0
                    for col in self.TDM.columns:
                        net = net + (self.TDM[col].iloc[i] - weights[col].iloc[i]) ** 2
                    net = math.sqrt(net)
                    if net < r:
                        for col in self.TDM.columns:
                            weights[col].iloc[j] = (self.TDM[col].iloc[i] + weights[col].iloc[j] * m.__getitem__(j)) / (
                                        m.__getitem__(j) + 1)
                        m.__setitem__(j, m.__getitem__(j) + 1)
                    threshold = threshold + 1
                if threshold == numClusters:
                    numClusters = numClusters + 1
                    weights.loc[numClusters - 1] = self.TDM.loc[i]
                    m.append(1)
            print("cycles: {0} numClusters: {1}".format(k, numClusters))
        return weights
