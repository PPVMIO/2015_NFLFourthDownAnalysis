# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 14:39:59 2016

@author: PaulPelayo
"""

import clean_nfl
import pandas as pd
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table
from scipy import stats
from statsmodels.formula.api import ols




all_plays = pd.read_csv('../data/nflplaybyplay2015.csv')
standings15 = pd.read_csv('../data/standings2015.csv')

play_codes = {'Punt': 'Punt', 'Field Goal': 'Field Goal', 'Pass': 'Play Attempt (Pass/Run/Sack)', 'No Play': 'Other', 'Run': 'Play Attempt (Pass/Run/Sack)', 'Sack': 'Play Attempt (Pass/Run/Sack)', 'QB Kneel': 'Other', 'Timeout': 'Other'}
all_plays['PlayTypeCode'] = all_plays['PlayType'].map(play_codes)


short_flag = all_plays['ydstogo'] < 5
med_flag = (all_plays['ydstogo'] >= 5) & (all_plays['ydstogo'] <= 10)
long_flag = all_plays['ydstogo'] > 10

all_plays.loc[short_flag, 'dist_cat'] = 'Short'
all_plays.loc[med_flag, 'dist_cat'] = 'Medium'
all_plays.loc[long_flag, 'dist_cat'] = 'Long'


other_plays = all_plays[all_plays['down'] != 4]
fourth_plays = all_plays[all_plays['down'] == 4]
fourth_plays = fourth_plays.drop(['Unnamed: 0', 'PlayAttempted', 'Season'], 1)
converted_flag = fourth_plays['ydstogo'] > fourth_plays['Yards.Gained']
fourth_plays['converted'] = 1
fourth_plays.loc[converted_flag, 'converted'] = 0

attempts = fourth_plays[fourth_plays['PlayTypeCode'] == 'Play Attempt (Pass/Run/Sack)']
fourth_plays_vc = dict(fourth_plays['posteam'].value_counts())
attempts_vc = dict(attempts['posteam'].value_counts())


standings15['4th Possesions'] = standings15['Team'].map(fourth_plays_vc)
standings15['4th Attempts'] = standings15['Team'].map(attempts_vc)

standings15['PercentAttempts'] = standings15['4th Attempts']/standings15['4th Possesions']

cleaned_attempts = attempts[attempts['ydstogo'] < 10]
cleaned_attempts_vc = dict(cleaned_attempts['posteam'].value_counts())
standings15['4th Attempts Cleaned'] = standings15['Team'].map(cleaned_attempts_vc)
standings15['Percent Attempts (Less than 10yds)'] = standings15['4th Attempts Cleaned']/standings15['4th Possesions']


punts = fourth_plays[fourth_plays['PlayTypeCode'] == 'Punt']
punts_vc = dict(fourth_plays['posteam'].value_counts())
standings15['Punts'] = standings15['Team'].map(punts_vc)
standings15['Attempts to Punt Ratio'] = standings15['4th Attempts Cleaned']/standings15['Punts']

model = ols('Win~PercentAttempts', standings15).fit()


#fdwn_avg_dist = np.mean(fourth_plays['ydstogo'])
#sns.distplot(fourth_plays['ydstogo'])

attempts = fourth_plays[fourth_plays['PlayTypeCode'] == 'Play Attempt (Pass/Run/Sack)']
punts = fourth_plays[fourth_plays['PlayTypeCode'] == 0]
field_goals = fourth_plays[fourth_plays['PlayTypeCode'] == 1]
other_plays = fourth_plays[fourth_plays['PlayTypeCode'] == -1]

first_qtr = fourth_plays[fourth_plays['qtr'] == 1]
second_qtr = fourth_plays[fourth_plays['qtr'] == 2]
third_qtr = fourth_plays[fourth_plays['qtr'] == 3]
fourth_qtr = fourth_plays[fourth_plays['qtr'] == 4]



def distribution_dist_cat():
    g1 = sns.FacetGrid(fourth_plays, col='PlayTypeCode')
    g1.map(plt.hist, 'dist_cat')
    g2 = sns.FacetGrid(fourth_plays, col='PlayTypeCode')
    g2.map(sns.boxplot, 'dist_cat')
    


def distribution_timsecs():
    g = sns.FacetGrid(fourth_plays, col='PlayTypeCode')
    g.map(sns.distplot, 'TimeSecs')



def distribution_dist_to_goal():
    g1 = sns.FacetGrid(fourth_plays, col='PlayTypeCode')
    g1.map(plt.hist, 'yrdline100')
    g2 = sns.FacetGrid(fourth_plays, col='PlayTypeCode')
    g2.map(sns.boxplot, 'yrdline100')
    
def boxplot_dist_to_goal():
    sns.boxplot(x='yrdline100', y='PlayTypeCode', orient='h', data=fourth_plays, palette="PRGn")
    sns.despine(offset=25, trim=True)
    
def distance_to_goal_stats():
    att = attempts['yrdline100']
    punt = punts['yrdline100']
    fg = field_goals['yrdline100']
    other = other_plays['yrdline100']
    rows = ['4th Down Attempt', 'Punt', 'FG', 'Other']
    
    distance_avg = [round(np.mean(att), 2), round(np.mean(punt), 2), round(np.mean(fg), 2), round(np.mean(other), 2)]
    distance_mode = [stats.mode(att).mode, stats.mode(punt).mode, stats.mode(fg).mode, stats.mode(other).mode]
    distance_sd = [round(np.std(att), 2), round(np.std(punt), 2), round(np.std(fg), 2), round(np.std(other), 2)]    
    tbl = Table([rows, distance_avg, distance_mode, distance_sd], names=('Type', 'Average Yards', 'Mode', 'SD'))
    print(tbl)

    
def main():
    #hist_distance()
    #distance_to_goal_stats()
    print('hello world')
    
    
if __name__ == '__main__':
    main()