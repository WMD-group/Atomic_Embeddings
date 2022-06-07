from scipy.stats import pearsonr
from numpy.linalg import norm
from itertools import combinations_with_replacement
import pandas as pd
from pymatgen.core import Element
from sklearn.metrics import DistanceMetric
import random
from sklearn import decomposition
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
from typing import Callable, Generator, Optional, Tuple
import os
import json
import numpy as np
from sklearn.manifold import TSNE

module_directory = path.abspath(path.dirname(__file__))
data_directory = path.join(module_directory, '../data')

class Atomic_Embeddings:

    def __init__(self, embeddings):
        self.embeddings=embeddings

        if not isinstance(self.embeddings["H"], np.ndarray):
            self.embeddings = {ele:np.array(self.embeddings[ele]) for ele in self.embeddings }

        self.dim = len(random.choice(list(self.embeddings.values())))
        self.element_list = list(self.embeddings.keys()) 
    @staticmethod
    def from_json(
    embedding_json: Optional[str]=None

    ):
        """Creates an instance of the Atomic_Embeddings class from a default embedding file.

        Args:
            embedding_json (str): JSON-style representation of a set of atomic embedding vectors.
            This is a python dictionary of element:embedding vector pairs.
            In a future update, this will be optional and will allow the user to
            specify embedding vectors from the data file.

        Returns:

            A :class:`Atomic_Embeddings` instance."""

        # Get the matscholar embeddings
        if (embedding_json == 'matscholar') or (embedding_json =='matscholar-embedding'):
            matscholar_json = path.join(data_directory, 'matscholar-embedding.json')
            with open(matscholar_json, 'r') as f:
                embedding_data = json.load(f)
        
        #Get the megnet 16 embeddings
        elif embedding_json == 'megnet16':
            megnet16_json = path.join(data_directory, 'megnet16.json')
            with open(megnet16_json, 'r') as f:
                embedding_data = json.load(f)
            # Remove 'Null' key from megnet embedding
            del embedding_data['Null']
        # Get the random_200 embeddings
        elif embedding_json =='random_200':
            random_200_json = path.join(data_directory, 'random_200.json')
            with open(random_200_json,'r') as f:
                embedding_data=json.load(f)
        # Get the mat2vec embeddings
        elif embedding_json == 'mat2vec':
            mat2vec_json = path.join(data_directory, 'mat2vec.json')
            with open(mat2vec_json,'r') as f:
                embedding_data=json.load(f)
        
        # Get the modified_pettifor embeddings
        elif embedding_json == 'mod_petti':
            mod_petti_json = path.join(data_directory, 'mod_petti.json')
            with open(mod_petti_json,'r') as f:
                embedding_data=json.load(f)
        
        # Get the magpie embeddings
        elif embedding_json == 'magpie':
            magpie_json = path.join(data_directory, 'magpie.json')
            with open(magpie_json,'r') as f:
                embedding_data=json.load(f)
        # Get the oliynyk embeddings
        elif embedding_json == 'oliynyk':
            oliynyk_json = path.join(data_directory, 'oliynyk.json')
            with open(oliynyk_json,'r') as f:
                embedding_data=json.load(f)
        
        # Get the SkipAtom embeddings
        elif embedding_json == 'skipatom':
            skipatom_csv = path.join(data_directory, 'skipatom_20201009_induced.csv')
            df=pd.read_csv(skipatom_csv)
            # Convert df to a dictionary of (ele:embeddings) pairs
            elements = list(df['element'])
            df.drop(['element'], axis=1, inplace=True)
            embeds_array=df.to_numpy()
            embedding_data={elements[i]:embeds_array[i] for i in range(len(embeds_array))}

        else:
            raise(ValueError(f'{embedding_json} not in the data directory.'))
        return Atomic_Embeddings(embedding_data)

    def create_pairs(self):
        ele_list=self.element_list()
        ele_pairs = combinations_with_replacement(ele_list,2)
        return ele_pairs

    def create_correlation_df(self):
        ele_pairs=self.create_pairs()
        table = []
        for ele1, ele2 in ele_pairs:
            pearson = pearsonr(self.embeddings[ele1], self.embeddings[ele2])
            dist = norm(self.embeddings[ele1] - self.embeddings[ele2])

            recip_dist= dist**-1
            table.append((ele1, ele2, pearson[0], dist, recip_dist))
            if ele1 != ele2:
                table.append((ele2, ele1, pearson[0], dist, recip_dist))

        corr_df=pd.DataFrame(table, columns=["ele_1","ele_2", "pearson_corr",
                                             "euclid_dist","reciprocal_euclid_dist"])

        mend_1 = [(Element(ele).mendeleev_no, ele) for ele in corr_df["ele_1"] ]
        mend_2 = [(Element(ele).mendeleev_no, ele) for ele in corr_df["ele_2"] ]

        corr_df["mend_1"] = mend_1
        corr_df["mend_2"] = mend_2

        corr_df=corr_df[["ele_1","ele_2","mend_1","mend_2","euclid_dist",
                    "reciprocal_euclid_dist", "pearson_corr"]]

        return corr_df

    def compute_distance_metric(self, ele1, ele2, metric = "euclidean"):
        """Computes distance metric between two vectors
        Input
            ele1 (str): element symbol
            ele2 (str): element symbol
            metric (str): name of a distance metric

        Output
            distance (float): distance between embedding vectors
            """
        valid_metrics = ["euclidean",
                        "manhattan",
                        "chebyshev"]

        if ele1 not in self.element_list():
            print("ele1 is not an element included within the atomic embeddings")
            raise ValueError
        if ele2 not in self.element_list():
            print("ele2 is not an element included within the atomic embeddings")
            raise ValueError

        if metric not in valid_metrics:
            print(f"Invalid distance metric. Use one of the following metrics:{valid_metrics}")
            raise ValueError

        distance = DistanceMetric.get_metric(metric)

        return distance.pairwise(self.embeddings[ele1].reshape(1,-1), self.embeddings[ele2].reshape(1,-1))


    def create_pearson_pivot_table(self):
        corr_df=self.create_correlation_df()
        pearson_pivot= corr_df.pivot_table(values="pearson_corr", index = "mend_1", columns = "mend_2")
        return pearson_pivot

    def create_distance_correlation_df(self, metric="euclidean"):
        ele_pairs=self.create_pairs()
        table = []
        for ele1, ele2 in ele_pairs:
            dist = self.compute_distance_metric(ele1, ele2, metric = metric)[0][0]
            table.append((ele1, ele2, dist))
            if ele1!=ele2:
                table.append((ele2, ele1, dist))
        corr_df = pd.DataFrame(table, columns = ["ele_1", "ele_2", metric])

        mend_1 = [(Element(ele).mendeleev_no, ele) for ele in corr_df["ele_1"] ]
        mend_2 = [(Element(ele).mendeleev_no, ele) for ele in corr_df["ele_2"] ]

        corr_df["mend_1"] = mend_1
        corr_df["mend_2"] = mend_2

        corr_df = corr_df[["ele_1", "ele_2", "mend_1", "mend_2", metric]]

        return corr_df

    def create_distance_pivot_table(self, metric = "euclidean"):
        corr_df = self.create_distance_correlation_df( metric = metric)
        distance_pivot = corr_df.pivot_table(values = metric, index = "mend_1", columns = "mend_2")
        return distance_pivot


    def plot_pearson_correlation(self, figsize=(24,24)):
        pearson_pivot=self.create_pearson_pivot_table()

        plt.figure(figsize=figsize)
        ax=sns.heatmap(pearson_pivot,
                      cmap="bwr",
                      square=True,
                      linecolor="k")
        plt.show()
        return

    def plot_distance_correlation(self, metric = "euclidean", figsize = (24, 24)):
        distance_pivot = self.create_distance_pivot_table(metric = metric)

        plt.figure(figsize=figsize)
        ax=sns.heatmap(distance_pivot,
                      cmap="bwr",
                      square=True,
                      linecolor="k")
        plt.show()
        return

    def plot_PCA_2D(self, figsize = (16,12), **kwargs):

        embeddings_array= np.array(list(self.embeddings.values()))
        element_array = np.array(self.element_list())

        fig=plt.figure(figsize=figsize)
        plt.cla() # clear current axes
        pca = decomposition.PCA(n_components=2) # project to 2 dimensions

        pca.fit(embeddings_array)
        X = pca.transform(embeddings_array)

        pca_dim1 = X[:,0]
        pca_dim2 = X[:,1]

        ax=sns.scatterplot(x=pca_dim1, y = pca_dim2)

        for i in range(len(X)):
            plt.text(x=pca_dim1[i], y=pca_dim2[i], s =element_array[i])

        plt.show()
        return

    def plot_tSNE(self, n_components=2, figsize=(16,12)):
        """A function to plot a t-SNE plot of the atomic embedding"""
        embeddings_array= np.array(list(self.embeddings.values()))
        element_array = np.array(self.element_list)

        tsne=TSNE(n_components)
        tsne_result = tsne.fit_transform(embeddings_array)

        # Create a dataframe to store the dimension and the label for t-SNE transformation
        tsne_df = pd.DataFrame({'tsne_dim1': tsne_result[:,0], 'tsne_dim2': tsne_result[:,1], 'element':element_array })
        #Create the t-SNE plot
        fig, ax = plt.subplots(figsize=figsize)
        sns.scatterplot(x='tsne_dim1', y='tsne_dim2', data=tsne_df, ax=ax)
        lim = (tsne_result.min()-5, tsne_result.max()+5)
        ax.set_xlim(lim)
        ax.set_ylim(lim)
        
        # Label the points
        for i in range(tsne_df.shape[0]):
            plt.text(x=tsne_df['tsne_dim1'][i], y =tsne_df['tsne_dim2'][i], s = tsne_df['element'][i])

        plt.show()
        return  