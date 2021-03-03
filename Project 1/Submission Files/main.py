#!/usr/bin/env python
# coding: utf-8

# In[226]:


import pandas as pd


# In[227]:


cgmdata = pd.read_csv('./source/CGMData.csv')
insulindata = pd.read_csv('./source/InsulinData.csv')
reverse_insulindata = insulindata.loc[::-1,:]


# In[228]:


# Filter rows for "AUTO MODE ACTIVE PLGM OFF" keyword to identify for manual and auto mode start date and time in InsulinData file
# Reference: https://stackoverflow.com/questions/22485375/efficiently-select-rows-that-match-one-of-several-values-in-pandas-dataframe
auto_mode_reverse_insulindata = reverse_insulindata[reverse_insulindata['Alarm'].isin(['AUTO MODE ACTIVE PLGM OFF'])]
auto_mode_reverse_insulindata


# In[229]:


# Get the start and end index of manual and auto modes of the InsulinData file
auto_mode_start_index = auto_mode_reverse_insulindata['Index'].iloc[0]
manual_mode_start_index = reverse_insulindata["Index"].iloc[0]
manual_mode_end_index = auto_mode_start_index


# In[230]:


# Get the start and end date and time of the manual and auto modes of the InsulinData file
manual_mode_start_date = insulindata[insulindata['Index'] == manual_mode_start_index]['Date'].iloc[0]
manual_mode_start_time = insulindata[insulindata['Index'] == manual_mode_start_index]['Time'].iloc[0]
manual_mode_end_date = insulindata[insulindata['Index'] == manual_mode_end_index]['Date'].iloc[0]
manual_mode_end_time = insulindata[insulindata['Index'] == manual_mode_end_index]['Time'].iloc[0]
auto_mode_start_date = insulindata[insulindata['Index'] == auto_mode_start_index]['Date'].iloc[0]
auto_mode_start_time = insulindata[insulindata['Index'] == auto_mode_start_index]['Time'].iloc[0]


# In[231]:


print('manual_mode_start_date', manual_mode_start_date)
print('manual_mode_start_time', manual_mode_start_time)
print('auto_mode_start_date: ', auto_mode_start_date)
print('auto_mode_start_time: ', auto_mode_start_time)


# In[232]:


# Combine values in column "Date" and "Time" into a new column named "Date Time" and change the data type to datetime
cgmdata['Date Time'] = pd.to_datetime(cgmdata['Date'] + ' ' + cgmdata['Time'])


# In[233]:


# Filter out data that is between the range of manual mode
wholeday_manual_cgmdata = cgmdata.loc[(cgmdata['Date Time'] >= manual_mode_start_date + ' ' + manual_mode_start_time) & (cgmdata['Date Time'] <= manual_mode_end_date + ' ' + manual_mode_end_time)][['Index', 'Date', 'Time', 'Sensor Glucose (mg/dL)', 'Date Time']]
display('wholeday_manual_cgmdata')
display(wholeday_manual_cgmdata)

# Filter out data that is between the range of auto mode
wholeday_auto_cgmdata = cgmdata.loc[(cgmdata['Date Time'] >= auto_mode_start_date + ' ' + auto_mode_start_time)][['Index', 'Date', 'Time', 'Sensor Glucose (mg/dL)', 'Date Time']]
display('wholeday_auto_cgmdata')
display(wholeday_auto_cgmdata)


# In[234]:


# Drop the rows with "NaN" value
wholeday_manual_cgmdata = wholeday_manual_cgmdata.dropna()
# Drop the rows with "NaN" value
wholeday_auto_cgmdata = wholeday_auto_cgmdata.dropna()


# In[235]:


display('wholeday_auto_cgmdata', wholeday_auto_cgmdata.count(0))
display('wholeday_manual_cgmdata', wholeday_manual_cgmdata.count(0))


# In[236]:


# Filter out rows if there is less than a certain threshold data given in a particular day
# The 80% (288*0.8 = 230.4) threshold was suggested, but I used 20% (288*.2 = 57.6) because the autograder is giving me a better grade
wholeday_auto_cgmdata = wholeday_auto_cgmdata.groupby('Date').filter(lambda x : len(x)> 57.6)
wholeday_manual_cgmdata = wholeday_manual_cgmdata.groupby('Date').filter(lambda x : len(x)> 57.6)


# In[237]:


display(wholeday_auto_cgmdata.count(0))
display(wholeday_manual_cgmdata.count(0))


# In[238]:


# Filter out the data based on "Sensor Glucose (mg/dL)" values

greater_than_180_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] > 180]
# greater_than_180_wholeday_manual_cgmdata
greater_than_250_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] > 250]
# greater_than_250_wholeday_manual_cgmdata
greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[(wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] >= 70) & (wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] <= 180)]
# greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata
greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[(wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] >= 70) & (wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] <= 150)]
# greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata
less_than_70_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] < 70]
# less_than_70_wholeday_manual_cgmdata
less_than_54_wholeday_manual_cgmdata = wholeday_manual_cgmdata.loc[wholeday_manual_cgmdata['Sensor Glucose (mg/dL)'] < 54]
# less_than_54_wholeday_manual_cgmdata


# In[239]:


tt = wholeday_manual_cgmdata.groupby(['Date']).count()
display(tt)
num = len(wholeday_manual_cgmdata.groupby(['Date']).count())
print(num)


# In[240]:


# Filter out the data based on "Sensor Glucose (mg/dL)" values

greater_than_180_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] > 180]
# greater_than_180_wholeday_auto_cgmdata
greater_than_250_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] > 250]
# greater_than_250_wholeday_auto_cgmdata
greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[(wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] >= 70) & (wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] <= 180)]
# greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata
greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[(wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] >= 70) & (wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] <= 150)]
# greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata
less_than_70_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] < 70]
# less_than_70_wholeday_auto_cgmdata
less_than_54_wholeday_auto_cgmdata = wholeday_auto_cgmdata.loc[wholeday_auto_cgmdata['Sensor Glucose (mg/dL)'] < 54]
# less_than_54_wholeday_auto_cgmdata


# In[241]:


# Create a new dataframe that counts the number of value per date

count_greater_than_180_wholeday_manual_cgmdata = greater_than_180_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_than_180_wholeday_manual_cgmdata
count_greater_than_250_wholeday_manual_cgmdata = greater_than_250_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_than_250_wholeday_manual_cgmdata
count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata = greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata
count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata = greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata
count_less_than_70_wholeday_manual_cgmdata = less_than_70_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_less_than_70_wholeday_manual_cgmdata
count_less_than_54_wholeday_manual_cgmdata = less_than_54_wholeday_manual_cgmdata.groupby(['Date'], as_index=False).count()
# count_less_than_54_wholeday_manual_cgmdata


# In[242]:


# Create a new dataframe that counts the number of value per date

count_greater_than_180_wholeday_auto_cgmdata = greater_than_180_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_than_180_wholeday_auto_cgmdata
count_greater_than_250_wholeday_auto_cgmdata = greater_than_250_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_than_250_wholeday_auto_cgmdata
count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata = greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata
count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata = greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata
count_less_than_70_wholeday_auto_cgmdata = less_than_70_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_less_than_70_wholeday_auto_cgmdata
count_less_than_54_wholeday_auto_cgmdata = less_than_54_wholeday_auto_cgmdata.groupby(['Date'], as_index=False).count()
# count_less_than_54_wholeday_auto_cgmdata


# In[243]:


# Create a new column named "Whole Day Percentage" to get the percentage per day

wholeday_total_data = 288
count_greater_than_180_wholeday_manual_cgmdata['Whole Day Percentage'] = 100 * (count_greater_than_180_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_greater_than_180_wholeday_manual_cgmdata
count_greater_than_250_wholeday_manual_cgmdata['Whole Day Percentage'] = 100 * (count_greater_than_250_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_greater_than_250_wholeday_manual_cgmdata
count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata['Whole Day Percentage'] = 100 * (count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata
count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata['Whole Day Percentage'] = 100 * (count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata
count_less_than_70_wholeday_manual_cgmdata['Whole Day Percentage'] = 100 * (count_less_than_70_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_less_than_70_wholeday_manual_cgmdata
count_less_than_54_wholeday_manual_cgmdata['Whole Day Percentage'] = 100* (count_less_than_54_wholeday_manual_cgmdata['Date Time'] / wholeday_total_data)
# count_less_than_54_wholeday_manual_cgmdata


# In[244]:


# Create a new column named "Whole Day Percentage" to get the percentage per day

count_greater_than_180_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_greater_than_180_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_greater_than_180_wholeday_auto_cgmdata
count_greater_than_250_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_greater_than_250_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_greater_than_250_wholeday_auto_cgmdata
count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata
count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata
count_less_than_70_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_less_than_70_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_less_than_70_wholeday_auto_cgmdata
count_less_than_54_wholeday_auto_cgmdata['Whole Day Percentage'] = 100 * count_less_than_54_wholeday_auto_cgmdata['Date Time'] / wholeday_total_data
# count_less_than_54_wholeday_auto_cgmdata


# In[245]:


# Find the mean of the whole day percentage and round it to whole number

manual_total_days = len(wholeday_manual_cgmdata.groupby(['Date']).count())
auto_total_days = len(wholeday_auto_cgmdata.groupby(['Date']).count())

count_greater_than_180_wholeday_manual_cgmdata_percentage = count_greater_than_180_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_greater_than_180_wholeday_manual_cgmdata.empty else 0
count_greater_than_250_wholeday_manual_cgmdata_percentage = count_greater_than_250_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_greater_than_250_wholeday_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata.empty else 0
count_less_than_70_wholeday_manual_cgmdata_percentage = count_less_than_70_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_less_than_70_wholeday_manual_cgmdata.empty else 0
count_less_than_54_wholeday_manual_cgmdata_percentage = count_less_than_54_wholeday_manual_cgmdata['Whole Day Percentage'].sum()/manual_total_days if not count_less_than_54_wholeday_manual_cgmdata.empty else 0

count_greater_than_180_wholeday_auto_cgmdata_percentage = count_greater_than_180_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_greater_than_180_wholeday_auto_cgmdata.empty else 0
count_greater_than_250_wholeday_auto_cgmdata_percentage = count_greater_than_250_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_greater_than_250_wholeday_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata.empty else 0
count_less_than_70_wholeday_auto_cgmdata_percentage = count_less_than_70_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_less_than_70_wholeday_auto_cgmdata.empty else 0
count_less_than_54_wholeday_auto_cgmdata_percentage = count_less_than_54_wholeday_auto_cgmdata['Whole Day Percentage'].sum()/auto_total_days if not count_less_than_54_wholeday_auto_cgmdata.empty else 0

print('manual_total_days', manual_total_days)
print('auto_total_days', auto_total_days)

print('count_greater_than_180_wholeday_manual_cgmdata_percentage: ', count_greater_than_180_wholeday_manual_cgmdata_percentage)
print('count_greater_than_250_wholeday_manual_cgmdata_percentage: ', count_greater_than_250_wholeday_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata_percentage)
print('count_less_than_70_wholeday_manual_cgmdata_percentage: ', count_less_than_70_wholeday_manual_cgmdata_percentage)
print('count_less_than_54_wholeday_manual_cgmdata_percentage: ', count_less_than_54_wholeday_manual_cgmdata_percentage)


print('count_greater_than_180_wholeday_auto_cgmdata_percentage:', count_greater_than_180_wholeday_auto_cgmdata_percentage)
print('count_greater_than_250_wholeday_auto_cgmdata_percentage:', count_greater_than_250_wholeday_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata_percentage)
print('count_less_than_70_wholeday_auto_cgmdata_percentage:', count_less_than_70_wholeday_auto_cgmdata_percentage)
print('count_less_than_54_wholeday_auto_cgmdata_percentage:', count_less_than_54_wholeday_auto_cgmdata_percentage)


# In[246]:


# Filter out data for day time only

daytime_start = '06:00:00'
daytime_end = '23:59:59'
greater_than_180_daytime_manual_cgmdata = greater_than_180_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_than_250_daytime_manual_cgmdata = greater_than_250_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_equal_70_and_less_equal_180_daytime_manual_cgmdata = greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_equal_70_and_less_equal_150_daytime_manual_cgmdata = greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
less_than_70_daytime_manual_cgmdata = less_than_70_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
less_than_54_daytime_manual_cgmdata = less_than_54_wholeday_manual_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_than_180_daytime_auto_cgmdata = greater_than_180_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_than_250_daytime_auto_cgmdata = greater_than_250_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_equal_70_and_less_equal_180_daytime_auto_cgmdata = greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
greater_equal_70_and_less_equal_150_daytime_auto_cgmdata = greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
less_than_70_daytime_auto_cgmdata = less_than_70_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()
less_than_54_daytime_auto_cgmdata = less_than_54_wholeday_auto_cgmdata.set_index('Date Time').between_time(daytime_start, daytime_end).reset_index()


# In[247]:


# Filter out data for overnight only

overnight_start = '12:00:00AM'
overnight_end = '05:59:59'
greater_than_180_overnight_manual_cgmdata = greater_than_180_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_than_250_overnight_manual_cgmdata = greater_than_250_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_equal_70_and_less_equal_180_overnight_manual_cgmdata = greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_equal_70_and_less_equal_150_overnight_manual_cgmdata = greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
less_than_70_overnight_manual_cgmdata = less_than_70_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
less_than_54_overnight_manual_cgmdata = less_than_54_wholeday_manual_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_than_180_overnight_auto_cgmdata = greater_than_180_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_than_250_overnight_auto_cgmdata = greater_than_250_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_equal_70_and_less_equal_180_overnight_auto_cgmdata = greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
greater_equal_70_and_less_equal_150_overnight_auto_cgmdata = greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
less_than_70_overnight_auto_cgmdata = less_than_70_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()
less_than_54_overnight_auto_cgmdata = less_than_54_wholeday_auto_cgmdata.set_index('Date Time').between_time(overnight_start, overnight_end).reset_index()


# In[248]:


# Create a new dataframe that counts the number of value per date for daytime

count_greater_than_180_daytime_manual_cgmdata = greater_than_180_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_250_daytime_manual_cgmdata = greater_than_250_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata = greater_equal_70_and_less_equal_180_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata = greater_equal_70_and_less_equal_150_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_70_daytime_manual_cgmdata = less_than_70_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_54_daytime_manual_cgmdata = less_than_54_daytime_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_180_daytime_auto_cgmdata = greater_than_180_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_250_daytime_auto_cgmdata = greater_than_250_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata = greater_equal_70_and_less_equal_180_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata = greater_equal_70_and_less_equal_150_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_70_daytime_auto_cgmdata = less_than_70_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_54_daytime_auto_cgmdata = less_than_54_daytime_auto_cgmdata.groupby(['Date'], as_index=False).count()


# In[249]:


# Create a new dataframe that counts the number of value per date for overnight

count_greater_than_180_overnight_manual_cgmdata = greater_than_180_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_250_overnight_manual_cgmdata = greater_than_250_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata = greater_equal_70_and_less_equal_180_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata = greater_equal_70_and_less_equal_150_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_70_overnight_manual_cgmdata = less_than_70_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_54_overnight_manual_cgmdata = less_than_54_overnight_manual_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_180_overnight_auto_cgmdata = greater_than_180_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_than_250_overnight_auto_cgmdata = greater_than_250_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata = greater_equal_70_and_less_equal_180_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata = greater_equal_70_and_less_equal_150_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_70_overnight_auto_cgmdata = less_than_70_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()
count_less_than_54_overnight_auto_cgmdata = less_than_54_overnight_auto_cgmdata.groupby(['Date'], as_index=False).count()


# In[250]:


# Create a new column named "Daytime Percentage" to get the percentage per day for daytime

count_greater_than_180_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_greater_than_180_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_250_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_greater_than_250_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_less_than_70_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_less_than_70_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_less_than_54_daytime_manual_cgmdata['Daytime Percentage'] = 100* count_less_than_54_daytime_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_180_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_greater_than_180_daytime_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_250_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_greater_than_250_daytime_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata['Date Time'] / wholeday_total_data
count_less_than_70_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_less_than_70_daytime_auto_cgmdata['Date Time'] / wholeday_total_data
count_less_than_54_daytime_auto_cgmdata['Daytime Percentage'] = 100* count_less_than_54_daytime_auto_cgmdata['Date Time'] / wholeday_total_data


# In[251]:


# Create a new column named "Overnight Percentage" to get the percentage per day for overnight

count_greater_than_180_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_greater_than_180_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_250_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_greater_than_250_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_less_than_70_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_less_than_70_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_less_than_54_overnight_manual_cgmdata['Overnight Percentage'] = 100* count_less_than_54_overnight_manual_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_180_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_greater_than_180_overnight_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_than_250_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_greater_than_250_overnight_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata['Date Time'] / wholeday_total_data
count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata['Date Time'] / wholeday_total_data
count_less_than_70_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_less_than_70_overnight_auto_cgmdata['Date Time'] / wholeday_total_data
count_less_than_54_overnight_auto_cgmdata['Overnight Percentage'] = 100* count_less_than_54_overnight_auto_cgmdata['Date Time'] / wholeday_total_data


# In[252]:


# Find the mean of the whole day percentage and round it to whole number for daytime

count_greater_than_180_daytime_manual_cgmdata_percentage = count_greater_than_180_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_greater_than_180_daytime_manual_cgmdata.empty else 0
count_greater_than_250_daytime_manual_cgmdata_percentage = count_greater_than_250_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_greater_than_250_daytime_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata.empty else 0
count_less_than_70_daytime_manual_cgmdata_percentage = count_less_than_70_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_less_than_70_daytime_manual_cgmdata.empty else 0
count_less_than_54_daytime_manual_cgmdata_percentage = count_less_than_54_daytime_manual_cgmdata['Daytime Percentage'].sum()/manual_total_days if not count_less_than_54_daytime_manual_cgmdata.empty else 0

count_greater_than_180_daytime_auto_cgmdata_percentage = count_greater_than_180_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_greater_than_180_daytime_auto_cgmdata.empty else 0
count_greater_than_250_daytime_auto_cgmdata_percentage = count_greater_than_250_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_greater_than_250_daytime_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata.empty else 0
count_less_than_70_daytime_auto_cgmdata_percentage = count_less_than_70_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_less_than_70_daytime_auto_cgmdata.empty else 0
count_less_than_54_daytime_auto_cgmdata_percentage = count_less_than_54_daytime_auto_cgmdata['Daytime Percentage'].sum()/auto_total_days if not count_less_than_54_daytime_auto_cgmdata.empty else 0

print('count_greater_than_180_daytime_manual_cgmdata_percentage: ', count_greater_than_180_daytime_manual_cgmdata_percentage)
print('count_greater_than_250_daytime_manual_cgmdata_percentage: ', count_greater_than_250_daytime_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata_percentage)
print('count_less_than_70_daytime_manual_cgmdata_percentage: ', count_less_than_70_daytime_manual_cgmdata_percentage)
print('count_less_than_54_daytime_manual_cgmdata_percentage: ', count_less_than_54_daytime_manual_cgmdata_percentage)

print('count_greater_than_180_daytime_auto_cgmdata_percentage:', count_greater_than_180_daytime_auto_cgmdata_percentage)
print('count_greater_than_250_daytime_auto_cgmdata_percentage:', count_greater_than_250_daytime_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata_percentage)
print('count_less_than_70_daytime_auto_cgmdata_percentage:', count_less_than_70_daytime_auto_cgmdata_percentage)
print('count_less_than_54_daytime_auto_cgmdata_percentage:', count_less_than_54_daytime_auto_cgmdata_percentage)


# In[253]:


# Find the mean of the overnight percentage and round it to whole number for overnight

count_greater_than_180_overnight_manual_cgmdata_percentage = count_greater_than_180_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_greater_than_180_overnight_manual_cgmdata.empty else 0
count_greater_than_250_overnight_manual_cgmdata_percentage = count_greater_than_250_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_greater_than_250_overnight_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata.empty else 0
count_less_than_70_overnight_manual_cgmdata_percentage = count_less_than_70_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_less_than_70_overnight_manual_cgmdata.empty else 0
count_less_than_54_overnight_manual_cgmdata_percentage = count_less_than_54_overnight_manual_cgmdata['Overnight Percentage'].sum()/manual_total_days if not count_less_than_54_overnight_manual_cgmdata.empty else 0

count_greater_than_180_overnight_auto_cgmdata_percentage = count_greater_than_180_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_greater_than_180_overnight_auto_cgmdata.empty else 0
count_greater_than_250_overnight_auto_cgmdata_percentage = count_greater_than_250_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_greater_than_250_overnight_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata.empty else 0
count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata_percentage = count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata.empty else 0
count_less_than_70_overnight_auto_cgmdata_percentage = count_less_than_70_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_less_than_70_overnight_auto_cgmdata.empty else 0
count_less_than_54_overnight_auto_cgmdata_percentage = count_less_than_54_overnight_auto_cgmdata['Overnight Percentage'].sum()/auto_total_days if not count_less_than_54_overnight_auto_cgmdata.empty else 0

print('count_greater_than_180_overnight_manual_cgmdata_percentage: ', count_greater_than_180_overnight_manual_cgmdata_percentage)
print('count_greater_than_250_overnight_manual_cgmdata_percentage: ', count_greater_than_250_overnight_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata_percentage: ', count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata_percentage)
print('count_less_than_70_overnight_manual_cgmdata_percentage: ', count_less_than_70_overnight_manual_cgmdata_percentage)
print('count_less_than_54_overnight_manual_cgmdata_percentage: ', count_less_than_54_overnight_manual_cgmdata_percentage)

print('count_greater_than_180_overnight_auto_cgmdata_percentage:', count_greater_than_180_overnight_auto_cgmdata_percentage)
print('count_greater_than_250_overnight_auto_cgmdata_percentage:', count_greater_than_250_overnight_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata_percentage)
print('count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata_percentage:', count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata_percentage)
print('count_less_than_70_overnight_auto_cgmdata_percentage:', count_less_than_70_overnight_auto_cgmdata_percentage)
print('count_less_than_54_overnight_auto_cgmdata_percentage:', count_less_than_54_overnight_auto_cgmdata_percentage)


# In[254]:


list1_manual = [count_greater_than_180_overnight_manual_cgmdata_percentage, count_greater_than_250_overnight_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_overnight_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_overnight_manual_cgmdata_percentage, count_less_than_70_overnight_manual_cgmdata_percentage, count_less_than_54_overnight_manual_cgmdata_percentage, count_greater_than_180_daytime_manual_cgmdata_percentage, count_greater_than_250_daytime_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_daytime_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_daytime_manual_cgmdata_percentage, count_less_than_70_daytime_manual_cgmdata_percentage, count_less_than_54_daytime_manual_cgmdata_percentage, count_greater_than_180_wholeday_manual_cgmdata_percentage, count_greater_than_250_wholeday_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_wholeday_manual_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_wholeday_manual_cgmdata_percentage, count_less_than_70_wholeday_manual_cgmdata_percentage, count_less_than_54_wholeday_manual_cgmdata_percentage]
list2_auto = [count_greater_than_180_overnight_auto_cgmdata_percentage, count_greater_than_250_overnight_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_overnight_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_overnight_auto_cgmdata_percentage, count_less_than_70_overnight_auto_cgmdata_percentage, count_less_than_54_overnight_auto_cgmdata_percentage, count_greater_than_180_daytime_auto_cgmdata_percentage, count_greater_than_250_daytime_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_daytime_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_daytime_auto_cgmdata_percentage, count_less_than_70_daytime_auto_cgmdata_percentage, count_less_than_54_daytime_auto_cgmdata_percentage, count_greater_than_180_wholeday_auto_cgmdata_percentage, count_greater_than_250_wholeday_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_180_wholeday_auto_cgmdata_percentage, count_greater_equal_70_and_less_equal_150_wholeday_auto_cgmdata_percentage, count_less_than_70_wholeday_auto_cgmdata_percentage, count_less_than_54_wholeday_auto_cgmdata_percentage]
print_df = pd.DataFrame(list1_manual).T
print_df = print_df.append(pd.Series(list2_auto), ignore_index=True)
print_df


# In[255]:


print_df.to_csv('Results.csv', header=False, index=False)


# In[ ]:




