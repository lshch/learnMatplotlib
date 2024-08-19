import pandas as pd
from bokeh.models import CategoricalAxis, ColumnDataSource, FactorRange, HoverTool
from bokeh.plotting import figure, show
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.transform import factor_cmap
import plotly.express as px


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

# Create the AgeGroup column
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 18, 30, 60, 100], labels=['Child', 'Young Adult', 'Adult', 'Senior'])
print_dataframe_info(df, "Create the AgeGroup column:")


# Calculate the SurvivalRate column
grouped_data = (df['Survived'].groupby(df['AgeGroup'], observed=False).mean() * 100).round(2)
grouped_data = grouped_data.reset_index(name="SurvivalRateByAge")
print_dataframe_info(grouped_data, "Calculate the SurvivalRate column, df grouped_data, new column SurvivalRateByAge:")


#df = pd.merge(df, grouped_data, on='AgeGroup', how='left')




# 3. Interactivity:
# o Add hover tools to display detailed information when hovering over any bar or point.
# o Implement filtering options to allow users to filter visualizations by class or gender

# Prepare the data
source = ColumnDataSource(df)

# Calculate survival rates by gender
gender_survival_rates = df.groupby("Sex")["Survived"].mean()
gender_survival_rates = gender_survival_rates.reset_index(name='SurvivalRateBySex')
print("Calculate survival rates by gender:")
print(gender_survival_rates)

# Calculate survival rates by age
age_survival_rates = df.groupby("AgeGroup")["Survived"].mean()
age_survival_rates = age_survival_rates.reset_index(name='SurvivalRateByAge')
print("Calculate survival rates by age:")
print(age_survival_rates)

# Calculate survival rates by class
class_survival_rates = df.groupby("Pclass")["Survived"].mean()
class_survival_rates = class_survival_rates.reset_index(name='SurvivalRateByClass')
print("Calculate survival rates by class:")
print(class_survival_rates)


# Create the Bokeh plot
sex_ = gender_survival_rates['Sex'].unique()

# Create the x-axis labels
x = [sex for sex in sex_]

# Create the data source
source1 = ColumnDataSource(data=dict(x=x, SurvivalRateBySex=gender_survival_rates['SurvivalRateBySex']))


# Create a bar chart for survival rates by gender
fig1 = figure(title="Survival Rates by Gender",
              x_axis_label="Gender", y_axis_label="Survival Rate"
            )
#fig1.vbar(x=df['Sex'], top=df['SurvivalRate'], width=0.5, color='skyblue')
fig1.vbar(x="Sex", bottom=gender_survival_rates['SurvivalRateBySex'], width=0.5, source=source1)
fig1.yaxis.axis_label_text_font_size = "14px"  # Adjust y-axis label font size

fig1.add_tools(HoverTool(tooltips=[("Gender", "@Sex"),
                                   ("Survival Rate", "@Survived")]))

# Show the visualizations
show(fig1)

# Create a scatter plot for survival rates by age
fig2 = figure(title="Survival Rates by Age", x_axis_label="Age", y_axis_label="Survival Rate")
fig2.circle(x="Age", y="Survived", source=source)
fig2.add_tools(HoverTool(tooltips=[("Age", "@Age"), ("Survival Rate", "@Survived")]))

# Create a stacked bar chart for survival rates by class
fig3 = figure(title="Survival Rates by Class", x_axis_label="Class", y_axis_label="Survival Rate")
fig3.vbar_stack(x="Pclass", stackers=["Survived", "Not Survived"], source=source)
fig3.add_tools(HoverTool(tooltips=[("Class", "@Pclass"), ("Survived", "@Survived"), ("Not Survived", "@{Not Survived}")]))

# Implement filtering options
gender_filter = Select(title="Gender", value="all", options=["all", "male", "female"])
class_filter = Select(title="Class", value="all", options=["all", 1, 2, 3])

def update(attr, old, new):
    if gender_filter.value == "all":
        gender_mask = True
    else:
        gender_mask = df["Sex"] == gender_filter.value
    if class_filter.value == "all":
        class_mask = True
    else:
        class_mask = df["Pclass"] == class_filter.value
    mask = gender_mask & class_mask
    source.data = df[mask]

gender_filter.on_change("value", update)
class_filter.on_change("value", update)

# Show the visualizations
#show(fig1)
show(fig2)
show(fig3)
