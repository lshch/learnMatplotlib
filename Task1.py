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


# 1. Neighborhood Distribution of Listings
# Plot: Create a bar plot to show the distribution of listings across different
# neighbourhood_group.
# Details: Label each bar with the count of listings, use distinct colors for each
# neighborhood group, and add titles and axis labels.
# Count the number of listings per neighborhood group

neighborhood_counts = df['neighbourhood_group'].value_counts()

# Create the bar plot
plt.figure(figsize=(6, 6))
sns.barplot(x=neighborhood_counts.index, y=neighborhood_counts.values, hue=neighborhood_counts.index, palette='pastel', legend=False)


plt.title('Distribution of Airbnb Listings by Neighborhood Group')
plt.xlabel('Neighborhood Group')
plt.ylabel('Number of Listings')

# Add labels to the bars
for index, value in enumerate(neighborhood_counts.values):
    plt.text(index, value, str(value), ha='center', va='bottom')

# Plot: Create a bar plot to show the distribution of listings across different
# neighbourhood_group.
plt.show()

# 2.  Price Distribution Across Neighborhoods
# Plot: Generate a box plot to display the distribution of price within each
# neighbourhood_group.
# Details: Use different colors for the box plots, highlight outliers, and add
# appropriate titles and axis labels.

# Create a box plot
sns.boxplot(x='neighbourhood_group', y='price', data=df)
plt.title('Price Distribution by Neighborhood Group')
plt.xlabel('Neighborhood Group')
plt.ylabel('Price')
plt.show()

# 3. Room Type vs. Availability
# Plot: Create a grouped bar plot to show the average availability_365 for each
# room_type across the neighborhoods.
# Details: Include error bars to indicate the standard deviation, use different colors
# for room types, and add titles and axis labels.

# Group the data by neighborhood and room type, then calculate the mean and standard deviation of availability
grouped_data = df.groupby(['neighbourhood_group', 'room_type'])['availability_365'].agg(['mean', 'std']).reset_index()

# Create a grouped bar plot
sns.barplot(x='neighbourhood_group', y='mean', hue='room_type', data=grouped_data, palette='pastel', errorbar='sd') # errorbar: 'ci', 'se', 'sd'
plt.title('Average Availability by Neighborhood and Room Type')
plt.xlabel('Neighborhood Group')
plt.ylabel('Average Availability (Days)')
plt.legend(title='Room Type')
plt.show()

# 4. Correlation Between Price and Number of Reviews
# Plot: Develop a scatter plot with price on the x-axis and number_of_reviews on the
# y-axis.
# Details: Differentiate points by room_type using color or marker style, add a
# regression line to identify trends, and include a legend, titles, and axis labels.

# Create a scatter plot
sns.scatterplot(x='price', y='number_of_reviews', data=df, hue='room_type', palette='pastel')

#print(df['number_of_reviews'])

# Add a regression line
sns.regplot(x='price', y='number_of_reviews', data=df, scatter=False, color='blue', line_kws={'linestyle': '-'})

plt.title('Price vs. Number of Reviews by Room Type')
plt.xlabel('Price')
plt.ylabel('Number of Reviews')
plt.legend(title='Room Type')
plt.show()
