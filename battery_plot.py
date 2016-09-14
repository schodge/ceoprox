#!/usr/bin/python3
"""
battery_plot.py
Copyright Shayne Hodge and SnapLogic Inc, 2016
All parts of the code not under another license are licensed under
a standard 3-clause BSD license.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df_b = pd.read_csv('d:/repos/prototype/ceo_prox/electron_dash/sample_battery_data.csv')
# Can't regress on datatime stamps. Seems like this conversion is
# kludgey and a better way exists
time_temp = pd.DatetimeIndex(df_b['time'])
time_temp_min = (24 * 60 * time_temp.day) + (60 * time_temp.hour) + time_temp.minute
delta_time = time_temp_min - time_temp_min[0]
df_b['time_elapsed_min'] = delta_time
sns.regplot(x="time_elapsed_min", y="capacity", data=df_b, fit_reg=True)
plt.show()
