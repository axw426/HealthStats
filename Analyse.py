import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np

file="NCHS_-_Leading_Causes_of_Death__United_States.csv" 
#sourced from https://catalog.data.gov/dataset/age-adjusted-death-rates-for-the-top-10-leading-causes-of-death-united-states-2013
rawdata=pd.read_csv(file,sep=",",header=0)
f=rawdata.loc[(rawdata['Cause Name']!='All causes')]

causes=f['Cause Name'].unique()
years=f['Year'].unique()
states=f['State'].unique()
deaths=f['Deaths'].unique()
print(causes)

#start by learning how to plot 
x='Cause Name'
y='Deaths'
state='Maryland'

mpl_fig=plt.figure() #equivalent of root canvas

#plot current death rates
ax=mpl_fig.add_subplot(111) #122 = 1 rows, 2 cols, 1st position out of these regions

#get data for specific state for most recent year
alabamastrokes=f.loc[(f['State']==state) & (f['Year']==f['Year'].max())]
N=np.arange(alabamastrokes.shape[0])
ax.bar(N,alabamastrokes[y])
ax.set_xlabel(x)
ax.set_xticks(N)
ax.set_xticklabels(alabamastrokes[x],rotation='vertical')
ax.set_ylabel(y)
ax.set_title("Deaths in "+state)
plt.tight_layout()#makes everything neat (fixes margins etc)
plt.show()

#plot evolution of death rates over the decades
mpl_fig2=plt.figure() 
ax2=mpl_fig2.add_subplot(111)

color=iter(cm.rainbow(np.linspace(0,1,causes.shape[0])))
for cause in causes:
	c=next(color)
	temp=f.loc[(f['State']==state) & (f['Cause Name']==cause)]
	ax2.plot( temp['Year'], temp['Deaths'],color=c, label=cause, linestyle='',marker='o',markersize=2)

ax2.legend(loc='best')
ax2.set_title("History of death rates "+state)

plt.tight_layout()#makes everything neat (fixes margins etc)
plt.show()


#average death rates across states for specific year?
stateaverages=pd.DataFrame(columns=['state',"deathrate"])
for state in states:
	sumdeathrate=f.loc[(f['State']==state) & (f['Year']==f['Year'].max())]["Age-adjusted Death Rate"].mean()
	stateaverages=stateaverages.append({'state':state,'deathrate':sumdeathrate},ignore_index=True)
stateaverages=stateaverages.sort_values(by=['deathrate'])
stateaverages=stateaverages.reset_index(drop=True)
#print(stateaverages)

mpl_fig3=plt.figure() 
ax3=mpl_fig3.add_subplot(111)

N=np.arange(stateaverages.shape[0])
ax3.bar(N,stateaverages['deathrate'])
ax3.bar(stateaverages.index[stateaverages['state']=="United States"],stateaverages.loc[stateaverages['state']=="United States"]['deathrate'],color='r')
#	ax3.set_xlabel("State")
ax3.set_ylabel("Death Rate / 100,000 of population")
ax3.set_xticks(N)
ax3.set_xticklabels(stateaverages['state'],rotation='vertical')
plt.tight_layout()#makes everything neat (fixes margins etc)
plt.show()




