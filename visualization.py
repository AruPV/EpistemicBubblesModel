import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv = pd.read_csv("1000_round.csv")
p1 = sns.heatmap(csv, xticklabels=False, yticklabels= False)
plt.title('1000 Rounds')
fig = p1.get_figure()
fig.savefig("1000_rounds.png")