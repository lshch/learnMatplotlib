import pandas as pd
from bokeh.models import CategoricalAxis, ColumnDataSource, FactorRange
from bokeh.plotting import figure, show
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.transform import factor_cmap


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
print("Calculate the SurvivalRate column, grouped_data:")
print_dataframe_info(grouped_data)

# Calculate the SurvivalRate column by + sex
grouped_data_by_sex = (data['Survived'].groupby([data['AgeGroup'], data['Sex']], observed=False).mean() * 100).round(2)
grouped_data_by_sex = grouped_data_by_sex.reset_index(name='SurvivalRateBySex')
print("Calculate the SurvivalRate column by + sex")
print(grouped_data_by_sex)


data = pd.merge(data, grouped_data, on='AgeGroup', how='left')
data = pd.merge(data, grouped_data_by_sex, on='AgeGroup', how='left')
data = data.rename(columns={'Survived_x': 'Survived'})
data = data.rename(columns={'Survived_y': 'SurvivalRate'})
data = data.rename(columns={'Sex_x': 'Sex'})
del data['Sex_y']

print_dataframe_info(data, "Added new 3 columns:")

# 2. Visualization:
# o Age Group Survival: Create a bar chart showing survival rates across different age
# groups.
# o Class and Gender: Create a grouped bar chart to compare survival rates across
# different classes (1st, 2nd, 3rd) and genders (male, female).
# o Fare vs. Survival: Create a scatter plot with Fare on the x-axis and survival status
# on the y-axis, using different colors to represent different classes.


# Age Group Survival
fig1 = figure(x_range=['Child', 'Young Adult', 'Adult', 'Senior'],
              title='Fig1: Survival Rates by Age Group',
              x_axis_label='Age Group', y_axis_label='Survival Rate (%)',
              width=800, height=400,
              toolbar_location=None, tools="")

fig1.vbar(x=data['AgeGroup'], top=data['SurvivalRate'], width=0.8, color='skyblue')

# Add labels to the figures
fig1.xaxis.axis_label_text_font_size = '12pt'
fig1.yaxis.axis_label_text_font_size = '12pt'

# Show the plots
show(fig1)
#---

# Create the Bokeh plot
ageGroup = grouped_data_by_sex['AgeGroup'].unique()
sex_ = grouped_data_by_sex['Sex'].unique()

# Create the x-axis labels
x = [(age_group, sex) for age_group in ageGroup for sex in sex_]
print("Create the x-axis labels")
print(x)

# Create the data source
source = ColumnDataSource(data=dict(x=x, SurvivalRateBySex=grouped_data_by_sex['SurvivalRateBySex']))

print("Create the data source:")
print(source)

# Seaborn visualization
sns.barplot(x='AgeGroup', y='SurvivalRateBySex', hue='Sex', data=grouped_data_by_sex)
plt.title('Survived by Sex and AgeGroup')
plt.show()

# Create the figure
fig2 = figure(x_range=FactorRange(*x), height=350, title="Fig2: Survived by AgeGroup and Sex",
           toolbar_location=None, tools="")

# Add the vbar glyph
fig2.vbar(x='x', top='SurvivalRateBySex', width=0.9, source=source)

# Customize the plot
fig2.y_range.start = 0
fig2.x_range.range_padding = 0.1
fig2.xaxis.major_label_orientation = 1
fig2.xgrid.grid_line_color = None

# Show the plot
show(fig2)



#-----------

data['Class_str'] = 'Class -' + data['Pclass'].astype(str)
data['Survived_str'] = data['Survived'].map({0: 'no', 1: 'yes'})

# Create a ColumnDataSource
source = ColumnDataSource(data.sort_values(by='Pclass'))
print("Create a ColumnDataSource: ")
print(source.data.keys())
print(source.data['Fare'])
print(source.data['Survived'])
print(source.data['Pclass'])

# Create the figure
fig3 = figure(title="Fig3. Fare vs. Survival by Class", x_axis_label="Fare",  y_axis_label="Survived", y_range=FactorRange(factors=['0', '1']))

# Add the scatter plot
# Define a color mapper to map Survived values to colors
# Define unique factors (class values)
factors = data["Pclass"].astype(str).unique()  # Get unique values from "Survived"

# Define colors for each class (modify the palette as needed)
palette = ['navy', 'green', 'blue']

# Create the color mapper
mapper = factor_cmap("Pclass",
                     palette=palette,
                     factors=factors)

# Use the color mapper in the scatter plot
fig3.xaxis.axis_label = 'Fare'
fig3.yaxis.axis_label = 'Survived'
fig3.y_range = FactorRange(factors=['no', 'yes'])

# Use the color mapper in the scatter plot
fig3.scatter(x="Fare", y="Survived_str", size=10, source=source,
             legend_field="Class_str",
             fill_color=mapper, line_color=mapper)

# Show the plot
show(fig3)
