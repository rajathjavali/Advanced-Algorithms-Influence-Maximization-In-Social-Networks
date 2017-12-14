#!/usr/local/bin/python3.6
import  InfluenceUtility as influence
import pickle
import random

def heuristic1 (graph_snaps, nodes_set, k, step_size, threshold) :
    load_influence_map_from_file = 0
    # graph_snaps: graph snapshots
    # nodes_set: set of nodes in the complete graph
    # k: number of nodes to influence initially
    # step_size: number of nodes to add to the opt set every iteration

    bestNodes = set();

    if not load_influence_map_from_file :
        influenceMap = getInfluenceMap(nodes_set,graph_snaps,threshold);
        f = open ("influenceMapObject.pickle", "wb")
        pickle.dump (influenceMap, f)
        f.close ()
    else :
        f = open ("influenceMapObject.pickle", "rb")
        influenceMap = pickle.load (f)

    uninfluencedNodes = nodes_set;
    for i in range(k):
        maxLength = 0;
        maxNode = 0;

        for uninfluenced_node in uninfluencedNodes:

            new_nodes_influenced = len(set.intersection(influenceMap[uninfluenced_node], uninfluencedNodes));
            if maxLength < new_nodes_influenced:
                maxLength = new_nodes_influenced;
                maxNode = uninfluenced_node;

        # print ("best nodes before", len(bestNodes))
        bestNodes = set.union(influenceMap[maxNode],bestNodes);
        print ("best nodes after", len(bestNodes))
        print ("maxLength intersection", maxLength)
        print ("maxLength before intersection", len(influenceMap[maxNode]))
        bestNodes.add(maxNode);
        uninfluencedNodes.remove(maxNode);
        uninfluencedNodes = uninfluencedNodes.difference(influenceMap[maxNode]);
        # print ("uninfluenced nodes", len(uninfluencedNodes))

    return  bestNodes;

def getInfluenceMap(nodes_set,graph_snapshots, threshold) :
    influencedMap = {};
    for node in nodes_set:
        node_set = set();
        node_set.add(node);
        influencedMap[node] = influence.find_influence(node_set,graph_snapshots,threshold);
    return influencedMap;





    # find the influence of each vertex
    # create a dict vert_influence with key as node and value as the set of nodes influenced by node 
    # best_node = node with the largest influence
    # best_set = set(best_node)
    # uninfluenced_set = nodes_set

    # repeat k times
    #   uninfluenced_set = uninfluenced_set - influence set of best node
    #   for every node in uninfluenced set
    #     num_new_influences = len(influence set of node from the dict created earlier    intersection     uninfluenced set)
    #   find best_node - the node which produces maximum num_new_influences
    #   add best_node to best_set
    # return best_set

def random_heuristic (graph_snaps, nodes_set, k, step_size, threshold) :
    size_of_inf_set = []
    for _ in range (10) :
        # Pick k nodes at random from nodes_set and add it to best nodes
        best_nodes = set ([])
        for _ in range (k) :
            best_nodes.add(random.sample(nodes_set, 1)[0])
        size_of_inf_set.append(len(influence.find_influence (best_nodes, graph_snaps, threshold)))
    avg_size_of_inf_set = sum(size_of_inf_set) / 10.0

    return avg_size_of_inf_set
