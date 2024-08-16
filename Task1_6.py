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

# 6. Price and Availability Heatmap
# Plot: Generate a heatmap to visualize the relationship between price and
# availability_365 across different neighborhoods.
# Details: Use a color gradient to represent the intensity of the relationship, label the
# axes, and include a color bar for reference.

# Group the data by neighborhood and calculate the mean of price and availability_365
print(df.columns)
if 'neighbourhood_group' in df.columns:
    print('Column neighbourhood_group is exists')

grouped_data = df.groupby('neighbourhood_group')[['price', 'availability_365']].mean().reset_index()

print(grouped_data)

# Create a heatmap using seaborn
sns.heatmap(grouped_data[['price', 'availability_365']], annot=True, cmap='viridis', linewidths=0.5)

# Set labels and title
plt.xlabel('Price')
plt.ylabel('Availability 365')
plt.title('Price vs. Availability 365 by Neighborhood')

# Show the plot
plt.show()