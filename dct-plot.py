import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="darkgrid")

data = pd.read_pickle(os.path.join(".", "out-dct", "data-result.pkl"))

g = sns.lmplot(data=data, x='Dimension', y='Time', hue='Type')
g.set(yscale='log')
plt.show()
fig = g.get_figure()
fig.savefig("./images/plotdct2.png")
