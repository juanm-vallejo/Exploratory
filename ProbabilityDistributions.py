#!/usr/bin/env python
# coding: utf-8

# In[113]:


import pandas as pd
from scipy import stats
from fitter import Fitter
from fitter import get_common_distributions
import math as mt
import numpy as np
from collections import defaultdict


def prob_dist(df_test):
    
    test = df_test
    dist = get_common_distributions()
    tester = test.dropna()
    
    for i in range(len(dist)):
        if stats.shapiro(tester)[1] >= 0.05:
            dist_tot_dict[tester].append('norm')

        else:

            f = Fitter(tester, timeout = 120, distributions= dist)
            f.fit()
            f.summary(plot=False)
            distributionParameters = f.get_best()
            distToTest = list(f.get_best())[0]
            parameters = f.fitted_param[distToTest]
            bestMatch = list(distributionParameters.keys())
            ksTable = (1.36/(mt.sqrt(len(tester))))
            ksTests = stats.kstest(np.array(tester), bestMatch[0], parameters)
            ksPValue = ksTests[1]
    
            if ksPValue >= ksTable:
                dfTest = pd.DataFrame(index = ['Distribution', 'Test', 'P-Value'] )
                print(distToTest, ksTable, ksPValue)
                column = [str(distToTest), float(ksTable), float(ksPValue)]
                dfTest[tester.name] = column
                return(dfTest)
                break
                
            else:
                
                dist.remove(distToTest)


# In[10]:


def Outliers(DataframeCol):
    test = DataframeCol
    outliers = []
    q1 = test.quantile(0.25)
    q3 = test.quantile(0.75)
    iqr = q3 - q1
    lowBound = q1 - 1.5 * iqr 
    upBound = q3 + 1.5 * iqr
    noOutLiers = test[~((test > upBound) | (test < lowBound))]
    Outliers = test[((test > upBound) | (test < lowBound))]
    
    return(noOutLiers, Outliers)

