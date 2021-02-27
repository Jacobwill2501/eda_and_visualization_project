import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# % matplotlib inline
import plotly.plotly as py
import plotly.offline as pyo
import plotly.graph_objs as go

# pyo.offline.init_notebook_mode()
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 12)

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
df = df.rename(columns={'Hipertenshion': 'Hypertension', "Handcap": "Handicap", "SMS_received": "SMSReceived"})

df['Presence'] = df['No-show'].apply(lambda x: 'Present' if x == "No" else "Absent")
df = df.drop('No-show', 1)

df['Waiting Time Days'] = df['AppointmentDay'] - df['ScheduledDay']
df['Waiting Time Days'] = df['Waiting Time Days'].dt.days

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
df['Month'] = df['AppointmentDay'].dt.month_name()
df['Hour'] = df['AppointmentDay'].dt.hour

print(df)
