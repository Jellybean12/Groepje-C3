from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
from math import sqrt

def parser(x):
    return datetime.strptime('190 ' +x, '%Y-%m')

series = pd.read_csv('metingenarima.csv', header=0, parse_dates=[0], index_col=0)
series['meting'] = series['meting'].multiply(1000)
y = series

# The term bfill means that we use the value before filling in missing values
y = y.fillna(y.bfill())
print(series.count())
print(y.count())
series = y
X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(5 ,1 ,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = sqrt(mean_squared_error(test, predictions))
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()