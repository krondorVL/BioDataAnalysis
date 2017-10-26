# -*- coding: utf-8 -*-
# -----------------
# Считаем АНОВУ, t-критерий...
# ------------------
import pandas as pd
import numpy as np
import scipy.stats as stats

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
        domSpecies = dayPercentData[dayPercentData.N>50]
        meanData = pd.concat([meanData,domSpecies.mean()]).fillna(0)
        print domSpecies
    #return meanData[0].tolist()
    #return domSpecies

# main
pd.options.display.max_rows = 9999
idx = pd.IndexSlice
# prepare data
data = pd.read_csv('base.csv', sep=';', parse_dates=True)
Sdate = '2013-01-01'
Ldate = '2015-12-31'
speciesList = data[(data.Date >= Sdate) & (data.Date <= Ldate)].groupby('Species').first().index.tolist()

Balka = data[(data.Station=='Балка_фоновая') & (data.Date >= Sdate) & (data.Date <= Ldate)].groupby(['Species'])['N'].sum()
Sadok = data[(data.Station=='Садок') & (data.Date >= Sdate) & (data.Date <= Ldate)].groupby(['Species'])['N'].sum()
Zabor = data[(data.Station=='Водозабор') & (data.Date >= Sdate) & (data.Date <= Ldate)].groupby(['Species'])['N'].sum()


BalkaList = Balka.reindex(speciesList, fill_value=0)
SadokList = Sadok.reindex(speciesList, fill_value=0)
ZaborList = Zabor.reindex(speciesList, fill_value=0)



# Mann-Whitney-Wilcoxon (MWW) RankSum test

#z_stat, p_val = stats.ranksums(BalkaList, SadokList)

# t-test
#t, p = stats.ttest_ind(BalkaList, SadokList, equal_var=False)

# ANOVA
#f_val, p_val = stats.f_oneway(SadokList, BalkaList, ZaborList)

# Kruskal–Wallis ANOVA
#fkw_val, pkw_val = stats.kruskal(SadokList, BalkaList, ZaborList)

# Mann-Whitney rank test
#t, p = stats.mannwhitneyu(BalkaList, SadokList)

# output
#print " Wilcoxon rank-sum (z,p) for Balka and Sadok =", z_stat, p_val #нельзя применять из-за длинной выборки
#print "Mann-Whitney rank test for Balka and Sadok =", t, p
#print "t-test (t,p) for Balka and Sadok =", t, p

#print "One-way ANOVA P =", p_val
#print "One-way Kruskal–Wallis ANOVA P =", pkw_val

print find_dominant(data[(data.Station=='Садок') & (data.Horizon == 0)  & (data.Date >= Sdate) & (data.Date <= Ldate)])

