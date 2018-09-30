
# coding: utf-8

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import openweathermapy.core as owm
# Import API key
import api_keys
# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# In[2]:


#!pip install citipy


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ## Perform API Calls

# In[3]:


# OpenWeatherMap API Key
api_key=api_keys.api_key
lat = []
lon=[]
Country=[]
Date=[]
Humidity=[]
MaxTemp=[]
Windspeed=[]
Cloudiness=[]
valid_city=[]

# Starting URL for Weather Map API Call
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key 
city_url = url + '&units=imperial' + '&q='
for city in cities:
    query_url = city_url + city
    response = requests.get(query_url).json()
    try:
        lat.append(response["coord"]["lat"])
        lon.append(response["coord"]["lon"])
        Country.append(response["sys"]["country"])
        Date.append(response["dt"])
        Humidity.append(response["main"]["humidity"])
        Windspeed.append(response["wind"]["speed"])
        MaxTemp.append(response["main"]["temp_max"])
        Cloudiness.append(response["clouds"]["all"])
        if response["coord"]["lat"]!= None:
            valid_city.append(city)
    except KeyError:
        print("Missing field/result... skipping.")
        continue


# In[4]:


print(response)


# ## Making Data fram of cities Weather and save it as csv file:

# In[5]:


weather_dict = {
    "city": valid_city,
    "lat": lat,
    "Lng": lon,
    "Max Temp": MaxTemp,
    "Date": Date,
    "Country": Country,
    "Wind speed": Windspeed,
    "Humidity": Humidity,
    "Cloudiness": Cloudiness
}

city_pd=pd.DataFrame.from_dict(weather_dict)
city_pd.to_csv("cities.csv")
city_pd.head()


# ### Is null value in city
# 

# In[6]:


city_pd.isnull().any()


# # Plotting Result

# ## 1:  latitude vs Temperature 

# In[7]:


get_ipython().run_line_magic('matplotlib', 'notebook')
fig = plt.figure()
latitude = city_pd['lat'].values
Temperature  = city_pd['Max Temp'].values

Temperature = plt.scatter(latitude,Temperature , marker="o", facecolors="red", edgecolors="black",
           alpha=0.75, label="Temperature")
from datetime import datetime
curentDate= city_pd["Date"][0]
date=datetime.utcfromtimestamp(curentDate).strftime('%Y-%m-%d')
plt.title(f"City latitude vs Temperature({date})")
plt.xlabel("latitude")
plt.ylabel(" Max Temperature(F)")
plt.grid()
plt.show()


# In[8]:


fig.savefig('City latitude vs Temperature.png')


# In[12]:


#finding the changing point between posetive and negative correlation. 
#find maximun temperature 
maxtem=max(city_pd['Max Temp'].tolist())
#filter dataframe to finde latitude for max Temp
filter=city_pd.loc[city_pd["Max Temp"]==maxtem,:]
#find max and min for lat
min_lat=min(lat)
max_lat=max(lat)
#take value for changing point latitude
change_point=filter["lat"].values[0]
# seprate city_df in two data frame before change point in latitude and after that .
posetive=city_pd.loc[city_pd['lat']<=change_point,:]
negative=city_pd.loc[city_pd['lat']>change_point,:]


# ### calculate Correclation between latitude vs Temperature and Result:

# In[13]:


pc=np.corrcoef(posetive['lat'],posetive['Max Temp'])[0][1]
nc=np.corrcoef(negative['lat'],negative['Max Temp'])[0][1]


# In[21]:


print("According to City latitude vs Temperature Analysis:")
print("----------------------------------------------")
print(f"There is polynomial correlation betweeen city latitude vs Temperature ")
print(f"There is a strong correlation between city latitude in range ({min_lat}: {change_point}) and  max Temperature for city")
print(f"strong correlation between  City latitude vs Temperature is {pc}." )
print(f"There is a strnog correlation between city latitude in range ({change_point}: {max_lat}) and  max Temperature for city")
print(f"strong negative correlation between  City latitude vs Temperature is {nc}." )
#print(f"There is a Negative correlation between city latitude in range ({filter['lat'].values[0]}: {max_lat}) and  max Temperature for city")


# ## 2: City latitude vs Cloudiness 

# In[15]:


fig = plt.figure()
latitude = city_pd['lat'].values
Cloudiness= city_pd['Cloudiness'].values

Temperature = plt.scatter(latitude,Cloudiness , marker="o", facecolors="blue", edgecolors="black",
            alpha=0.75, label="Cloudiness")
from datetime import datetime
curentDate= city_pd["Date"][0]
date=datetime.utcfromtimestamp(curentDate).strftime('%Y-%m-%d')

plt.title(f"City latitude vs Cloudiness ({date})")
plt.xlabel("latitude")
plt.ylabel(" Cloudiness %")
plt.grid()
plt.show()


# In[72]:


fig.savefig('City latitude vs Cloudiness .png')


# ### Calculate Correlation between latitude vs Cloudiness and Result:

# In[16]:


cf= np.corrcoef(city_pd['lat'],city_pd['Cloudiness'])[0][1]


# In[17]:


print("According to City latitude vs Cloudiness Analysis:")
print("----------------------------------------------")
print(f"There is no  specifice correlation between city's latitude and Cloudniess")
print(f"The correlation between City latitude vs Cloudiness is {cf}, and this is very low ")


# ## 2: City latitude vs Wind speed

# In[18]:


fig = plt.figure()
latitude = city_pd['lat'].values
Windspeed= city_pd['Wind speed'].values

Temperature = plt.scatter(latitude,Windspeed , marker="o", facecolors="blue", edgecolors="black",
           alpha=0.75, label="Wind speed")
from datetime import datetime
curentDate= city_pd["Date"][0]
date=datetime.utcfromtimestamp(curentDate).strftime('%Y-%m-%d')
plt.title(f"City latitude vs Wind speed ({date})")
plt.xlabel("latitude")
plt.ylabel("Wind speed(mph)")
plt.grid()
plt.show()


# In[167]:


fig.savefig('City latitude vs Wind speed .png')


# ### Calculate Correlation between latitude vs wind speed and Result:

# In[19]:


wc=np.corrcoef(city_pd['lat'],city_pd['Wind speed'])[0][1]


# In[20]:


print("According to City latitude vs Cloudiness Analysis:")
print("----------------------------------------------")
print(f"The correlation between city latitude vs wind speed is {wc} and this is not strong.")
print("The avarage wind speed for most of cityis is in range 0 to 20")

