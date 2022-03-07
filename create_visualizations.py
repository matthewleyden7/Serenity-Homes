import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits
import sklearn
from sklearn import preprocessing, ensemble
from sklearn.model_selection import train_test_split
import seaborn as sns
from collections import Counter


# Load dataset into Pandas dataframe and create bar graphs and plots to describe the data

# create average price by view bar chart
def average_price_by_view(dataframe):
    views = dataframe['view'].unique()
    views = list(views)
    view_dict = {'views': [], 'average_price': []}
    views = sorted(list(views))
    for view in views:
        df = dataframe[dataframe.view == view]
        mean_df = df['price'].mean()
        view_dict['views'].append(view)
        view_dict['average_price'].append(mean_df)

    df = pd.DataFrame(view_dict, columns=['views', 'average_price'])
    bar = sns.barplot(y='average_price', x='views', data=df)
    bar.set_title('Average price of house based on quality of view', fontdict= { 'fontsize': 11})
    bar.set_xlabel('View')
    bar.set_ylabel('Average Price')
    plt.savefig('data_images/Average price by view.png')

# create average price by zipcode bar chart.
def average_price_per_zipcode(dataframe):
    zipcodes = dataframe['zipcode'].unique()
    zipcode_dict = {'zipcodes': [], 'average_price': []}
    for zip_code in zipcodes:
        df = dataframe[dataframe.zipcode==zip_code]
        mean_df = df['price'].mean()
        zipcode_dict['zipcodes'].append(zip_code)
        zipcode_dict['average_price'].append(mean_df)

    df = pd.DataFrame(zipcode_dict, columns=['zipcodes', 'average_price'])
    print(df.head())
    sns.barplot(y='average_price', x='zipcodes', data=df)
    plt.show()

# create average price by condition bar chart
def average_price_per_condition(dataframe):
    conditions = dataframe['condition'].unique()
    conditions = list(conditions)
    condition_dict = {'conditions': [], 'average_price': []}
    conditions = sorted(list(conditions))
    for cond in conditions:
        df = dataframe[dataframe.condition == cond]
        mean_df = df['price'].mean()
        condition_dict['conditions'].append(cond)
        condition_dict['average_price'].append(mean_df)

    df = pd.DataFrame(condition_dict, columns=['conditions', 'average_price'])
    bar = sns.barplot(y='average_price', x='conditions', data=df)
    bar.set_title('Average price of house based on condition', fontdict= { 'fontsize': 11})
    bar.set_xlabel('Condition')
    bar.set_ylabel('Average Price')
    plt.savefig('data_images/Average price per condition.png')

# Create average price by grade bar chart
def average_price_per_grade(dataframe):
    grades = dataframe['grade'].unique()
    grades = list(grades)
    grades = sorted(grades)
    grades_dict = {'grades': [], 'average_price': []}
    for grade in grades:
        df = dataframe[dataframe.grade == grade]
        mean_df = df['price'].mean()
        grades_dict['grades'].append(grade)
        grades_dict['average_price'].append(mean_df)

    df = pd.DataFrame(grades_dict, columns=['grades', 'average_price'])
    bar = sns.barplot(y='average_price', x='grades', data=df)
    bar.set_title('Average price of by level of construction/design', fontdict= { 'fontsize': 11})
    bar.set_xlabel('Grade')
    bar.set_ylabel('Average Price ( * 1 million)')
    plt.savefig('data_images/Average price per grade.png')

# Create price by square footage of internal living space plot
def price_per_sqft_living(data):
    data['price'] = data['price'].map(lambda i: np.log(i) if i > 0 else 0)
    data['sqft_lot'] = data['sqft_lot'].map(lambda i: np.log(i) if i > 0 else 0)
    data['view'] = data['view'].map(lambda i: np.log(i) if i > 0 else 0)
    data.skew()
    target_col = ['price']
    features = list(set(list(data.columns)) - set(data[target_col]))
    # Normalize features between 0 and 1
    data[features] = data[features] / data[features].max()
    data.describe()
    data.skew()

    y = data[target_col].values
    sns.set()
    fig=plt.figure(figsize=(20,6))
    plt.scatter(data['sqft_living'],y, color='green')
    plt.xlabel('Square Footage Living Space', fontdict= { 'fontsize': 16})
    plt.ylabel('Price', fontdict= { 'fontsize': 16})
    plt.title('Price by Square Footage', fontdict= { 'fontsize': 16})
    plt.savefig('data_images/Price by square footage.png')



# Load the modified dataset into a Pandas dataframe
df = pd.read_csv('modified_house_data.csv')

# average_price_by_view(df)
# average_price_per_zipcode(df)
# average_price_per_condition(df)
# average_price_per_grade(df)



