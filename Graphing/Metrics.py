import numpy as np

"""
The following are helper functions that compute various metrics for ONE box.
"""


def comp(T1, T2,start, end, diff_mag):
    """
    Finds indexes where the difference between T1 and T2 is at least alpha

    Inputs:
        T1 - A track 
        T2 - Another track to compare to T1
        alpha - a float s.t. only indices where |T1-T2| >= alpha are considered
        box - a list that contains the start and end points of a box. 
    
    Outputs:
        diff_locs - an np array containing all indices of differences above the alpha threshold according to the given box_starts and alphas 
    """
    Difference = np.absolute(np.subtract(T1, T2))
    diff_locs = np.where(Difference[start:end] >= diff_mag)[0] + start
    return diff_locs



def clust(diff_locs, neigbour_dist):
    """
    Clusters indices where differences occur based on their proximity to each other

    Inputs:
        diff_locs - a list of np arrays containing all indices of differences above the alpha threshold, see compare fxn.
        betas -  list of maximum distance apart two indices of difference can be while still considered in the same cluster

    Outputs:
        clusters - list of clusters. Each entry list follows the following format: [x,y]. Where
            x is the starting index of the cluster (inclusive)
            y is the ending index of the cluster (inclusive)
    """
    clusters = []

    #take care of empty case.
    if len(diff_locs) == 0:
        return []
    else:
        current_cluster = [diff_locs[0], diff_locs[0]]

    for j in diff_locs:
        if (j - current_cluster[1]) > neigbour_dist:
            clusters.append(current_cluster)
            current_cluster = [j,j]
        else:
            current_cluster[1] = j

    clusters.append(current_cluster)
    return clusters
 


def elim(clusters, hood_size):
    """
    Eliminates clusters of size < gamma
    
    Inputs:
        clusters - list of clusters. Each entry list follows the following format: [i1,i2,...ij]. Where
            i1 is the starting index of the cluster
            ij is the ending index of the cluster

        gamma - the minimum number of indices a cluster must span to be kept.

    Outputs:
        kept - a updated list of the clusters input, where only clusters larger than size gamma remain.

    """
    kept = []
    for j in clusters:
        if abs(j[1] - j[0] + 1) >= hood_size:
            kept.append(j)
    return kept
