import pickle
import numpy as np
import pandas as pd
import sklearn
from sklearn import preprocessing, ensemble
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import csv



# preprocess the data to create modified dataset with only the columns we want
def preprocess_data(filename):
    df = pd.read_csv(filename)
    print(df.head())

    df = df.drop(['id', 'date', 'sqft_above', 'sqft_basement', 'lat', 'long', 'sqft_living15', 'sqft_lot15'], axis=1)
    print(df.head())
    print(df.shape)

    df.to_csv('data/modified_house_data.csv', sep=',', index=False)

def preprocess_data2(filename):
    all_rows = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = row[2:12] + row[14:17]
            all_rows.append(row)

    print(len(all_rows))

    with open('data/modified_house_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)





# Method to train data with gradient boosting decision tree regressor
def train_decision_regressor(filename):
    df = pd.read_csv(filename)

    labels = df['price']
    train = df.drop(['price'],axis=1)

    Xtrain , Xtest , Ytrain , Ytest = train_test_split(train, labels, test_size = 0.10,random_state =2)

    generator = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
              learning_rate = 0.1, loss = 'ls')

    generator.fit(Xtrain, Ytrain)

    score = generator.score(Xtest,Ytest)

    print(f'Accuracy  -->  {score}')

    # save the model
    with open('model/new_model.pkl', 'wb') as fid:
      pickle.dump(generator, fid)

    return score


def train_linear_regression(filename):
    df = pd.read_csv(filename)


    print(df.head())
    print(df.describe())

    generator = LinearRegression()

    labels = df['price']

    train = df.drop(['price'], axis=1)

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(train, labels, test_size=0.10, random_state=2)

    generator.fit(Xtrain, Ytrain)
    score = generator.score(Xtest, Ytest)

    print(f'Accuracy  -->  {score}')

    # save the model
    with open('model/new_model.pkl', 'wb') as fid:
        pickle.dump(generator, fid)



#preprocess_data('data/kc_house_data.csv')
#preprocess_data2('data/kc_house_data.csv')
#train_linear_regression('data/modified_house_data.csv')
#train_decision_regressor('data/modified_house_data.csv')

