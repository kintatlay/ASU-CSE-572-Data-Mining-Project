#!/usr/bin/env python
# coding: utf-8

# In[128]:


import numpy as np
import pandas as pd
import datetime
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# In[129]:


# Extract data from CSVs
cgmData_file_1 = pd.read_csv('CGMData.csv', sep=',', low_memory = False)
cgmData_file_2 = pd.read_csv('CGM_patient2.csv', sep=',', low_memory = False)
cgm = pd.concat([cgmData_file_1, cgmData_file_2],axis=0)
# cgm = pd.read_csv('CGMData.csv', sep=',', low_memory = False)
cgm['dateTime'] = pd.to_datetime(cgm['Date'] + ' ' + cgm['Time'])
cgm = cgm.sort_values(by='dateTime',ascending=True)
# display(cgm)

insulinData_file_1 = pd.read_csv('InsulinData.csv', sep=',', low_memory = False)
insulinData_file_2 = pd.read_csv('Insulin_patient2.csv', sep=',', low_memory = False)
insulin = pd.concat([insulinData_file_1, insulinData_file_2],axis=0)
# insulin = pd.read_csv('InsulinData.csv', sep=',', low_memory = False)
insulin['dateTime'] = pd.to_datetime(insulin['Date'] + ' ' + insulin['Time'])
insulin = insulin.sort_values(by='dateTime',ascending=True)
# display(insulin)


# In[130]:


# Extract data for meal time
# Compare the dateTime to identify how long have one eaten the previous meal
mealTimes = insulin.loc[insulin['BWZ Carb Input (grams)'] > 0][['Index', 'Date', 'Time', 'BWZ Carb Input (grams)', 'dateTime']]
mealTimes['diff'] = mealTimes['dateTime'].diff(periods=1)
mealTimes['shiftUp'] = mealTimes['diff'].shift(-1)
# display(mealTimes)


# In[131]:


# Using the previous meal time, filter out any meals eaten before the threshold (2 hours)
mealTimes = mealTimes.loc[(mealTimes['shiftUp'] > datetime.timedelta (minutes = 120)) | (pd.isnull(mealTimes['shiftUp']))]
# display(mealTimes)


# In[132]:


# Create a new dataframe. Using the meal time data from insulindata file and filter out the relevant time. Add those rows into the new dataframe
cgmdata_withMeal = pd.DataFrame()
for i in range(len(mealTimes)) : 
    preMealTime = mealTimes['dateTime'].iloc[i] - datetime.timedelta(minutes = 30)
    endMealTime = mealTimes['dateTime'].iloc[i] + datetime.timedelta(minutes = 120)
    filteredcgmdata = cgm.loc[(cgm['dateTime'] >= preMealTime) & (cgm['dateTime'] < endMealTime )]
#     display(filteredcgmdata)
    arr = []
    for j in range(len(filteredcgmdata)) :
        arr.append(filteredcgmdata['Sensor Glucose (mg/dL)'].iloc[j])
    cgmdata_withMeal = cgmdata_withMeal.append(pd.Series(arr), ignore_index=True)

# cgmdata_withMeal = cgmdata_withMeal.dropna()
cgmdata_withMeal


# In[133]:


# Apply interpolation for missing data
no_of_rows= cgmdata_withMeal.shape[0]
no_of_columns = cgmdata_withMeal.shape[1]
cgmdata_withMeal.dropna(axis=0, how='all', thresh=no_of_columns/4, subset=None, inplace=True)
cgmdata_withMeal.dropna(axis=1, how='all', thresh=no_of_rows/4, subset=None, inplace=True)
cgmdata_withMeal.interpolate(axis=0, method ='linear', limit_direction ='forward', inplace=True)
cgmdata_withMeal.bfill(axis=1,inplace=True)
cgmdata_withMeal['label'] = 1
# display(cgmdata_withMeal)


# In[134]:


# Get the no meal start time into an array
no_meal_time = []
for i in range(len(mealTimes)) : 
    startTime = mealTimes['dateTime'].iloc[i] + datetime.timedelta(minutes = 120)
    endTime = startTime + datetime.timedelta(minutes = 120)
    fullDataEndTime = insulin['dateTime'].iloc[-1]
    no_meal_continue = True
    while (no_meal_continue == True) :
        tempRange = insulin.loc[(insulin['dateTime'] >= startTime) & (insulin['dateTime'] < endTime) & (insulin['BWZ Carb Input (grams)'] > 0)]
        if (len(tempRange) > 0) :
            no_meal_continue = False
        else :
            no_meal_time.append(startTime)
        startTime = startTime + datetime.timedelta(minutes = 120)
        endTime = endTime + datetime.timedelta(minutes = 120)
        if (startTime > fullDataEndTime) :
            no_meal_continue = False
# display(no_meal_time)


# In[135]:


# Use the no meal start time and apply to the cgmdata file
cgmdata_noMeal = pd.DataFrame()
for i in no_meal_time:
    noMealStartTime = i
    noMealEndTime = i + datetime.timedelta(minutes = 120)
    filteredcgmdata = cgm.loc[(cgm['dateTime'] >= noMealStartTime) & (cgm['dateTime'] < noMealEndTime)]
    arr = []
    for j in range(len(filteredcgmdata)):
        arr.append(filteredcgmdata['Sensor Glucose (mg/dL)'].iloc[j])
    if (len(arr) > 24):
        continue
    cgmdata_noMeal = cgmdata_noMeal.append(pd.Series(arr), ignore_index=True)
    
# cgmdata_noMeal


# In[136]:


no_of_rows= cgmdata_noMeal.shape[0]
no_of_columns = cgmdata_noMeal.shape[1]
cgmdata_noMeal.dropna(axis=0, how='all', thresh=no_of_columns/4, subset=None, inplace=True)
cgmdata_noMeal.dropna(axis=1, how='all', thresh=no_of_rows/4, subset=None, inplace=True)
cgmdata_noMeal.interpolate(axis=0, method ='linear', limit_direction ='forward', inplace=True)
cgmdata_noMeal.bfill(axis=1,inplace=True)
cgmdata_noMeal['label'] = 0
# display(cgmdata_noMeal)


# In[137]:


totalResult = pd.concat([cgmdata_withMeal, cgmdata_noMeal], sort = False)
totalResult = totalResult.interpolate(axis = 0)
# display(totalResult)
condense_totalResult = totalResult[totalResult.columns[:24]]
# display(totalResult)
# display(condense_totalResult)


# In[138]:


# Divide data into train and test
x = np.asarray(condense_totalResult)
y = np.asarray(totalResult['label'])
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=1)
clf = MLPClassifier(random_state=1, max_iter=300).fit(x_train, y_train)


# In[139]:


filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))


# In[140]:


# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(x_test, y_test)
# print(result)


# In[141]:


# # Reference: https://towardsdatascience.com/a-quick-overview-of-5-scikit-learn-classification-algorithms-33fdc11ab0b9
# # Logistic regression - train the model and then predict() function to make predictions on the test set
# from sklearn.linear_model import LogisticRegression
# clf = LogisticRegression().fit(x_train, y_train)
# predictions_logistic = clf.predict(x_test)

# # Run classification report to compare predictions (we care about the accuracy f1-score)
# from sklearn.metrics import classification_report
# print(classification_report(y_test, predictions_logistic))


# In[142]:


# # KNN - try KNN and run classification report to compare prediction (we care about the accuracy f1-score)
# from sklearn.neighbors import KNeighborsClassifier
# neigh = KNeighborsClassifier()
# neigh.fit(x_train, y_train)
# predictions = neigh.predict(x_test)

# from sklearn.metrics import classification_report
# print(classification_report(y_test, predictions))


# In[143]:


# # Decision Tree - run classification report to compare prediction 
# from sklearn.tree import DecisionTreeClassifier
# clf = DecisionTreeClassifier(random_state=0)
# clf.fit(x_train, y_train)
# predictions = clf.predict(x_test)

# from sklearn.metrics import classification_report
# print(classification_report(y_test, predictions))


# In[144]:


# # Random Forrest - run classification report to compare prediction 
# from sklearn.ensemble import RandomForestClassifier
# clf = RandomForestClassifier(random_state=0)
# clf.fit(x_train, y_train)
# predictions = clf.predict(x_test)

# from sklearn.metrics import classification_report
# print(classification_report(y_test, predictions))


# In[145]:


# # Gradient boosting - run classification report to compare prediction 
# from sklearn.ensemble import GradientBoostingClassifier
# clf_win = GradientBoostingClassifier(random_state=0)
# clf_win.fit(x_train, y_train)
# predictions = clf_win.predict(x_test)

# from sklearn.metrics import classification_report
# print(classification_report(y_test, predictions))


# In[ ]:


# filename = 'finalized_model.sav'
# pickle.dump(clf_win, open(filename, 'wb'))

