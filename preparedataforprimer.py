# -*- coding: utf-8 -*-
# -----------------
# Работаем с иерархической кластеризацией
# используем праймер-стайл
# строки - образцы (дата+станция)
# столбцы - виды
# берем данные со второго горизонта
# ------------------

import pandas as pd
import datetime

def partofMonth(x):
    x = int(x)
    res = 'err'
    if ( x<11):
        res = 'I'
    if ( 10< x < 21 ):
        res =  'II'
    if ( x > 20 ):
        res = 'III'
    return res

def primer(st, species, dates):
    #allData = pd.DataFrame(data=np.zeros(len(species)), index = species)
    allData = pd.DataFrame()
    for date in dates:
#        try:
        dayDataSt = st.loc[idx[date, :]].reset_index(0)['N'].reindex(species, fill_value=0)
#        except:
#            dayDataSt = pd.DataFrame(np.zeros(len(species)),index=species)
        allData = pd.concat([allData, dayDataSt], axis=1)
    allData.columns=dates

    return allData

def preparedata(data, horizon):
    speciesList = data[data.Horizon == horizon].groupby('Species').first().index.tolist()
    datesSadok = data[(data.Station == 'Парис_садок') & (data.Horizon == horizon)].groupby('Date').first().index.tolist()
    datesBalka = data[(data.Station == 'Балка_фоновая') & (data.Horizon == horizon)].groupby('Date').first().index.tolist()
    dateslist = []
    for i in range(len(datesSadok)):
        date = datetime.datetime.strptime(datesSadok[i], '%Y-%m-%d')
        months = date.strftime('%b')
        part = partofMonth(date.strftime('%d'))
       # print date.strftime('%d')
        dateslist.append(months+part+'-1')
    for i in range(len(datesBalka)):
        date = datetime.datetime.strptime(datesBalka[i], '%Y-%m-%d')
        months = date.strftime('%b')
        part = partofMonth(date.strftime('%d'))
        dateslist.append(months+part+'-2')
   # print date.strftime('%d')
    #dateslist.append(months+part+'-2')
#    dateslist = []
#    for i in range(len(datesSadok)):
#        d = datetime.datetime.strptime(datesSadok[0], '%Y-%m-%d')
#        dateslist.append()
    #dateslist = [datesSadok[i]+' st. 1' for i in range(len(datesSadok))]+[datesBalka[i]+' st. 2' for i in range(len(datesBalka))]

#    print dateslist[0]
#    print dateslist[0].split("-",1)
#    print dateslist[0].split("-",1)[1]
#    print dateslist[0].split("-",2)

    groupSadok = data[(data.Horizon == horizon) & (data.Station == 'Парис_садок')].groupby(['Date', 'Species'])['N'].first()
    groupBalka = data[(data.Horizon == horizon) & (data.Station == 'Балка_фоновая')].groupby(['Date', 'Species'])['N'].first()

    sadok = primer(groupSadok,speciesList,datesSadok)
    balka = primer(groupBalka,speciesList,datesBalka)

    primerdata = pd.concat([sadok.T,balka.T],  axis=0, ignore_index=True)
    primerdata.index = dateslist

    return primerdata
# main part
pd.options.display.max_rows = 9999
idx = pd.IndexSlice

inBio = pd.read_csv('base.csv', sep=';', parse_dates=True)
Bio2013 = inBio[(inBio.Date >= '2012-12-01') & (inBio.Date <= '2013-11-31')]
Bio2014 = inBio[(inBio.Date >= '2013-12-01') & (inBio.Date <= '2014-11-31')]
Bio2015 = inBio[(inBio.Date >= '2014-12-01') & (inBio.Date <= '2015-11-31')]

horizont = 0
primer2013 = preparedata(Bio2013,horizont)
primer2014 = preparedata(Bio2014,horizont)
primer2015 = preparedata(Bio2015,horizont)

primer2013.astype(int).to_csv('data2013.csv', sep=';', encoding='utf-8')
primer2014.astype(int).to_csv('data2014.csv', sep=';', encoding='utf-8')
primer2015.astype(int).to_csv('data2015.csv', sep=';', encoding='utf-8')
