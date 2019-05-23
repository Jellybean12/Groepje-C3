import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import re
from matplotlib.pylab import rcParams
import sqlite3
import seaborn as sns; sns.set()
from tqdm import tqdm
rcParams['figure.figsize'] = 12, 10
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error


def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

series = read_csv('satallbor475.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)
series = pd.DataFrame(series)
series['meting'] = series['meting'].multiply(1000)
series = series.head(1000)
X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()


from statsmodels.tsa.arima_model import ARIMA

model = ARIMA(series.meting, order=(2, 2, 10))
results_ARIMA = model.fit(disp=-1)