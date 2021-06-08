import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="darkgrid")

data = pd.read_pickle(os.path.join(".", "out-dct", "data-dct.pkl"))
data_fft = pd.read_pickle(os.path.join(".", "out-dct", "data-fft.pkl"))
data_my_dct = pd.DataFrame({"HomeMade DCT": [np.nan, np.nan, np.nan]},
                           index=[8, 9, 10])
frames = [data_fft, data_my_dct]
result = pd.concat(frames, axis=1)
frames = [data, result]
result = pd.concat(frames)
g = sns.lineplot(data=result)
g.set(yscale='log')
values = ['2^4', '2^5', '2^6', '2^7', '2^8', '2^9', '2^10', '2^11', '2^12', '2^13', '2^14']
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], values)
plt.show()
fig = g.get_figure()
fig.savefig("./images/plotdct2.png")
