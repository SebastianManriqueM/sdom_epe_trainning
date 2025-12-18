# -*- coding: utf-8 -*-
"""
Created on Wed May 28 14:50:00 2025

@author: mkoleva
"""
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mc # For the legend
from matplotlib.colors import LinearSegmentedColormap

# Another utility for the legend
from matplotlib.cm import ScalarMappable
import os

current_folder = os.getcwd()
print("Current folder:", current_folder)

# Configuration----------------------------------
start_date = '2025-01-01 00:00:00' # Or any starting date
case_name = "br_test_daily_b"
output_folder_name = f"sample_results_{case_name}"
# Configuration----------------------------------
# Heat map
folder_csv_results = os.path.join(current_folder, output_folder_name)
results = pd.read_csv(os.path.join(folder_csv_results, f"OutputGeneration_{case_name}.csv"))


results_LiIon = pd.DataFrame(results.loc[results["Technology"] == "Li-Ion", "State of charge (MWh)"])
n_periods = len(results)
hours = np.arange(1, n_periods)

# Create the DataFrame with the hours
df = pd.DataFrame(data=hours, columns=["Hour of the Year"])

# Create a DatetimeIndex for a year (assuming the data starts at the beginning of the year)

datetime_index = pd.date_range(start=start_date, periods=n_periods, freq='H')

# Assign the DatetimeIndex to the DataFrame
df['timestamp'] = datetime_index

# Extract day of year and hour of day
df['day_of_year'] = df['timestamp'].dt.dayofyear
df['hour_of_day'] = df['timestamp'].dt.hour

# Re-arrange SOC values
SOC = results_LiIon['State of charge (MWh)'].values.reshape(24, len(df['day_of_year'].unique()), order="F")
norm_SOC = SOC*100/np.max(SOC) # Percentage %

# # Compute x and y grids, passed to `ax.pcolormesh()`.

# # The first + 1 increases the length
# # The outer + 1 ensures days start at 1, and not at 0.
xgrid = np.arange(df['day_of_year'].max() + 1) + 1

# # Hours start at 0, length 2
ygrid = np.arange(25)

fig, ax = plt.subplots(figsize=(12,10))

CB_color_cycle = [
                 '#00296b','#003f88', '#00509d',  '#1F449C' , '#ffd500', '#fdc500',  '#F05039'                             
                  ]

custom_cmap = LinearSegmentedColormap.from_list("my_cmap", CB_color_cycle)

heatmap = ax.pcolormesh(xgrid, ygrid, norm_SOC, cmap = custom_cmap)
ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=16) 
ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=16)
ax.set_frame_on(False) # remove all spines
current_xticks = plt.xticks()[0]
current_xticklabels = [label.get_text() for label in plt.xticks()[1]]

# Add the last x-value if it's not already a tick
if xgrid[-1] not in current_xticks:
    new_xticks = np.append(current_xticks, xgrid[-1])
    new_xticklabels = np.append(current_xticklabels, str(xgrid[-1]))
    plt.xticks(new_xticks, new_xticklabels)

# Get the current tick locations and labels for y-axis
current_yticks = plt.yticks()[0]
current_yticklabels = [label.get_text() for label in plt.yticks()[1]]

# Add the last y-value if it's not already a tick
if ygrid[-1] not in current_yticks:
    new_yticks = np.append(current_yticks, ygrid[-1])
    new_yticklabels = np.append(current_yticklabels, str(ygrid[-1]))
    plt.yticks(new_yticks, new_yticklabels)
plt.xlim(0, 365)  
plt.ylim(0,24)
plt.colorbar(heatmap)
plt.xlabel("Day of the year", fontsize = 20)
plt.ylabel("Hour of the day", fontsize = 20)
plt.title("Annual Hourly Li-Ion Battery Storage State of Charge (%)", y=1.05, fontsize = 20)
plt.savefig('SOC_Li_ion.png', dpi=1000)
