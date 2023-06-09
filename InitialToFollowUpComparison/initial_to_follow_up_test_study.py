# -*- coding: utf-8 -*-
"""Initial to Follow-Up Test Study

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WlNa04zpXGn6QDETss4XFGGLo3VTTUow
"""

## from google.colab import drive
## drive.mount('/content/drive')

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
from scipy.stats import kstest
import scipy as sp
import pandas as pd
import statsmodels.formula.api as smf

## results = '/content/drive/MyDrive/.S23/497 - Peanut Butter Research Group/Code Files & Github/Dataset/Results'
results = pd.read_csv("TimedtoSequential.csv")
results.info()
results.shape
results.head()
linregdata = pd.read_csv("TimedtoSequentialNoNans.csv")

sns.boxplot(data=results, x='5th Draw');
plt.title("Boxplot");

sns.histplot(data=results, x='5th Draw', bins=50, color='.3');
plt.ylabel('Frequency')
plt.xlabel('Lead Level')
plt.title("Distribution of Sequential 5th Draw Lead Levels");

sns.histplot(data=results, x='5 Minute', bins=50, color='.3');
plt.ylabel('Frequency')
plt.xlabel('Lead Level')
plt.title("Distribution of Timed 5 Minute Lead Levels");

results['5th Draw'].mean()
## results['5th Draw'].median()
## results['5 Minute'].mean()
## results['5 Minute'].median()

sns.pairplot(results, x_vars=['1st Draw'], 
             y_vars='5th Draw', height=4, aspect=1, kind='scatter')
plt.xscale('log')
plt.yscale('log')
plt.show()

sns.pairplot(results, x_vars=['1st Draw', '3 Minute'], 
             y_vars='8th Draw', height=4, aspect=1, kind='scatter')
plt.xscale('log')
plt.yscale('log')
plt.show()

sns.heatmap(results.corr(), cmap="Purples", annot = True, linewidths=0, annot_kws={"size":6})
plt.show()

x = linregdata['5 Minute']
y = linregdata['5th Draw']
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.7, 
                                                    test_size = 0.3, random_state = 100)

linregdata.info()
linregdata.shape
linregdata.head()
linregdata = linregdata.dropna()
x_train
y_train

rng = np.random.default_rng()
stats.kstest(stats.uniform.rvs(size=100, random_state=rng), stats.norm.cdf)

x_train_sm = sm.add_constant(x_train)
lr = sm.OLS(y_train, x_train_sm).fit()
lr.params
lr.summary()

x_multi = results.drop('5th Draw', axis=1)
x_multi_cons = sm.add_constant(x_multi)
x_multi_cons.isna().sum()
results['3 Minute'].apply(lambda x: float(x))

x_multi_cons.isna().sum()

results = results.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
results.info()
results.shape
results.head()

twoToThreeMinute = results['3 Minute'].values
fiveMinute = results['5 Minute'].values
eightDraw = results['8th Draw'].values
result1 = kstest(twoToThreeMinute, fiveMinute)
result2 = kstest(fiveMinute, eightDraw)
print("KS test for 3 Minute:", result1)
print("KS test for 5 Minute:", result2)

def cdf(sample, x, sort = False):
    if sort:
        sample.sort()
    cdf = sum(sample <= x)
    cdf = cdf / len(sample)
    return cdf

stats.norm.cdf(x = x, loc = 0, scale = 1)

def ksnorm(sample):
    sample.sort()
    D_ks = []
    for x in sample:
        cdf_normal = stats.norm.cdf(x = x, loc = 0, scale = 1)
        cdf_sample = cdf(sample = sample, x  = x)
        D_ks.append(abs(cdf_normal - cdf_sample))
    ks_stat = max(D_ks)
    p_value = stats.kstwo.sf(ks_stat, len(sample))
    return {"ks_stat": ks_stat, "p_value" : p_value}

twothree = results['3 Minute'].values
five = results['5 Minute'].values

threetwo = ksnorm(twothree)
print("Results for 3-minute dataset:")
print(threetwo)

cinco = ksnorm(five)
print("Results for 5-minute dataset:")
print(cinco)

def ks_2samp(sample1, sample2):

    obs = np.concatenate((sample1, sample2))
    obs.sort()

    sample1.sort()
    sample2.sort()
    D_ks = []
    for x in obs:
        cdf_sample1 = cdf(sample = sample1, x  = x)
        cdf_sample2 = cdf(sample = sample2, x  = x)
        D_ks.append(abs(cdf_sample1 - cdf_sample2))
    ks_stat = max(D_ks)


    m, n = float(len(sample1)), float(len(sample2))
    en = m * n / (m + n)
    p_value = stats.kstwo.sf(ks_stat, np.round(en))
    return {"ks_stat": ks_stat, "p_value" : p_value}

result = ks_2samp(twothree, five)
print(result)

def kstwo(sample1, sample2):
    sample1.sort()
    sample2.sort()
    D_ks = []
    for x in sample1:
        cdf1 = sum(sample1 <= x) / len(sample1)
        cdf2 = sum(sample2 <= x) / len(sample2)
        D_ks.append(abs(cdf1 - cdf2))
    ks_stat = max(D_ks)
    p_value = stats.ks_2samp(sample1, sample2).pvalue
    return {"ks_stat": ks_stat, "p_value" : p_value}


twothree = results['3 Minute'].values
five = results['5 Minute'].values
fifth = results['5th Draw'].values
eighth = results['8th Draw'].values
first = results['1st Draw'].values

comptwothreefive = kstwo(twothree, five)
print("KS test statistic:", comptwothreefive['ks_stat'])
print("p-value:", comptwothreefive['p_value'])

compfivefifth = kstwo(five, fifth)
print("KS test statistic:", compfivefifth['ks_stat'])
print("p-value:", result['p_value'])

compfiveeighth = kstwo(five, eighth)
print("KS test statistic:", compfiveeighth['ks_stat'])
print("p-value:", compfiveeighth['p_value'])