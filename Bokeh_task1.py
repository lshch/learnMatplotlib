import pandas as pd
from bokeh.plotting import figure, show


# 1. Data Preparation:
# o Handle missing values in the Age, Cabin, and Embarked columns appropriately.
# o Create a new column AgeGroup to categorize passengers into age groups (e.g.,
# Child, Young Adult, Adult, Senior).
# o Create a SurvivalRate column to calculate the percentage of passengers who
# survived within each group.

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


# Load the Titanic dataset (replace 'titanic.csv' with the actual file path)
data = pd.read_csv('Titanic-Dataset.csv')

# Handle missing values
avgAge = int(data['Age'].mean())
data.loc[:, 'Age'] = data['Age'].fillna(avgAge)
data.loc[:, 'Cabin'] = data['Cabin'].fillna('Unknown')
data.loc[:, 'Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])

# Create the AgeGroup column
data['AgeGroup'] = pd.cut(data['Age'], bins=[0, 18, 30, 60, 100], labels=['Child', 'Young Adult', 'Adult', 'Senior'])

# Calculate the SurvivalRate column
grouped_data = (data['Survived'].groupby(data['AgeGroup'], observed=False).mean() * 100).round(2)

grouped_data = grouped_data.reset_index()
print(grouped_data)

data = pd.merge(data, grouped_data, on='AgeGroup', how='left')
data = data.rename(columns={'Survived_x': 'Survived'})
data = data.rename(columns={'Survived_y': 'SurvivalRate'})

# Create a figure for the bar chart
fig = figure(title='Survival Rates by Age Group', x_axis_label='Age Group', y_axis_label='Survival Rate (%)', width=800,
             height=400)

# Create the bar chart

print(data['AgeGroup'])
age_group_mapping = {'Child': 1, 'Young Adult': 2, 'Adult': 3, 'Senior': 4}
data['AgeGroup_num'] = data['AgeGroup'].map(age_group_mapping)
print(data['AgeGroup_num'])
fig.vbar(x=data['AgeGroup_num'], top=data['SurvivalRate'], width=0.8, color='skyblue')

print_dataframe_info(data, "Data:")
# Show the plot
show(fig)
