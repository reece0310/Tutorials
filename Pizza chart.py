#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np

from scipy import stats
import math

from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.pyplot as plt


# In[3]:


#import csv of premier league defensive stats from fbref. I have uploaded the data but I changed the column names in the csv prior.
df = pd.read_csv('pizza_tutorial.csv')

#when you first read in the csv from fbref, you'll notice the player names are kind of weird. This code splits them on the \
df['Player'] = df['Player'].str.split('\\',expand=True)[0]


# In[4]:


df.head(10)


# In[5]:


# only midfielders and only those with more than 12 90's played 
#(This data is from about week 35 so 12 90s will help us eliminate most outliers)
df = df.loc[(df['Pos']=='MF') & (df['90s']>15)]
#recheck the dataframe
df.head(10)


# In[6]:


# We now need to drop all of the columns that we don't want. 
# These are all the columns that won't be used included in the pizza plot
# These are just the ones I need to drop you may need to drop more or less depending on what you want to compare
df = df.drop(['Rk','Nation','Pos','Squad','Age','Born'],axis=1).reset_index()


# In[7]:


df.head()


# In[8]:


#Create a parameter list
params = list(df.columns)
params


# In[9]:


#drop the first 3 list item becuase we will not be using player,index, or 90s as a comparison metric
params = params[2:]
params


# In[10]:


# Now we filter the df for the player we want. We will look at ruben dias. 
# The player needs to be spelled exactly the same way as it is in the data. Accents and everything.
player = df.loc[df['Player']=='Thiago Alcántara'].reset_index()
player = list(player.loc[0])
print(player)


# In[11]:


df.Player.values


# In[12]:


# the length of our players in longer than the length of the params. we need to drop the first 3 player list items
print(len(player),print(len(params)))
player = player[3:]
print(len(player),print(len(params)))


# In[13]:


# now that we have the player scores, we need to calculate the percentile values with scipy stats.
# I am doing this because I do not know the percentile beforehand and only have the raw numbers
values = []
for x in range(len(params)):   
    values.append(math.floor(stats.percentileofscore(df[params[x]],player[x])))


# In[14]:


round(stats.percentileofscore(df[params[0]],player[0]))


# In[15]:


for n,i in enumerate(values):
    if i == 100:
        values[n] = 99


# In[16]:


baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
)


# In[19]:


# plot pizza
fig, ax = baker.make_pizza(
    values,              # list of values
    figsize=(8, 8),      # adjust figsize according to your need
    param_location=110,  # where the parameters will be added
    kwargs_slices=dict(
        facecolor="#E40019", edgecolor="#000000",
        zorder=2, linewidth=1
    ),                   # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=12,
        va="center", alpha=.5
    ),                   # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=12,
        zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="#FFFFFF",
            boxstyle="round,pad=0.2", lw=1
        )
    )                    # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.97, "Thiago Alcántara - Liverpool", size=18,
    ha="center", color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.942,
    "Per 90 Percentile Rank vs Premier League Midfielders | 2020-21",
    size=15,
    ha="center", color="#000000"
)

# add credits
notes = 'Players only with more than 15 90s'
CREDIT_1 = "data: statsbomb via fbref"
CREDIT_2 = "created by Reece Chambers"

fig.text(
    0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}", size=9,
    color="#000000",
    ha="right"
)

plt.savefig('pizza.png',dpi=500,bbox_inches = 'tight')


# In[ ]:




