# This is a Kolmogrov-Smirnov test to find in a quick manner the probability distribution of the data.

import pandas as pd
from scipy import stats
from fitter import Fitter
from fitter import get_common_distributions
import math as mt
import numpy as np

## This function will split the outliers, giving us the extreme and no extreme data. The data between the upper and lower bound will be analysed in the 
## probability distribution function. Here we use the interquartilic range method

def Outliers(DataframeCol):
    '''
    Input, column of dataframe. Output, outliers and normal data. 
    '''
    test = DataframeCol.dropna()
    q1 = test.quantile(0.25)
    q3 = test.quantile(0.75)
    iqr = q3 - q1
    lowBound = q1 - 1.5 * iqr 
    upBound = q3 + 1.5 * iqr
    noOutLiers = test[~((test > upBound) | (test < lowBound))]
    Outliers = test[((test > upBound) | (test < lowBound))]
    
    return(noOutLiers, Outliers)



## The variables of this function are the column of the dataframe to analyse, the common distrubutions for fitter 'cauchy', 'chi2', 'expon', 
## 'exponpow', 'gamma', 'lognorm','norm', 'powerlaw','rayleigh', 'uniform'
def prob_dist(df_test):
    '''
    
    '''
    test = df_test
    dist = get_common_distributions()
    tester = test
    
## Here we iterate over all the distributions the dist varaible has. We will be testing the distribution untill one of them gets acceped by the 
## Kolmogrov-Smirnov goodness test. We use this specific test, given that other test are not precise for n > 5000. 
    for i in range(len(dist)):
        
        
            f = Fitter(tester, timeout = 120, distributions= dist)
            f.fit()
            f.summary(plot=False)
            distributionParameters = f.get_best()
            distToTest = list(f.get_best())[0]
            parameters = f.fitted_param[distToTest]
            bestMatch = list(distributionParameters.keys())
            ksTable = (1.36/(mt.sqrt(len(tester))))
            ksTests = stats.kstest(np.array(tester), bestMatch[0], parameters)
            ksCriteria = ksTests[1]
    
            if ksCriteria >= ksTable:
            # This statement checks if the Criteria valie is bigger than the value calculated in the Kolmogrov Smirnov Table for 0.05. 
            # If approved, we create the following dataframe.
                dfTest = pd.DataFrame(index = ['Distribution', 'Test', 'P-Value'] )
                column = [str(distToTest), float(ksTable), float(ksCriteria)]
                dfTest[tester.name] = column
                return(dfTest)
                break
                
            else:
            #Here the Goodness test was not accepted. So we have to delete this distribution and re-run the test. If we do not delet the distribution, we will get the 
            #same result for every i in the loop. So, at the end we would get nothing. 
                dist.remove(distToTest)

         
df_test = Outliers(DataframeCol)
prob_dist(df_test[0])
#the output will be like this:
	#NameOfTheColumn
#Distribution|	DistAccepted
#Test|	Test_Result
#P-Value|	P-value
