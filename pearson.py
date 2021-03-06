# -*- coding: utf-8 -*-
# -----------------
# Считаем коэфициент Пирсона с помощью скайпи
# между гидрохимией и количеством
# на станции Садок
# + доминирующие виды
# ------------------
import pandas as pd
import numpy as np
import scipy.stats as stats

def pearson_prepare_himia(indata):
    '''Подготавливаем данные гидрохими к обработке Пирсоном. \
    На входе - срезы по периодам \
    На выходе - словарь с Гидрохимией'''
    CH = {'t': pd.Series(indata['t'].tolist()),
          'S': pd.Series(indata['S'].tolist()),
          'pH': pd.Series(indata['pH'].tolist()),
          'SS': pd.Series(indata['SS'].tolist()),
          'COD_nf': pd.Series(indata['COD_nf'].tolist()),
          'DIN_uM': pd.Series(indata['DIN_uM'].tolist()),
          'Si_uM': pd.Series(indata['Si_uM'].tolist()),
          'DIP_uM': pd.Series(indata['DIP_uM'].tolist()),
          'DOP_uM': pd.Series(indata['DOP_uM'].tolist()),
          'Cl': pd.Series(indata['Cl'].tolist())
          }
    return CH


def pearson_prepare_bio(indata, otdel):
    '''
    Подготавливаем данные биологии к обработке Пирсоном\
    На входе - срезы по периодам и название отдела для группировки.\
    На выходе - словарь (количество и биомасса) с биологией
    '''
    OtdelData = indata[(indata.Otdel == otdel)]
    GroupData = OtdelData.groupby(['Date']).agg({'N': np.mean, 'B': np.mean})
    # ssqrt transform
    GroupData = np.sqrt(np.sqrt(GroupData))
    # log transform
    #GroupData = np.log(1.0+GroupData)
    BIO = {'N': pd.Series([GroupData.iloc[i, 1] for i in range(0, len(GroupData))]),
           'B': pd.Series([GroupData.iloc[i, 0] for i in range(0, len(GroupData))])}
    return BIO['N'].tolist()

def find_dominant(indata):
    '''
    Ищем домимантные виды (больше 20% от общей численности)\
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
    return meanData[0].tolist()

def print_pearson(data):
     print data['t'][0], data['S'][0], data['pH'][0], data['SS'][0], data['COD_nf'][0], \
        data['DIN_uM'][0], data['Si_uM'][0], data['DIP_uM'][0], data['DOP_uM'][0], data['Cl'][0]
def print_significance(data):
      print data['t'][1], data['S'][1], data['pH'][1], data['SS'][1], data['COD_nf'][1], \
        data['DIN_uM'][1], data['Si_uM'][1], data['DIP_uM'][1], data['DOP_uM'][1], data['Cl'][1]
def check(data):
    if (0.01<data[1]<0.05):
        return str(data[0])+'*'
    if (data[1]<0.01):
        return str(data[0])+'**'
    return data[0]
def print_format(data):
      print check(data['t']), check(data['S']), check(data['pH']), check(data['SS']), check(data['COD_nf']), \
        check(data['DIN_uM']), check(data['Si_uM']), check(data['DIP_uM']), check(data['DOP_uM']), check(data['Cl'])

def pearson(inBio, inHimia, Otd, SdateB, LdateB, SdateH, LDateH):
    '''
    Считаем пирсона со значимостью по отделам на период
    '''
    biodata = inBio[(inBio.Horizon == 0) & (inBio.Date >= SdateB) & (inBio.Date <= LdateB) & (inBio.Station == 'Садок')]
    himiadata = inHimia.loc[(inHimia.Date >= SdateH) & (inHimia.Date <= LDateH)]
    B = pearson_prepare_bio(biodata, Otd)
    H = pearson_prepare_himia(himiadata)
    if (SdateB=='2013-12-01'):
        del B[1]

    if ((Otd=='Dino') and (SdateB=='2013-06-01')):
        for el in H:
            del H[el][1]

    if ((Otd=='Bacil') and (SdateB=='2014-12-01')):
        del B[2]
    if ((Otd=='Dino') and (SdateB=='2013-03-01')):
        for el in H:
            del H[el][1]
    if (SdateB=='2015-06-01'):
        del B[3:5]
    if ((Otd=='Dino') and (SdateB=='2015-03-01')):
        for el in H:
            del H[el][2]
    try:
        stats.pearsonr(H['t'], B)
        stats.pearsonr(H['S'], B)
        stats.pearsonr(H['pH'], B)
        stats.pearsonr(H['SS'], B)
        stats.pearsonr(H['COD_nf'], B)
        stats.pearsonr(H['DIN_uM'], B)
        stats.pearsonr(H['Si_uM'], B)
        stats.pearsonr(H['DIP_uM'], B)
        stats.pearsonr(H['DOP_uM'], B)
        stats.pearsonr(H['Cl'], B)
    except ValueError:
        PC = {'err': 'Check data!',
              'pt': '',
              'pS': '',
              'ppH': '',
              'pSS': '',
              'pCOD': '',
              'pDIN': '',
              'pSi': '',
              'pDIP': '',
              'pDOP': '',
              'Cl': ''}
    else:
        PC = {'err': 'ok!',
              't': stats.pearsonr(H['t'], B),
              'S': stats.pearsonr(H['S'], B),
              'pH': stats.pearsonr(H['pH'], B),
              'SS': stats.pearsonr(H['SS'], B),
              'COD_nf': stats.pearsonr(H['COD_nf'], B),
              'DIN_uM': stats.pearsonr(H['DIN_uM'], B),
              'Si_uM': stats.pearsonr(H['Si_uM'], B),
              'DIP_uM': stats.pearsonr(H['DIP_uM'], B),
              'DOP_uM': stats.pearsonr(H['DOP_uM'], B),
              'Cl': stats.pearsonr(H['Cl'], B)}
    if (PC['err'] == 'ok!'):
        print_format(PC)
    else:
        print PC['err']

def pearson_dominant(inBio, inHimia, SdateB, LdateB, SdateH, LDateH):
    '''
    Считаем пирсона со значимостью для доминантных видов на период
    '''
    biodata = inBio[(inBio.Horizon == 0) & (inBio.Date >= SdateB) & (inBio.Date <= LdateB) & (inBio.Station == 'Садок')]
    himiadata = inHimia.loc[(inHimia.Date >= SdateH) & (inHimia.Date <= LDateH)]
    B = find_dominant(biodata)
    H = pearson_prepare_himia(himiadata)
    if (SdateB=='2013-12-01'):
        del B[1]
    if (SdateB=='2014-12-01'):
        del B[2]
    if (SdateB=='2015-06-01'):
        del B[3:5]
    try:
        stats.pearsonr(H['t'], B)
        stats.pearsonr(H['S'], B)
        stats.pearsonr(H['pH'], B)
        stats.pearsonr(H['SS'], B)
        stats.pearsonr(H['COD_nf'], B)
        stats.pearsonr(H['DIN_uM'], B)
        stats.pearsonr(H['Si_uM'], B)
        stats.pearsonr(H['DIP_uM'], B)
        stats.pearsonr(H['DOP_uM'], B)
        stats.pearsonr(H['Cl'], B)
    except ValueError:
        PC = {'err': 'Check data!',
              'pt': '',
              'pS': '',
              'ppH': '',
              'pSS': '',
              'pCOD': '',
              'pDIN': '',
              'pSi': '',
              'pDIP': '',
              'pDOP': '',
              'Cl': ''}
    else:
        PC = {'err': 'ok!',
              't': stats.pearsonr(H['t'], B),
              'S': stats.pearsonr(H['S'], B),
              'pH': stats.pearsonr(H['pH'], B),
              'SS': stats.pearsonr(H['SS'], B),
              'COD_nf': stats.pearsonr(H['COD_nf'], B),
              'DIN_uM': stats.pearsonr(H['DIN_uM'], B),
              'Si_uM': stats.pearsonr(H['Si_uM'], B),
              'DIP_uM': stats.pearsonr(H['DIP_uM'], B),
              'DOP_uM': stats.pearsonr(H['DOP_uM'], B),
              'Cl': stats.pearsonr(H['Cl'], B)}
    if (PC['err'] == 'ok!'):
        print_format(PC)
    else:
        print PC['err']

# main
pd.options.display.max_rows = 9999
idx = pd.IndexSlice
# prepare data
data = pd.read_csv('base.csv', sep=';', parse_dates=True)
himia = pd.read_csv('hydrochemistry.csv', sep=',', parse_dates=True)
# output

# pearson correlation coefficients by otdels
#'''
print '2013'
pearson(data, himia,'Bacil','2013-02-01', '2013-02-28', '2013-01-01', '2013-02-28')
pearson(data, himia,'Dino','2013-02-01', '2013-02-28', '2013-01-01', '2013-02-28')
pearson(data, himia,'Bacil','2013-04-01', '2013-05-31', '2013-04-01', '2013-05-31')
pearson(data, himia,'Dino','2013-03-01', '2013-05-31', '2013-03-01', '2013-05-31')
pearson(data, himia,'Bacil','2013-06-01', '2013-08-31', '2013-06-01', '2013-08-31')
pearson(data, himia,'Dino','2013-06-01', '2013-08-31', '2013-06-01', '2013-08-31')
pearson(data, himia,'Bacil','2013-09-01', '2013-11-30', '2013-09-01', '2013-11-30')
pearson(data, himia,'Dino','2013-09-01', '2013-11-30', '2013-09-01', '2013-11-30')
print '2014'
pearson(data, himia,'Bacil','2013-12-01', '2014-02-28', '2013-12-01', '2014-02-28')
pearson(data, himia,'Dino','2013-12-01', '2014-02-28', '2013-12-01', '2014-02-28')
pearson(data, himia,'Bacil','2014-03-01', '2014-05-31', '2014-03-01', '2014-05-31')
pearson(data, himia,'Dino','2014-03-15', '2014-05-31', '2014-03-15', '2014-05-31')
pearson(data, himia,'Bacil','2014-06-01', '2014-08-31', '2014-06-01', '2014-08-31')
pearson(data, himia,'Dino','2014-06-01', '2014-08-31', '2014-06-01', '2014-08-31')
pearson(data, himia,'Bacil','2014-09-01', '2014-11-30', '2014-09-01', '2014-11-30')
pearson(data, himia,'Dino','2014-09-01', '2014-11-30', '2014-09-01', '2014-11-30')
print '2015'
pearson(data, himia,'Bacil','2014-12-01', '2015-02-28', '2014-12-01', '2015-02-28')
pearson(data, himia,'Dino','2014-12-10', '2015-02-28', '2014-12-01', '2015-02-28')
pearson(data, himia,'Bacil','2015-03-01', '2015-05-31', '2015-03-01', '2015-05-31')
pearson(data, himia,'Dino','2015-03-01', '2015-05-31', '2015-03-01', '2015-05-31')
pearson(data, himia,'Bacil','2015-06-01', '2015-08-31', '2015-06-01', '2015-08-31')
pearson(data, himia,'Dino','2015-06-01', '2015-08-31', '2015-06-01', '2015-08-31')
pearson(data, himia,'Bacil','2015-09-01', '2015-11-30', '2015-09-01', '2015-11-30')
pearson(data, himia,'Dino','2015-09-01', '2015-11-30', '2015-09-01', '2015-11-30')
#'''
'''
# pearson correlation coefficients for dominantes
print '2013'
pearson_dominant(data, himia,'2013-02-01', '2013-02-28', '2013-01-01', '2013-02-28')
pearson_dominant(data, himia,'2013-03-01', '2013-05-31', '2013-03-01', '2013-05-31')
pearson_dominant(data, himia,'2013-06-01', '2013-08-31', '2013-06-01', '2013-08-31')
pearson_dominant(data, himia,'2013-09-01', '2013-11-30', '2013-09-01', '2013-11-30')
print '2014'
pearson_dominant(data, himia,'2013-12-01', '2014-02-28', '2013-12-01', '2014-02-28')
pearson_dominant(data, himia,'2014-03-01', '2014-05-31', '2014-03-01', '2014-05-31')
pearson_dominant(data, himia,'2014-06-01', '2014-08-31', '2014-06-01', '2014-08-31')
pearson_dominant(data, himia,'2014-09-01', '2014-11-30', '2014-09-01', '2014-11-30')
print '2015'
pearson_dominant(data, himia,'2014-12-01', '2015-02-28', '2014-12-01', '2015-02-28')
pearson_dominant(data, himia,'2015-03-01', '2015-05-31', '2015-03-01', '2015-05-31')
pearson_dominant(data, himia,'2015-06-01', '2015-08-31', '2015-06-01', '2015-08-31')
pearson_dominant(data, himia,'2015-09-01', '2015-11-30', '2015-09-01', '2015-11-30')
'''