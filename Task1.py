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

# 5. Time Series Analysis of Reviews
# Plot: Create a line plot to show the trend of number_of_reviews over time
# (last_review) for each neighbourhood_group.
# Details: Use different colors for each neighborhood group, smooth the data with a
# rolling average, and add titles, axis labels, and a legend.

# Convert 'last_review' to a datetime format
df['last_review'] = pd.to_datetime(df['last_review'])



# Group the data by neighborhood group and last review month, then count the number of reviews
#grouped_data = df.groupby(['neighbourhood_group', pd.Grouper(key='last_review', freq='ME')])['number_of_reviews'].count().reset_index()

# Group data by neighborhood group and month, count reviews
grouped_data = df.groupby(['neighbourhood_group', df['last_review'].dt.to_period('M')])['number_of_reviews'].count().reset_index()



# Calculate a rolling average of the number of reviews using rolling(window=3)
rolling_avg = grouped_data.groupby('neighbourhood_group')['number_of_reviews'].rolling(window=3).mean()



# Check the number of levels in the index (optional)
num_levels = rolling_avg.index.nlevels

if num_levels > 1:  # If there are multiple levels (unlikely based on the error)
    # Assuming the second level is the date (month), use this:
    rolling_avg = rolling_avg.reset_index(level=0)
else:  # If there's only one level (or no level)
    # No level argument needed, reset the index directly
    rolling_avg = rolling_avg.reset_index()

# Create the line plot with clear labels, title, and legend
sns.lineplot(
    x='last_review',
    y='number_of_reviews',
    hue='neighbourhood_group',
    style='neighbourhood_group',  # Add style for potential marker differentiation
    data=grouped_data,
    marker='o'  # Add markers for better visual representation
)

# Create a line plot for each neighborhood group

def test():
    for group in df['neighbourhood_group'].unique():
        group_data = df[df['neighbourhood_group'] == group]  # Filter data for each group
        neighbourhood_grouped_data = group_data.groupby(pd.Grouper(key='last_review', freq='ME'))['number_of_reviews'].count().reset_index()
        neighbourhood_grouped_data = neighbourhood_grouped_data.assign(neighbourhood_group=grouped_data['neighbourhood_group'])
        rolling_avg = neighbourhood_grouped_data.groupby('neighbourhood_group')['number_of_reviews'].rolling(window=3).mean().reset_index()
        # Verify column presence before plotting
        if 'last_review' in neighbourhood_grouped_data.columns:
            sns.lineplot(x='last_review', y='number_of_reviews', data=neighbourhood_grouped_data, label=group)
        else:
            print(f"Warning: 'last_review' not found in data for group: {group}")
    print(neighbourhood_grouped_data)
    print(neighbourhood_grouped_data.columns)
    print(rolling_avg)
    print(rolling_avg.columns)

plt.title('Trend of Number of Reviews Over Time (By Neighborhood Group)')
plt.xlabel('Last Review Month')
plt.ylabel('Number of Reviews')
plt.legend(title='Neighborhood Group')
#plt.show()