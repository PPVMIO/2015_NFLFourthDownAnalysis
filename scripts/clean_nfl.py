# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 12:18:16 2016

@author: PaulPelayo
"""
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action = "ignore")

df = pd.read_csv('../data/nflplaybyplay2015.csv')
#df.drop(['Unnamed: 0'], axis=1, inplace=True)

all_plays_vc = df['posteam'].value_counts()
all_plays = all_plays_vc.to_dict()


fourth = df[df['down'] == 4]
fourth_plays = pd.DataFrame(fourth['posteam'].value_counts())
#fourth_plays = fourth_plays.rename(columns={'Index': 'Team Name', 'posteam': '4th Down'})
#fourth_plays['Total Plays'] = fourth_plays..map(all_plays)


play_codes = {'Punt': 0, 'Field Goal': 1, 'Pass': 2, 'No Play': -1,
              'Run': 2, 'Sack': 2, 'QB Kneel': -1, 'Timeout': -1}
fourth['PlayTypeCode'] = fourth['PlayType'].map(play_codes)


fourth['QtrTime'] = fourth['TimeSecs'] * 10 + fourth['qtr']
fourth = fourth.drop(['Unnamed: 0', 'PlayAttempted', 'Season'], 1)
converted_flag = fourth['ydstogo'] > fourth['Yards.Gained']
fourth['converted'] = 1
fourth.loc[converted_flag, 'converted'] = 0







