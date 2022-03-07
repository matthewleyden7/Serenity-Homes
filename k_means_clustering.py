from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import random
import os

# Main method to create k-means cluster images

def create_k_means_clusters(variable1, variable2, num_clusters, count):

    colors = ['blue', 'red', 'pink', 'orange', 'yellow', 'black', 'green']

    df = pd.read_csv('data/modified_house_data.csv')
    df = df[[variable1, variable2]]


    # elbow
    k_rng = range(1, 10)
    sse = []
    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(df[[variable1, variable2]])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of squared error')
    plt.plot(k_rng, sse)
    plt.savefig(f'k_means_images/elbow{count}.png')
    plt.close()


    km = KMeans(n_clusters=num_clusters)
    y_predicted = km.fit_predict(df[[variable1, variable2]])
    df['cluster2'] = y_predicted

    # create new dataframe for each cluster integer and put in dataframes list
    dataframes = []
    for i in range(num_clusters):
        new_df = df[df.cluster2==i]
        dataframes.append(new_df)

    # choose random colors for plots
    color_codes = []
    for i in range(num_clusters):
        color = random.choice([c for c in colors if c not in color_codes])
        color_codes.append(color)

    # Use matplotlib to scatter each dataframes data points on graph
    dataframes = [plt.scatter(dataframe[variable1], dataframe[variable2], color=color_codes[i], label=variable2)
                  for i, dataframe in enumerate(dataframes)]
    # insert centroids
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')

    plt.xlabel(variable1)
    plt.ylabel(variable2)
    plt.legend()
    plt.title('Clusters')
    plt.savefig(f'k_means_images/clusters{count}.png')
    plt.close()


    # scaling for scaled clusters
    scaler = MinMaxScaler()
    scaler.fit(df[[variable2]])
    df[variable2] = scaler.transform(df[[variable2]])
    scaler.fit(df[[variable1]])
    df[variable1] = scaler.transform(df[[variable1]])

    km2 = KMeans(n_clusters=num_clusters)
    y_predicted2 = km2.fit_predict(df[[variable1, variable2]])
    print(y_predicted)
    df['cluster'] = y_predicted2

    dataframes2 = []
    for i in range(num_clusters):
        new_df = df[df.cluster==i]
        dataframes2.append(new_df)

    dataframes2 = [plt.scatter(dataframe[variable1], dataframe[variable2], color=color_codes[i], label=variable2)
                  for i, dataframe in enumerate(dataframes2)]

    plt.scatter(km2.cluster_centers_[:, 0], km2.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')
    plt.xlabel(variable1)
    plt.ylabel(variable2)
    plt.legend()
    plt.title('Scaled Clusters')
    plt.savefig(f'k_means_images/scaled_clusters{count}.png')
    plt.close()

    # create centroids only image
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')
    plt.xlabel(variable1)
    plt.ylabel(variable2)
    plt.title('Centroids')
    plt.savefig(f'k_means_images/centroids{count}.png')
    plt.close()




