# -*- coding: utf-8 -*-
# -----------------
# Ящики с усами по температуре и солености за каждый год
# https://habrahabr.ru/post/267123/
# http://r-analytics.blogspot.ru/2011/11/r_08.html#.VsqSDOYdaCc
# http://www.slideshare.net/DEVTYPE/ss-53792094
# ------------------
import pandas as pd
import matplotlib.pyplot as plt

def plotbox_year(data, station, name):
    data2013 = data[station].loc[data.Date <= '2013-12-31']
    data2014 = data[station].loc[(data.Date >= '2014-01-01') & (data.Date <= '2014-12-31')]
    data2015 = data[station].loc[(data.Date >= '2015-01-01') & (data.Date <= '2015-12-31')]
    condata = pd.concat([data2013.reset_index(drop=True), data2014.reset_index(drop=True),
                         data2015.reset_index(drop=True)], axis=1)
    condata.columns = ['2013', '2014', '2015']
    print station
    print condata.describe()
    condata.plot(kind='box')
    plt.savefig(name)
    plt.cla()
    plt.clf()
# main
allsal = pd.read_csv('salinity.txt', sep='\t', parse_dates=True)
alltemp = pd.read_csv('temperature.txt', sep='\t', parse_dates=True)
# salParis
print 'Salinity'
plotbox_year(allsal, 'Paris', 'salinity_Paris.pdf')
# salBalka
plotbox_year(allsal, 'Balka', 'salinity_Balka.pdf')
# salVodozabor
#plotbox_year(allsal, 'Vodozabor', 'salinity_Vodozabor.pdf')
salzabor = allsal['Vodozabor'].loc[(allsal.Date >= '2015-01-01') & (allsal.Date <= '2015-12-31')]
salzabor.plot(kind='box')
plt.savefig('salinity_Vodozabor.pdf')
plt.cla()
plt.clf()
print 'Vodozabor'
print salzabor.describe()
# tempParis
print 'Temperature'
plotbox_year(alltemp, 'Paris', 'temperature_Paris.pdf')
# tempBalka
plotbox_year(alltemp, 'Balka', 'temperature_Balka.pdf')
# temp Vodozabor
tempzabor14 = alltemp['Vodozabor'].loc[(alltemp.Date >= '2014-01-01') & (alltemp.Date <= '2014-12-31')]
tempzabor15 = alltemp['Vodozabor'].loc[(alltemp.Date >= '2015-01-01') & (alltemp.Date <= '2015-12-31')]
tempzabor = pd.concat([tempzabor14.reset_index(drop=True), tempzabor15.reset_index(drop=True)], axis=1)
tempzabor.columns = ['2014', '2015']
tempzabor.plot(kind='box')
plt.savefig('temperature_Vodozabor.pdf')
print 'Vodozabor'
print tempzabor.describe()