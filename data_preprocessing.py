import pandas as pd

caffeine_dat_uncleaned = pd.read_csv('caffeine.csv')
caffeine_dat_uncleaned.rename(columns={'Caffeine (mg)': 'caffeine',
                                       'Volume (ml)': 'volumn'}, inplace=True)
caffeine_dat_uncleaned.columns= caffeine_dat_uncleaned.columns.str.lower()
caffeine_dat_uncleaned.isnull().sum()


caffeine_dat_uncleaned.describe()


caffeine_dat_uncleaned.t0_csv('caffeine_cleaned.csv')
