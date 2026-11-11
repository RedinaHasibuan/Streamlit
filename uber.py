import streamlit as st
import pandas as pd
import numpy as np

# 1 SET TITLE --> RUN
st.title('Uber pickups in NYC')

# 2 SET CONST
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'

'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# 2.1 Create Func. for loading the data
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# 2.2 Get data --> RUN
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# 3 Show and Hide DataFrame --> RUN
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 4 Adding Histogram --> RUN
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#5.1 Map filters based on the hour filter
# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour ==
hour_to_filter]
#5.2 Show the map --> RUN
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)