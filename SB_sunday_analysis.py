#Will I get a DMCA takedown for using the term Super Bowl? Lets find out!

import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))

conn = sqlite3.connect("chucks.db")

df = pd.read_sql_query('''SELECT * from Beerlist WHERE abv != "X"''', conn)
df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H:%M:%S")
df = df[(df.datetime >= pd.to_datetime("2016-02-07 10:00:00",\
        "%Y-%m-%d %H:%M:%S")) & (df.datetime <= pd.to_datetime("2016-02-08 00:01:00",\
        format="%Y-%m-%d %H:%M:%S"))]

df['pint_cost'] = df['pint_cost'].str.lstrip('$').astype('float64')
df['abv'] = df['abv'].astype('float64')
df['print_label'] = df['brewery'] + ":" + df['beer']

grouped_count = pd.DataFrame({'count' : df.groupby("print_label",\
        as_index=False).size()}).reset_index()
grouped_count = grouped_count.set_index('print_label')
grouped_count['count'] = grouped_count['count'] / 4.0

df = df.set_index('print_label')
df = df.ix[:, 'pint_cost':]
key_metrics = grouped_count.join(df)

key_metrics = key_metrics.drop_duplicates()

print key_metrics.sort(['count'], axis=0)[0:10]
sns_plot = sns.lmplot("abv", "count", data=key_metrics)
sns_plot.set_axis_labels('ABV', 'Hours on tap')
sns_plot1 = plt.gcf()
sns_plot1.savefig("SB_abv_count.png")

sns_plot = sns.lmplot("pint_cost", "count", data=key_metrics)
sns_plot.set_axis_labels('Pint cost', 'Hours on tap')
sns_plot1 = plt.gcf()
sns_plot1.savefig("SB_cost_count.png")

fig, ax = plt.subplots()
fig.set_size_inches(12, 8)
key_metrics.plot('abv', 'pint_cost', kind='scatter', ax=ax)
key_metrics['print_label'] = key_metrics.index

label_point(key_metrics.abv, key_metrics.pint_cost, key_metrics.print_label, ax)

labeled_plot = plt.gcf()
labeled_plot.savefig("SB_labeled.png")
