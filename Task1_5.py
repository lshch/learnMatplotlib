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


def print_dataframe_info(df, message=None):
  """Prints basic information about a DataFrame.

  Args:
    df: The DataFrame to inspect.
    message: An optional message to print before the DataFrame information.
  """

  if message:
    print(message)

  print("Shape:", df.shape)
  print("Columns:", df.columns)
  print("Data types:", df.dtypes)
  print("Missing values:\n", df.isnull().sum())
  print(df)


# Load the dataset
# Reads the CSV file into a Pandas DataFrame named airbnb_df.

df = pd.read_csv('AB_NYC_2019.csv')






# 5. Time Series Analysis of Reviews
# Plot: Create a line plot to show the trend of number_of_reviews over time
# (last_review) for each neighbourhood_group.
# Details: Use different colors for each neighborhood group, smooth the data with a
# rolling average, and add titles, axis labels, and a legend.

# Convert 'last_review' to a datetime format
df['last_review'] = pd.to_datetime(df['last_review'])

# Group the data by neighborhood group and month-end

grouped_data = df.groupby(['neighbourhood_group', pd.Grouper(key='last_review', freq='ME', label='right')]).agg(
    avg_reviews=('number_of_reviews', 'mean')
)

# Reset the index to have separate columns
grouped_data = grouped_data.reset_index()

# Check data type of avg_reviews
#print(grouped_data['avg_reviews'].dtype)  # Should be float64

#print_dataframe_info(grouped_data, "grouped_data:")

# Ensure index is sorted (if needed)
grouped_data.sort_values(by='last_review', inplace=True)

# Ensure dataframe grouped_data have 'last_review' as index
#grouped_data.set_index('last_review', inplace=True)

# Calculate rolling average
rolling_avg = grouped_data.groupby('neighbourhood_group')['avg_reviews'].rolling(window=6).mean().reset_index()



# Ensure dataframe rolling_avg have 'last_review' as index
#rolling_avg.set_index('last_review', inplace=True)


#print_dataframe_info(rolling_avg, "rolling_avg:")

# Align based on last_review index
grouped_data, rolling_avg = grouped_data.align(rolling_avg, axis=0)

# Add rolling average as a new column
grouped_data['rolling_avg'] = rolling_avg['avg_reviews']

print_dataframe_info(grouped_data, "grouped_data:")

# Create the line plot
sns.lineplot(x='last_review', y='avg_reviews', hue='neighbourhood_group', data=grouped_data)

# Set labels and title
plt.xlabel('Last Review Month')
plt.ylabel('Average Number of Reviews')
plt.title('Trend of Average Number of Reviews Over Time (By Neighborhood Group)')

# Show the plot
plt.show()


# Create the line plot with rolling_avg
sns.lineplot(x='last_review', y='rolling_avg', hue='neighbourhood_group', data=grouped_data)

# Set labels and title
plt.xlabel('Last Review Month')
plt.ylabel('Average Number of Reviews')
plt.title('Trend of Average Number of Reviews Over Time (By Neighborhood Group)')

# Show the plot
plt.show()