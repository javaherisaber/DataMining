"""
=========================================================
Comparing different clustering algorithms on toy datasets
=========================================================

This example aims at showing characteristics of different
clustering algorithms on datasets that are "interesting"
but still in 2D. The last dataset is an example of a 'null'
situation for clustering: the data is homogeneous, and
there is no good clustering.

While these examples give some intuition about the algorithms,
this intuition might not apply to very high dimensional data.

The results could be improved by tweaking the parameters for
each clustering strategy, for instance setting the number of
clusters for the methods that needs this parameter
specified. Note that affinity propagation has a tendency to
create many clusters. Thus in this example its two parameters
(damping and per-point preference) were set to mitigate this
behavior.
"""
#
#   print out above document
print(__doc__)

import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

#
#   Cause random numbers predictable , this means that every time random number going to create
#   it choose the same data which has been created on previous call to np.random.rand method
#   though the same data will appear each time
np.random.seed(0)

# Generate datasets. We choose the size big enough to see the scalability
# of the algorithms, but not too big to avoid too long running times
#
#   Number of instances in each figure
n_samples = 1500
#
#   Create data for 1st row figure
#   figure looks like a hierarchical circles with the same center
#   data comes from Sklearn datasets library
#   Arguments :
#   @n_samples = number of samples to be created
#   @factor = Scale factor between inner and outer circle
#   @noise = Standard deviation of Gaussian noise added to the data
noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5,
                                      noise=.05)
#
#   Create data for 2nd row figure
#   figure looks like two moons which stock together in opposite positions
#   data comes from Sklearn datasets library
#   Arguments :
#   @n_samples = number of samples to be created
#   @noise = Standard deviation of Gaussian noise added to the data
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)
#
#   Create data for 3rd row figure
#   figure looks like some drop of blobs
#   data comes from Sklearn datasets library
#   Arguments :
#   @n_samples = number of samples to be created
#   @random_state = this is the seed number used by the random number generator
blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
#
#   Create data for 4th row figure
#   Create an array of the given shape and propagate it with random samples from a uniform distribution over [0, 1)
#   figure looks like a messed page with some sands which has no structure in it
#   Arguments :
#   @n_samples = number of samples to be created
#   @second argument = define's shape of the data
#   as the output is tuple , "None" at the end of the line is specified for making the second index of our tuple blank
no_structure = np.random.rand(n_samples, 2), None
#
#   Array of color names
colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
#
#   Makes color array larger by 20 point
colors = np.hstack([colors] * 20)

#
#   a list of clustering names which has been used in this code
clustering_names = [
    'MiniBatchKMeans', 'AffinityPropagation', 'MeanShift',
    'SpectralClustering', 'Ward', 'AgglomerativeClustering',
    'DBSCAN', 'Birch']
#
#   Create a plot with a graphical user interface in order to visualize each algorithm
#   Arguments :
#   @figsize = specify figure size in inches
plt.figure(figsize=(len(clustering_names) * 2 + 3, 9.5))
#
#   Tune the subplot layout (within the previous line of code we just created a figure which would have
#   some subplot's inside it)
#   Arguments :
#   @left = the left side of the subplots of the figure
#   @right = the right side of the subplots of the figure
#   @bottom = the bottom of the subplots of the figure
#   @top = the top of the subplots of the figure
#   @wspace = the amount of width reserved for blank space between subplots
#   @hspace = the amount of height reserved for white space between subplots
plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                    hspace=.01)
#
#   Position of plot for each algorithm
#   This variable will be used for detect location of the plot to be illustrated
plot_num = 1
#
#   A list of all datasets which just created in previous lines of code
datasets = [noisy_circles, noisy_moons, blobs, no_structure]
#
#   Iterate in datasets
#   In each iteration one row of the figure will be illustrated
#   Iteration variables :
#   %i_dataset = this variable used to detect first row of figures in order to stick a title above them
#   %dataset = contains a data set to be currently used by each algorithm
for i_dataset, dataset in enumerate(datasets):
    #
    #   Intermediate variable to store our dataset
    X, y = dataset
    #
    #   normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    #
    #   estimate bandwidth for mean shift
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)

    #
    #   connectivity matrix for structured Ward
    connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
    #
    #   This line accumulates connectivity with it's transposed
    #   which makes connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    # create clustering estimators
    #
    #   MeanShift Algorithm
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
    #
    #   two_means Algorithm
    two_means = cluster.MiniBatchKMeans(n_clusters=2)
    #
    #   Agglomerative Algorithm
    ward = cluster.AgglomerativeClustering(n_clusters=2, linkage='ward',
                                           connectivity=connectivity)
    #
    #   Spectral Algorithm
    spectral = cluster.SpectralClustering(n_clusters=2,
                                          eigen_solver='arpack',
                                          affinity="nearest_neighbors")
    #
    #   DBscan Algorithm
    dbscan = cluster.DBSCAN(eps=.2)
    #
    #   Affinity Propagation Algorithm
    affinity_propagation = cluster.AffinityPropagation(damping=.9,
                                                       preference=-200)
    #
    #   Calculate the average linkage
    average_linkage = cluster.AgglomerativeClustering(
        linkage="average", affinity="cityblock", n_clusters=2,
        connectivity=connectivity)
    #
    #   Birch Algorithm
    birch = cluster.Birch(n_clusters=2)
    #
    #   A list of each algorithm result which will be used in inner for loop
    clustering_algorithms = [
        two_means, affinity_propagation, ms, spectral, ward, average_linkage,
        dbscan, birch]
    #
    #   Calculate each algorithm and illustrate in plot graph
    for name, algorithm in zip(clustering_names, clustering_algorithms):
        # predict cluster memberships
        #
        #   Time stamp to determine how much time it takes to do the algorithm
        #   "Start time"
        t0 = time.time()
        #
        #   Doing the algorithm
        algorithm.fit(X)
        #
        #   End of time stamp
        #   in this line we will know about duration of the algorithm
        #   "End time"
        t1 = time.time()
        #
        #   determine if specified algorithm has mentioned attribute or not
        if hasattr(algorithm, 'labels_'):
            #
            #   Predict color schema
            y_pred = algorithm.labels_.astype(np.int)
        else:
            #
            #   Predict color schema
            y_pred = algorithm.predict(X)

        # plot
        #
        #   Create subplot with 4 rows and columns by length of clustering_algorithms variable at position plot_num
        plt.subplot(4, len(clustering_algorithms), plot_num)
        #
        #   if iteration is for first time
        #   we are in first row
        #   then we can stick a title label above the plot
        if i_dataset == 0:
            #
            #   stick a title label above the plot
            #   with title = name and size of 18
            plt.title(name, size=18)
        #
        #   Figure a scatter graph with our data
        #   colorize the points by a prediction variable
        #   first argument = x axis of scatter
        #   second argument = y axis of scatter
        #   s = size of the scatter in points^2
        plt.scatter(X[:, 0], X[:, 1], color=colors[y_pred].tolist(), s=10)
        #
        #   Determine if current algorithm has mentioned attribute or not
        if hasattr(algorithm, 'cluster_centers_'):
            #
            #   Calculate centers
            centers = algorithm.cluster_centers_
            #
            #   Calculate centers color
            center_colors = colors[:len(centers)]
            #
            #   Plot a scatter for centers
            plt.scatter(centers[:, 0], centers[:, 1], s=100, c=center_colors)
        #
        #   Set range of x axis
        plt.xlim(-2, 2)
        #
        #   Set range of y axis
        plt.ylim(-2, 2)
        #
        #   Clear labels of x axis
        plt.xticks(())
        #
        #   Clear labels of y axis
        plt.yticks(())
        #
        #   Write Elapsed time of algorithm onto the plot
        plt.text(.99, .01, ('%.2fs' % (t1 - t0)).lstrip('0'),
                 transform=plt.gca().transAxes, size=15,
                 horizontalalignment='right')
        #
        #   Increase plot_num (This variable was position of plot that is currently in progress)
        plot_num += 1
#
#   Show the plot into graphical user interface
plt.show()
