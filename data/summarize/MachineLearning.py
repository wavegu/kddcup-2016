import pylab as pl
import numpy as np
from sklearn import datasets, linear_model ,svm, preprocessing
from aff import Affiliation,SELECTED_AFF_LIST
from sklearn.cross_validation import train_test_split
aff_conf_year_to_kdd_score_dict = Affiliation.get_aff_conf_year_to_kdd_score_dict()
YEAR_LIST = ['2011', '2012', '2013', '2014', '2015']
CONF_NAME_LIST = ['SIGIR', 'SIGMOD', 'SIGCOMM']
now = 2
class MachineLearning:
    def __init__(self):
        self.affList = SELECTED_AFF_LIST
        self.x_test = []
        self.y_test = []
        self.x_train = []
        self.y_train = []
        
    def initData(self, confName):
        self.x_test = []
        self.y_test = []
        self.x_train = []
        self.y_train = []        
        real = []
        for aff in self.affList:
            score_train = []
            score_test = []
            for conf in [confName]:
                for i in [0,1,2]:
                    score_train.append(aff_conf_year_to_kdd_score_dict[aff][conf][YEAR_LIST[i]])
                    score_test.append(aff_conf_year_to_kdd_score_dict[aff][conf][YEAR_LIST[i + 1]])
            self.x_train.append(score_train)
            self.x_test.append(score_test)
            self.y_train.append(aff_conf_year_to_kdd_score_dict[aff][confName][YEAR_LIST[3]])
            self.y_test.append(aff_conf_year_to_kdd_score_dict[aff][confName][YEAR_LIST[4]])
    def init_cross_validation(self, confName):
        self.x_test = []
        self.y_test = []
        self.x_train = []
        self.y_train = []
        for aff in self.affList:
            score_train = []
            for conf in [confName]:
                for i in [0,1,2,3]:
                    score_train.append(aff_conf_year_to_kdd_score_dict[aff][conf][YEAR_LIST[i]])
            self.x_train.append(score_train)
            self.y_train.append(aff_conf_year_to_kdd_score_dict[aff][confName][YEAR_LIST[4]])
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.x_train,self.y_train)
    def merge(self, predict):
        confName = CONF_NAME_LIST[now]
        result = []
        for i in range(len(predict)):
            result.append([self.affList[i],predict[i],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[0]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[1]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[2]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[3]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[4]]])# result.append([self.affList[i], predict[i], self.y_test[i]]) #
        result = sorted(result, key=lambda d: d[1], reverse=True)
        return result

    def linearRegression(self, conf_name):
        regr = linear_model.LassoCV()
        self.initdata(confName = conf_name)
        regr.fit(self.x_train, self.y_train)
        predict = regr.predict(self.x_test)
        print (regr.score(self.x_test, self.y_test))
        return self.merge(predict)

    def polynomialFeatures(self, conf_name):
        self.initData(confName = conf_name)
        self.x_train = preprocessing.PolynomialFeatures(degree=2).fit_transform(self.x_train)
        self.x_test = preprocessing.PolynomialFeatures(degree=2).fit_transform(self.x_test)
        regr = linear_model.LassoCV()
        regr.fit(self.x_train, self.y_train)
        predict = regr.predict(self.x_test)
        print (regr.score(self.x_test, self.y_test))
        return self.merge(predict)

    def printOnScreen(self,result):
        for i in range(10):
            print ("\t".join([str(item) for item in result[i]]))
if __name__ == '__main__':
    train = MachineLearning()
    train.polynomialFeatures(CONF_NAME_LIST[now])
    train.printOnScreen(train.linearRegression(CONF_NAME_LIST[now]))
    #Rank.write_result_tsv()
