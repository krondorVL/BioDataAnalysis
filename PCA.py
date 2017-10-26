# -*- coding: utf-8 -*-
# -----------------------------------
# формируем праймер-стайл таблицу с избранными видами и параметрами среды
# -----------------------------------
import pandas as pd
import numpy as np

def find_dominant(indata):
    '''
    Ищем домимантные виды (больше 50% от общей численности)\
    На входе - срез по периоду и горизонту (общевидовой состав видов)\
    На выходе - список по датам,видам и количество в виде датафрейма панды
    '''
    dates = indata.groupby('Date').first().index.tolist()
    allSpecies = indata.groupby(['Date', 'Species'])['N'].first()
    meanData = pd.DataFrame()
    for date in dates:
        dayData = allSpecies.loc[idx[date, :]].reset_index(0)['N']
        summa = dayData.sum()
        dayPercentData = pd.DataFrame(dayData/summa*100)
        domSpecies = dayPercentData[dayPercentData.N>20]
        meanData = pd.concat([meanData,domSpecies.mean()]).fillna(0)
        print date
        print domSpecies


pd.options.display.max_rows = 9999
idx = pd.IndexSlice

#Prorocentrum triestinum
# prepare data
data = pd.read_csv('base.csv', sep=';', parse_dates=True)
himia = pd.read_csv('hydrochemistry.csv', sep=',', parse_dates=True)

speciesList = ['Prorocentrum triestinum','Small flagellata','Chaetoceros decipiens','Rhizosolenia setigera',
               'Thalassionema nitzschioides','Thalassionema frauenfeldii','Cryptomonas sp.','Thalassiosira sp. (d=32)',
               'Chattonella sp.','Pseudo–nitzschia delicatissima','Skeletonema sp.','Chrysochromulina sp.',
               'Thalassiosira nordenskioeldii']

species2013 = ['Chaetoceros debilis','Thalassiosira nordenskioeldii','Chaetoceros didymus','Licmophora abbreviata',
               'Chrysochromulina sp.','Navicula directa','Gyrodinium spirale','Eutreptia lanowii','Eutreptia sp.',
               'Grammatophora marina','Dinophysis acuminata','Chaetoceros sp.','Dinophysis acuminata',
               'Prorocentrum micans','Skeletonema dohrnii','Protoperidinium pellucidum',
               'Pseudo-nitzschia delicatissima','Pseudo-nitzschia pungens','Cerataulina dentata',
               'Skeletonema japonicum','Thalassionema frauenfeldii']

species2014 = ['Chattonella sp.','Pseudo-nitzschia pungens','Skeletonema japonicum',
               'Thalassionema frauenfeldii','Thalassiosira nordenskioeldii',
               'Thalassiosira sp. (d=32)','Cryptomonas sp.','Eutreptia lanowii',
               'Oxytoxum sceptrum','Skeletonema dohrnii',
               'Thalassionema frauenfeldii','Small flagellata','Prorocentrum minimum',
               'Prorocentrum triestinum','Protoperidinium bipes',
               'Chaetoceros didymus','Thalassionema nitzschioides','Rhizosolenia setigera']

species2015 = ['Gyrodinium spirale','Protoperidinium pellucidum','Chaetoceros simplex',
               'Pseudo-nitzschia delicatissima','Thalassiosira sp. (d=32)','Thalassiosira sp. (d = 17)',
               'Eutreptia lanowii','Licmophora abbreviata','Navicula vanhoeffenii',
               'Chaetoceros decipiens','Small flagellata','Skeletonema dohrnii',
               'Thalassionema frauenfeldii','Chaetoceros decipiens','Prorocentrum triestinum',
               'Skeletonema japonicum','Thalassionema nitzschioides']
# data
Sdate = '2014-12-01'
Ldate = '2015-11-31'
Sadok =  data[(data.Station=='Парис_садок') & (data.Date >= Sdate) & (data.Date <= Ldate) & (data.Horizon == 0)].groupby(['Date','Species'])['N'].first()
# finding dates list
datesList = []
for taxa in species2014:
    try:
        datesList.extend(Sadok[:,taxa].index.tolist())
    except:
        print 'error', taxa
datesList = np.unique(datesList).tolist()

# forming bio data
bioData = pd.DataFrame( np.zeros((np.size(datesList),len(species2014))) )
bioData.index = datesList
bioData.columns = species2014
for date in datesList:
    for taxa in species2014:
        #bioData[taxa].loc[date] = np.random.rand()
        try:
            bioData.loc[date][taxa] = np.log(1.0 + Sadok[date,taxa])
        except:
            bioData.loc[date][taxa] = 0.0

#bioData.astype(float).to_csv('cca_bio_n_log_2014.csv', sep=';', encoding='utf-8')

find_dominant(data[(data.Station=='Парис_садок') & (data.Horizon == 0)  & (data.Date >= Sdate) & (data.Date <= Ldate)])
