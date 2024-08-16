import pandas as pd
import matplotlib.pyplot as plt
# Seaborn - Python data visualization library built on top of Matplotlib. It provides a high-level interface for creating attractive and informative statistical graphics. Seaborn offers a wide range of functions for visualizing different types of data, including:  
#
# Distributions: Histograms, KDE plots, and rug plots for visualizing the distribution of a single variable.
# Relationships: Scatter plots, line plots, and joint plots for exploring relationships between two or more variables.
# Categorical data: Bar plots, count plots, and box plots for visualizing categorical data.
# Grids: Facet grids and pair plots for organizing multiple plots together.
# Heatmaps: Heatmaps for visualizing two-dimensional data.
import seaborn as sns

# Load the dataset
# Reads the CSV file into a Pandas DataFrame named airbnb_df.
df = pd.read_csv('AB_NYC_2019.csv')


# 7.  Room Type and Review Count Analysis
# Plot: Create a stacked bar plot to display the number_of_reviews for each
# room_type across the neighbourhood_group.
# Details: Stack the bars by room type, use different colors for each room type, and
# add titles, axis labels, and a legend.


# Group the data by neighbourhood_group and room_type, then sum the number of reviews
grouped_data = df.groupby(['neighbourhood_group', 'room_type'])['number_of_reviews'].sum().reset_index()

# Create a stacked bar plot using Seaborn
sns.barplot(x='neighbourhood_group', y='number_of_reviews', hue='room_type', data=grouped_data, palette='viridis')

# Set labels and title
plt.xlabel('Neighborhood Group')
plt.ylabel('Number of Reviews')
plt.title('Room Type and Review Count by Neighborhood')

# Show the plot
plt.show()