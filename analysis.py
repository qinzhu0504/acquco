#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from scipy.stats import zscore
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


# In[10]:


username = 'postgres'
password = 'Simple123'
engine = create_engine(f'postgresql://{username}:{password}@shippingdata.ctewbirxs5yo.us-east-2.rds.amazonaws.com:1234/postgres')


# In[11]:


shippingdata_df = pd.read_sql_table('shippingdata', engine, schema = 'shipping')


# In[ ]:





# In[12]:


# Remove outliers with Z score 
z_scores = zscore(shippingdata_df[['Cost_per_unit']])
abs_z_scores = np.abs(z_scores)
z_filter = (abs_z_scores < 3).all(axis = 1)
shippingdata_df_filtered = shippingdata_df[z_filter]


# In[13]:


def verify_holiday_week(date, holidays):
    holiday_period = []
    for holiday in holidays:
        holiday = {'start':holiday - timedelta(days=3), 'end':holiday + timedelta(days=3)}
        holiday_period.append(holiday)
    
    
    for holiday in holiday_period:
        if date >= holiday['start'] and date <= holiday['end']:
            return True
    return False


# In[15]:


cal = calendar()
holidays = cal.holidays(start=min(shippingdata_df_filtered['Ship_Date']), end=max(shippingdata_df_filtered['Ship_Date']))


# In[16]:


shippingdata_df_filtered['Holiday'] = shippingdata_df_filtered['Ship_Date'].apply(verify_holiday_week, args = [holidays])


# In[ ]:





# In[17]:


shippingdata_df_filtered['Month'] = shippingdata_df_filtered['Ship_Date'].apply(lambda x: int(x.strftime("%m")))


# In[18]:


shippingdata_df_filtered.boxplot('Quantity', figsize=(12, 8))


# In[19]:


# Remove quantity outliers with Z score 
z_scores = zscore(shippingdata_df_filtered[['Quantity']])
abs_z_scores = np.abs(z_scores)
z_filter = (abs_z_scores < 3).all(axis = 1)
shippingdata_df_filtered = shippingdata_df_filtered[z_filter]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[20]:


quantity_x = np.array(shippingdata_df_filtered['Quantity']/100).reshape((-1, 1))
month_x = np.array(shippingdata_df_filtered['Month']).reshape((-1, 1))
holiday_x = np.array(shippingdata_df_filtered['Holiday']).reshape((-1, 1))
y = np.array(shippingdata_df_filtered['Cost_per_unit'])


# In[21]:





# In[28]:


model = LinearRegression()
model.fit(quantity_x, y)
r_sq_quantity = model.score(quantity_x, y)
print('R-Square:', r_sq_quantity)
print('intercept:', model.intercept_)
print('slope:', model.coef_)


# In[29]:


model2 = LinearRegression()
model2.fit(month_x, y)
r_sq_month = model2.score(month_x, y)
print('R-Square:',r_sq_month)
print('intercept:', model2.intercept_)
print('slope:', model2.coef_)


# In[30]:


model3 = LinearRegression()
model3.fit(holiday_x, y)
r_sq_holiday = model3.score(holiday_x, y)
print('R-Square:',r_sq_holiday)
print('intercept:', model3.intercept_)
print('slope:', model3.coef_)


# In[ ]:




