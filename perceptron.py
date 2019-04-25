import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

data = pd.read_csv('Iris.csv')
y = data.iloc[0:100,5].values
# print y

y = np.where(y == 'Iris-setosa',1,0)
# print y

target = y
x = data.iloc[0:100,[1,4]].values
# print x
# w = np.random.uniform(0,1,x.shape[1])
# print w
X_train, X_test, y_train, y_test = train_test_split(x, target, test_size=0.30, random_state=42)
print X_train.shape

np.random.seed(93)

class Perceptron(object):
    def __init__(self,alpha=0.01,epoch=20):
        self.alpha = alpha
        self.epoch = epoch

    def predict(self,x):
        p = np.dot(x,self.w) + self.b
        return 1.0 if p >= 0.0 else 0.0

    def perc(self,x,y):
        self.w = np.random.uniform(0,1,x.shape[1])
        self.b = np.random.uniform(0,1,1)

        for i in range(self.epoch):
            cost = 0
            for xt,yt in zip(x,y):
                pred = self.predict(xt)
                costy = np.square(yt-pred)
                up = self.alpha * costy
                self.w += up * xt
                self.b += up
        print "parameters: {:.2f}(X1) + {:.2f}(X2) + {:.2f}".format(self.w[0],self.w[1],float(self.b))

clf = Perceptron()
clf.perc(X_train, y_train)


