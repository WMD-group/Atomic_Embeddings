"""Test the plotter module."""

import os
import unittest

import matplotlib.pyplot as plt
import pytest

from elementembeddings.core import Embedding
from elementembeddings.plotter import dimension_plotter, heatmap_plotter

_file_path = os.path.dirname(__file__)


class HeatmapTest(unittest.TestCase):
    """Test the heatmap_plotter function."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        cls.test_skipatom = Embedding.load_data("skipatom")

    def test_heatmap_plotter(self):
        """Test that the heatmap_plotter function works."""
        # Get the embeddings
        skipatom_cos_plot = heatmap_plotter(
            self.test_skipatom,
            metric="cosine_similarity",
        )
        assert isinstance(skipatom_cos_plot, plt.Axes)
        skipatom_euc_plot = heatmap_plotter(
            self.test_skipatom,
            metric="euclidean",
            show_axislabels=False,
        )
        assert isinstance(skipatom_euc_plot, plt.Axes)


class DimensionTest(unittest.TestCase):
    """Test the dimension_plotter function."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        cls.test_skipatom = Embedding.load_data("skipatom")
        cls.scatter_params = {"s": 50}

    @pytest.mark.mpl_image_compare(
        baseline_dir=f"{_file_path}/baseline",
        filename="test_dimension_2d_plotter_pca.png",
    )
    def test_dimension_2d_plotter_pca(self):
        """Test that the dimension_plotter function works for pca."""
        pca_params = {"svd_solver": "full", "random_state": 42}
        fig, ax = plt.subplots(figsize=(16, 12))
        dimension_plotter(
            self.test_skipatom,
            ax=ax,
            n_components=2,
            reducer="pca",
            adjusttext=False,
            reducer_params=pca_params,
            scatter_params=self.scatter_params,
        )
        return fig

    @pytest.mark.mpl_image_compare(
        baseline_dir=f"{_file_path}/baseline",
        filename="test_dimension_2d_plotter_tsne.png",
    )
    def test_dimension_2d_plotter_tsne(self):
        """Test that the dimension_plotter function works."""
        tsne_params = {"n_iter": 1000, "random_state": 42, "perplexity": 50}
        fig, ax = plt.subplots(figsize=(16, 12))
        dimension_plotter(
            self.test_skipatom,
            ax=ax,
            n_components=2,
            reducer="tsne",
            adjusttext=False,
            reducer_params=tsne_params,
            scatter_params=self.scatter_params,
        )
        return fig

    @pytest.mark.mpl_image_compare(
        baseline_dir=f"{_file_path}/baseline",
        filename="test_dimension_2d_plotter_umap.png",
    )
    def test_dimension_2d_plotter_umap(self):
        """Test that the dimension_plotter function works."""
        umap_params = {"n_neighbors": 15, "random_state": 42}
        fig, ax = plt.subplots(figsize=(16, 12))
        dimension_plotter(
            self.test_skipatom,
            ax=ax,
            n_components=2,
            reducer="umap",
            adjusttext=True,
            reducer_params=umap_params,
            scatter_params=self.scatter_params,
        )
        return fig

    def test_dimension_2d_plotter(self):
        """Test that the dimension_plotter function works."""
        skipatom_pca_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="pca",
            adjusttext=False,
        )
        assert isinstance(skipatom_pca_plot, plt.Axes)
        skipatom_tsne_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="tsne",
            adjusttext=False,
        )
        assert isinstance(skipatom_tsne_plot, plt.Axes)
        skipatom_umap_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="umap",
            adjusttext=True,
        )
        assert isinstance(skipatom_umap_plot, plt.Axes)

        self.assertRaises(
            ValueError,
            dimension_plotter,
            self.test_skipatom,
            n_components=2,
            reducer="badreducer",
        )

    def test_dimension_3d_plotter(self):
        """Test that the dimension_plotter function works in 3D."""
        skipatom_3d_pca_plot = dimension_plotter(
            self.test_skipatom,
            n_components=3,
            reducer="pca",
            adjusttext=False,
        )
        assert isinstance(skipatom_3d_pca_plot, plt.Axes)

    def test_dimension_Nd_plotter(self):
        """Test that the dimension_plotter function will fail in d>3."""
        self.assertRaises(
            ValueError,
            dimension_plotter,
            self.test_skipatom,
            n_components=4,
            reducer="pca",
        )

    def test_kwargs_plotter(self):
        """Test that the dimension_plotter function works with kwargs."""
        pca_params = {"svd_solver": "full", "random_state": 42}
        tsne_params = {"n_iter": 1000, "random_state": 42, "perplexity": 50}
        umap_params = {"n_neighbors": 15, "random_state": 42}
        scatter_params = {"s": 1}
        skipatom_pca_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="pca",
            adjusttext=False,
            reducer_params=pca_params,
            scatter_params=scatter_params,
        )
        assert isinstance(skipatom_pca_plot, plt.Axes)
        skipatom_tsne_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="tsne",
            adjusttext=False,
            scatter_params=scatter_params,
            reducer_params=tsne_params,
        )
        assert isinstance(skipatom_tsne_plot, plt.Axes)
        skipatom_umap_plot = dimension_plotter(
            self.test_skipatom,
            n_components=2,
            reducer="umap",
            adjusttext=False,
            scatter_params=scatter_params,
            reducer_params=umap_params,
        )
        assert isinstance(skipatom_umap_plot, plt.Axes)


if __name__ == "__main__":
    unittest.main()
