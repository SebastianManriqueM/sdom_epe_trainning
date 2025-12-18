"""
Created on Wed May 28 14:50:00 2025

@author: mkoleva
"""
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as mc # For the legend
from matplotlib.colors import LinearSegmentedColormap

# Another utility for the legend
from matplotlib.cm import ScalarMappable
import os

current_folder = os.getcwd()
print("Current folder:", current_folder)

folder_csv_results = os.path.join(current_folder, "sample_results_br_test_daily_b")
# Open the csv file
data = pd.read_csv(os.path.join(folder_csv_results, "OutputSummary_br_test_daily_b.csv"))

# Doughnut chart
gen_capacity = pd.DataFrame(data.loc[data["Metric"] == "Capacity", "Optimal Value"][0:3]).reset_index(drop=True)
gen_capacity_label = pd.DataFrame(data.loc[data["Metric"] == "Capacity", "Technology"][0:3]).reset_index(drop=True)
sto_capacity = pd.DataFrame(data.loc[data["Metric"] == "Average power capacity", "Optimal Value"][0:4]).reset_index(drop=True)
sto_capacity_label = pd.DataFrame(data.loc[data["Metric"] == "Average power capacity", "Technology"][0:4]).reset_index(drop=True)
sto_capacity_label_strings = [str(label) for label in sto_capacity_label['Technology']]

capacity = pd.concat([gen_capacity, sto_capacity])
capacity_labels = pd.concat([gen_capacity_label, sto_capacity_label])
total_capacity = round(sum(capacity['Optimal Value'])/1000) #GW
capacity_n_labels = pd.concat([capacity_labels, capacity], axis=1)


capacity_filtered = capacity_n_labels[capacity_n_labels['Optimal Value'] > 0]

color_map = {'Thermal': '#5E1688', 
             'Solar PV': '#FFC903', 
             'Wind': '#00B6EF'}

# Define a list of colors for storage technologies
storage_colors = ['#FF4A88', '#FF4741', '#CC0079', '#FF7FBB', '#7F7FFF', '#FFB347', '#47FFB3']

# Add storage technologies to color_map dynamically
for i, tech in enumerate(sto_capacity_label_strings):
    color_map[tech] = storage_colors[i % len(storage_colors)]
 
colors = [color_map[label] for label in capacity_filtered['Technology']]  
    

fig, ax = plt.subplots(figsize=(10, 10))
ax.pie(capacity_filtered['Optimal Value'], 
       #labels=capacity_labels['Technology'], 
       startangle=90, colors = colors, autopct='%1.1f%%', pctdistance=0.8,  textprops={'fontsize': 20, 'fontweight':'bold','color':'black'})

# Draw a circle at the center to create the donut effect
centre_circle = plt.Circle((0, 0), 0.60, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Ensure the circle is a circle
ax.axis('equal')

# Display the chart
plt.title('Capacity per technology (MW)', y = 0.95, fontsize = 28)
legend = plt.legend(capacity_filtered['Technology'], bbox_to_anchor=(1.15, 0.9), loc="upper right", frameon=False, fontsize = 20, labelcolor='black')

centre_text = f'{total_capacity}GW'
centre_text_line_2 = f'Total Capacity'
ax.text(0,0.1, centre_text, horizontalalignment='center', 
            verticalalignment='center', 
            fontsize=32, fontweight='bold',
            color='black')
ax.text(0,-0.1, centre_text_line_2, horizontalalignment='center', 
            verticalalignment='center', 
            fontsize=30, fontweight='bold',
            color='black')
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show()
plt.savefig(os.path.join(current_folder,'training_material','training_sesion_1','Capacity_per_tech.png'), dpi=1000)

