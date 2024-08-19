import pandas as pd
from bokeh.models import CategoricalAxis, ColumnDataSource, FactorRange, HoverTool, CategoricalColorMapper
from bokeh.palettes import Category20
from bokeh.plotting import figure, show

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
df = pd.read_csv('Titanic-Dataset.csv')


# Handle missing values
avgAge = int(df['Age'].mean())
df.loc[:, 'Age'] = df['Age'].fillna(avgAge)


# 3. Interactivity:
# o Add hover tools to display detailed information when hovering over any bar or point.
# o Implement filtering options to allow users to filter visualizations by class or gender

#print_dataframe_info(df, "Titanic df:")



# Calculate survival rates by class
class_counts = df.groupby('Pclass')['Survived'].agg(['sum', 'count'])
class_counts.columns = ['Survived', 'Total']
class_counts['Died'] = class_counts['Total'] - class_counts['Survived']
class_counts['SurvivalRate'] = class_counts['Survived'] / class_counts['Total']
class_mapping = {1: "1st Class", 2: "2nd Class", 3: "3rd Class"}
#class_counts['PclassText'] = class_counts['Pclass'].map(class_mapping)
#class_counts['PclassText'] = str(class_counts['Died'])

class_counts = class_counts.reset_index()
print("Calculate survival rates by class:")
print(class_counts)



survived_list = [item[0] for item in x]  # Extract survived counts
died_list = [item[1] for item in x]  # Extract died counts

# Combine class labels with counts into tuples
x = list(zip(class_counts['Pclass'], survived_list, died_list))

# Update ColumnDataSource with the new x data
source = ColumnDataSource(data=dict(x=x, Pclass=class_counts['Pclass']))



# Update ColumnDataSource with the x labels
source = ColumnDataSource(data=dict(x=x, Pclass=class_counts['Pclass']))


# Create a figure with a bar chart
fig1 = figure(
    x_range=FactorRange(*x),
    height=350,
    title="Survival Rates by Passenger Class",
    x_axis_label='Passenger Class',
    y_axis_label='Number of Passengers',
    toolbar_location=None, tools=""
)

# Add a bar chart for survivors
fig1.vbar(x='Pclass', top='Survived', width=0.5, color='green', source=source, legend_label='Survived')
# Add a bar chart for non-survivors
fig1.vbar(x='Pclass', top='Died', width=0.5, color='red', source=source, legend_label='Not Survived')



# Add a hover tool for more information
hover = HoverTool(
    tooltips=[
        ('Passenger Class', '@Pclass'),
        ('Survived', '@Survived'),
        ('Not Survived', '@Died')
    ]
)
fig1.add_tools(hover)

# Show the plot
show(fig1)



