import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# pyo.offline.init_notebook_mode()
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 20)

# importing the csv
df = pd.read_csv('KaggleV2-May-2016.csv')

# Dropping two columns for simplification
df.drop(['PatientId', 'AppointmentID'], axis=1, inplace=True)

# Checking the number of rows and columns
print("Number of records (patients): ", df.shape[0])
print("Number of columns (features): ", df.shape[1])

# Cleaning ScheduledDay and AppointmentDay columns from object to datetime64[ns]
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay']).dt.date.astype('datetime64[ns]')
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay']).dt.date.astype('datetime64[ns]')

# Fixing name of columns
df = df.rename(columns={'Hipertension': 'Hypertension', "Handcap": "Handicap", "SMS_received": "SMSReceived"})

df['Presence'] = df['No-show'].apply(lambda x: 'Present' if x == "No" else "Absent")
df = df.drop('No-show', 1)

df['Waiting Time Days'] = df['AppointmentDay'] - df['ScheduledDay']
df['Waiting Time Days'] = df['Waiting Time Days'].dt.days

# Add a weekday feature to allow analysis of which day people miss the most
df['WeekDay'] = df['AppointmentDay'].apply(lambda x: x.weekday())
replace_map = {
    'WeekDay': {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday'
    }
}

df.replace(replace_map, inplace=True)

# Add features for month and hour
df['Month'] = df['AppointmentDay'].dt.month_name()
df['Hour'] = df['AppointmentDay'].dt.hour

print(df)

print("Unique values in 'Gender' column:", list(df.Gender.unique()))
print("Unique values in 'Scholarship' column:", list(df.Scholarship.unique()))
print("Unique values in 'Hypertension' column:", list(df.Hypertension.unique()))
print("Unique values in 'Diabetes' column:", list(df.Diabetes.unique()))
print("Unique values in 'Alcoholism' column:", list(df.Alcoholism.unique()))
print("Unique values in 'Handicap' column:", list(df.Handicap.unique()))
print("Unique values in 'SMSReceived' column:", list(df.SMSReceived.unique()))

print(df.describe())

labels = df['Gender'].value_counts().index
values = df['Gender'].value_counts().values
colors = ['#eba796', '#9bd9e6']

fig_male_vs_female = {'data': [{'type': 'pie',
                                'name': "Patients by Gender: Pie chart",
                                'labels': labels,
                                'values': values,
                                'direction': 'clockwise',
                                'marker': {'colors': colors}}], 'layout': {'title': 'Patients by Gender'}}

labels = df['Presence'].value_counts().index
values = df['Presence'].value_counts().values
colors = ['#93bf85', '#ed5765']

fig_present_vs_absent = {'data': [{'type': 'pie',
                                   'name': "Present vs Absent by Appointment Date: Pie chart",
                                   'labels': labels,
                                   'values': values,
                                   'direction': 'clockwise',
                                   'marker': {'colors': colors}}],
                         'layout': {'title': 'Present vs Absent by Appointment Date'}}

# pyo.plot(fig_present_vs_absent)
x0 = df.Age.values

trace0 = go.Box(
    x=x0,
    name='Age',
    marker=dict(
        color='rgb(0,128,128)',
    )
)

data = [trace0]

# pyo.plot(data)

# Create variable with true if a patient is present
present = df['Presence'] == "Present"

# Select all cases where a patient is present
df_present_patients = df[present]
absent = df['Presence'] == "Absent"

# Select all cases where a patient is present
df_absent_patients = df[absent]

x1 = df_present_patients.Age.values

x2 = df_absent_patients.Age.values

trace1 = go.Box(
    x=x1,
    name='Present',
    marker=dict(
        color='#3D9970',
    )
)

trace2 = go.Box(
    x=x2,
    name='Absent',
    marker=dict(
        color='#FF4136',
    )
)

data = [trace1, trace2]

# layout = go.Layout(
#     boxmode='group'
# )
# fig = go.Figure(data=data, layout=layout)
# pyo.plot(fig)

# Analyzing the age ranges of males and females
female = df['Gender'] == 'F'
male = df['Gender'] == 'M'

# Select all cases where a patient is present
df_female_patients = df[female]
df_male_patients = df[male]

x3 = df_female_patients.Age.values
x4 = df_male_patients.Age.values

trace3 = go.Box(
    x=x3,
    name='Females',
    marker=dict(
        color='#3D9970',
    )
)

trace4 = go.Box(
    x=x4,
    name='Males',
    marker=dict(
        color='#FF4136',
    )
)

data = [trace3, trace4]

layout = go.Layout(
    boxmode='group'
)
# fig = go.Figure(data=data, layout=layout)
# pyo.plot(fig)

# Present vs Absent by Gender - BAR

trace5 = go.Bar(
    x=df_present_patients['Gender'].value_counts().index,
    y=df_present_patients['Gender'].value_counts().values,
    name='Present'
)

trace6 = go.Bar(
    x=df_absent_patients['Gender'].value_counts().index,
    y=df_absent_patients['Gender'].value_counts().values,
    name='Absent'
)

data = [trace5, trace6]
layout = go.Layout(
    barmode='group'
)

# fig = go.Figure(data=data, layout=layout)
# pyo.plot(fig, filename='grouped-bar')

# Days of the week people do not show up - BAR

trace7 = go.Bar(
    x=df_absent_patients['WeekDay'].value_counts().index,
    y=df_absent_patients['WeekDay'].value_counts().values,
    name='Absent    '
)

data = [trace7]
layout = go.Layout(
    barmode='group'
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='grouped-bar')
