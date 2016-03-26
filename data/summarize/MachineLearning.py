import pylab as pl
import numpy as np
from sklearn import datasets, linear_model ,svm, preprocessing
from aff import Affiliation,SELECTED_AFF_LIST
from sklearn.cross_validation import train_test_split
aff_conf_year_to_kdd_score_dict = Affiliation.get_aff_conf_year_to_kdd_score_dict()
YEAR_LIST = ['2011', '2012', '2013', '2014', '2015']
CONF_NAME_LIST = ['SIGIR', 'SIGMOD', 'SIGCOMM']
now = 0
option = {'SIGIR':[7, 3, True],'SIGMOD':[5, 3, False],'SIGCOMM':[3, 2, False]}
class MachineLearning:
    def __init__(self):
        self.affList = SELECTED_AFF_LIST
        x_test = []
        y_test = []
        x_train = []
        y_train = []
        
    def trainData(self, confName, years = 7, overlap = 5,predictYear = 2015,otherConf = False):
        x_test = []
        y_test = []
        x_train = []
        y_train = []        
        real = []
        if otherConf:
            confList = CONF_NAME_LIST
        else:
            confList = [confName]
        for aff in self.affList:
            for i in (0,overlap):
                score_train = []
                for conf in confList:
                    for year in range(predictYear - 1 - i - years,predictYear - 1 - i):
                        score_train.append(aff_conf_year_to_kdd_score_dict[aff][conf][str(year)])
                x_train.append(score_train)
                y_train.append(aff_conf_year_to_kdd_score_dict[aff][confName][str(predictYear - 1 - i)])
            score_test = []
            for conf in confList:
               for year in range(predictYear - years,predictYear):
                    score_test.append(aff_conf_year_to_kdd_score_dict[aff][conf][str(year)])
            x_test.append(score_test)
            if predictYear < 2016:
                y_test.append(aff_conf_year_to_kdd_score_dict[aff][confName][str(predictYear)])
            else:
                y_test.append(aff_conf_year_to_kdd_score_dict[aff][confName][str(2015)])
        return x_train,x_test,y_train,y_test

    def init_cross_validation(self, confName):
        x_test = []
        y_test = []
        x_train = []
        y_train = []
        for aff in self.affList:
            score_train = []
            for conf in [confName]:
                for i in [0,1,2,3]:
                    score_train.append(aff_conf_year_to_kdd_score_dict[aff][conf][YEAR_LIST[i]])
            x_train.append(score_train)
            y_train.append(aff_conf_year_to_kdd_score_dict[aff][confName][YEAR_LIST[4]])
        x_train,x_test,y_train,y_test = train_test_split(x_train,y_train)
    def merge(self, predict):
        confName = CONF_NAME_LIST[now]
        result = []
        for i in range(len(predict)):
            result.append([self.affList[i],predict[i],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[0]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[1]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[2]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[3]],aff_conf_year_to_kdd_score_dict[self.affList[i]][confName][YEAR_LIST[4]]])# result.append([self.affList[i], predict[i], y_test[i]]) #
        result = sorted(result, key=lambda d: d[1], reverse=True)
        return result

    def linearRegression(self, conf_name,data = 0):
        if data == 0:
            years = option[conf_name][0]
            overlap = option[conf_name][1]
            otherConf = option[conf_name][2]
            data = self.trainData(confName= conf_name,years = years,overlap = overlap,predictYear = 2016,otherConf = otherConf)
        x_train,x_test,y_train,y_test = data
        regr = linear_model.LassoCV()
        regr.fit(x_train, y_train)
        predict = regr.predict(x_test)
        return self.merge(predict)
    def linearRegressionTest(self, confName, years = 7, overlap = 5 ,predictYear = 2015,otherConf = False):
        x_train,x_test,y_train,y_test = self.trainData(confName, years, overlap,predictYear,otherConf)
        regr = linear_model.LassoCV()
        regr.fit(x_train, y_train)
        return regr.score(x_test, y_test)

    def polynomialFeatures(self, conf_name,data = 0):
        if data == 0:
            data = self.trainData(confName= conf_name)
        x_train,x_test,y_train,y_test = data
        x_train = preprocessing.PolynomialFeatures(degree=2).fit_transform(x_train)
        x_test = preprocessing.PolynomialFeatures(degree=2).fit_transform(x_test)
        regr = linear_model.LinearRegression()
        regr.fit(x_train, y_train)
        predict = regr.predict(x_test)
        regr.score()
        print (regr.score(x_test, y_test))
        return self.merge(predict)

    def printOnScreen(self,result):
        for i in range(10):
            print ("\t".join([str(item) for item in result[i]]))
if __name__ == '__main__':
    train = MachineLearning()

    for conf in CONF_NAME_LIST:
        bestScore = 0
        option = []
        for overlap in range(1,6):
            for years in range(3,8):
                for otherConf in [True,False]:
                    score = 0
                    for predictYear in [2013,2014,2015]:
                        score += train.linearRegressionTest(conf,years,overlap,predictYear,otherConf)
                    if score > bestScore:
                        bestScore = score
                        option = [years,overlap,otherConf]
        print (conf + str(option))

    '''for predictYear in [2013,2014,2015]:
        for conf in CONF_NAME_LIST:
            print (str(predictYear) + " " + conf + ":")
            for overlap in range(1,6):
                print ("\t".join([str(train.linearRegressionTest(conf,years,overlap,predictYear)) for years in range(3,8)]))'''
  #  for conf in CONF_NAME_LIST:
        #train.linearRegression(conf)
    #train.printOnScreen()
    #Rank.write_result_tsv()
