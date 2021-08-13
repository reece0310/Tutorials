#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np

import highlight_text


# In[2]:


# the famous import font code to use Andale Mono
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])


# In[3]:


#import data
df = pd.read_csv('beeswarmTutorial.csv')


# In[4]:


df2 = pd.read_csv('InStat Pos.csv')


# In[5]:


#set default colors
text_color = 'white'
background = '#000000'


# In[6]:


#look at top of dataframe
df.head()


# In[7]:


#create a new column for progressive passes per 90
df['per90'] = df['Prog']/df['90s']
df


# In[8]:


#filter the dataframe so it is only players who have played more than 6.5 90's which is about 585 minutes
df = df[df['90s']>=6.5].reset_index()
df


# In[9]:


df.describe()


# In[10]:


df = df.sort_values(by='per90',ascending=False)


# In[11]:


df = df[df['Pos'] != 'GK']


# In[12]:


df.head(10)


# In[13]:


fig, ax = plt.subplots(figsize=(10,5))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
spines = ['top','bottom','left','right']
for x in spines:
    if x in spines:
        ax.spines[x].set_visible(False)

sns.swarmplot(x='per90',data=df,color='white',zorder=1)

#plot thiago
plt.scatter(x=9.87,y=0,c='red',edgecolor='white',s=200,zorder=2)
plt.text(s='Thiago',x=9.87,y=-.04,c=text_color)

#plot de bruyne
plt.scatter(x=7.564,y=0,c='blue',edgecolor='white',s=200,zorder=2)

plt.title('Progressive Passes in the Premier League 2020/21',c=text_color,fontsize=14)

plt.xlabel('Progressive Passes per 90',c=text_color)



#plt.savefig('swarm.png',dpi=500,bbox_inches = 'tight',facecolor=background)


# In[14]:


#import our next dataframe
df2 = pd.read_csv('beeswarm2.csv')


# In[15]:


df2.head(10)


# In[16]:


#do some data preprocessing and cleaning

#split the player names
df2['Player'] = df2['Player'].str.split('\\',expand=True)[0]

df2 = df2[df2['Pos'] != 'GK']

df2 = df2[df2['90s'] > 6.5].reset_index()


# In[17]:


#make the per 90 stats
#metrics = ['Prog90','1/390','xA90','Cmp%','KP90','PPA90']
df2['Progressive Passes per 90'] = df2['Prog'] / df2['90s']
df2['Final third passes per 90'] = df2['1/3'] / df2['90s']
df2['Expected Assists per 90'] = df2['xA'] / df2['90s']
df2['Key Passes per 90'] = df2['KP'] / df2['90s']
df2['Passes into the penalty area per 90'] = df2['PPA'] / df2['90s']


# In[18]:


print(df2.head())

df2.Player.unique()


# In[27]:


#create a list of 6 metrics to compare
metrics = ['Progressive Passes per 90','Final third passes per 90','Expected Assists per 90','Cmp%','Key Passes per 90','Passes into the penalty area per 90']


# In[28]:


fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(df2['Player'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=df2,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
#Add the first player    

    for x in range(len(df2['Player'])):
        #if df2['Player'][x] == 'Thiago Alcántara':
            #ax.scatter(x=df2[metrics[met_counter]][x],y=0,s=200,c='red',zorder=2)
        if df2['Player'][x] == 'Ben Chilwell':
            ax.scatter(x=df2[metrics[met_counter]][x],y=0,s=200,c='blue',zorder=2)

#Add the second player

    for x in range(len(df2['Player'])):
        #if df2['Player'][x] == 'Thiago Alcántara':
            #ax.scatter(x=df2[metrics[met_counter]][x],y=0,s=200,c='red',zorder=2)
        if df2['Player'][x] == 'Luke Shaw':
            ax.scatter(x=df2[metrics[met_counter]][x],y=0,s=200,c='#FF0000',zorder=2)
                        
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
        
# add title
fig.text(
    0.4, 0.93, "Ben Chilwell", size=25,
    ha="center", color="blue"
)

fig.text(
    0.50, 0.93, " vs", size=25,
    ha="center", color="#FFFFFF"
)

fig.text(
    0.6, 0.93, "Luke Shaw", size=25,
    ha="center", color="#FF0000"
)


# add subtitle
fig.text(
    0.499, 0.9,
    "Per 90 Passing stats | Includes all outfield players with more than 6.5 90s played | Premier League 2020/21",
    size=10,
    ha="center", color="#FFFFFF"
) 

fig.text(.12,.03,"Created by Reece Chambers | Data via FBRef + Statsbomb", fontstyle='normal',fontsize=11, fontfamily='Arial',color=text_color)

plt.savefig('Chilwell vs Shaw.png',dpi=500,bbox_inches = 'tight',facecolor=background)


# In[ ]:




