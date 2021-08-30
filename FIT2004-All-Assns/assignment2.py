"""
Assignment 2 file for FIT2004 by Ian Tongs, 2020. Contains all required functions.
When run, produces no independent outputs as is. All complexities are optimal.

@author         Ian Tongs, 27765369
@since          26 April 2020
"""

# Imports:
# Carried over from assignment 1
# import math                         # Not used
# # It was mentioned by Nathan in the forums it was fine to import this
# import time                         # Not used
# import random                       # Not used
# import matplotlib.pyplot as plt     # Not used


# Functions:

########################################################################################################################
# Task 1
########################################################################################################################


def longest_oscillation(L):
    """
    Function that finds the longest oscillation

    @param L                The list we wish to get the longest oscillation from
    @return long_osc        The length of the longest oscillation
    @return osc_index_list  List of the longest oscillation
    @complexity             For an input 'L' of size n, this function has O(n) time complexity as the list is only
                            looped over once, and O(n) auxiliary space complexity as two lists of size n are made in
                            the function (one for the indices, the other for the associated index values)
    """
    osc_list = []
    osc_index_list = []
    if L == []:
        return (0, [])
    for i in range(len(L)):
        if osc_list == []:
            osc_list = [L[i]]
            osc_index_list = [i]
        elif osc_list[-1] == L[i]:
            continue
        elif len(osc_list) == 1:
            osc_list.append(L[i])
            osc_index_list.append(i)
        elif (L[i] - osc_list[-1]) * (osc_list[-1] - osc_list[-2]) < 0:
            osc_list.append(L[i])
            osc_index_list.append(i)
        else:
            osc_list[-1] = L[i]
            osc_index_list[-1] = i
    long_osc = len(osc_index_list)
    return (long_osc, osc_index_list)


# Basic Testing:
#llist = [3, 2, 1]
#ret = longest_oscillation(llist)
#print(ret[0])
#print(ret[1])


########################################################################################################################
# Task 2
########################################################################################################################


def longest_walk(M):
    """
    Function that finds the longest oscillation

    @param M            The Matrix we wish to get the longest walk from
    @return long_walk   The length of the longest walk
    @return walk_list   List of the path of the longest walk
    @complexity         Time: O(NM) where N and M are the dimensions of the matrix M
                        Space: O(NM), with the same dimensions
    """
    if M == [[]] or M == []:
        return (0, [])
    long_walk = -1

    # Terminating point of the walk
    starting_point = [-1, -1]

    # Array of max walks to each point in the matrix
    path_lengths = [[-1 for _ in range(len(M[0]))] for _ in range(len(M))]

    # Loop for longest path and starting location - O(NM) time (worst case of 2NM time roughly, once O(NM) in the inner
    # most loop, the rest O(1) for a total of O(2NM) = 0(NM)
    for i in range(len(M)):
        for j in range(len(M[0])):
            if (path_lengths[i][j] == -1):   # Only call aux function if the max length is unassigned - up to O(NM) once
                longest_path_auxiliary(i, j, M, path_lengths)
            if path_lengths[i][j] > long_walk:      # Set as max if max
                long_walk = path_lengths[i][j]
                starting_point = [i, j]

    # Call function for longest path - worst-case of O(NM) time if it has to recurse through all positions
    walk_list = pathfinder_auxiliary(starting_point[0], starting_point[1], M)

    # Return the given values
    return (long_walk, walk_list)


def longest_path_auxiliary(row, col, M, path_lengths):
    """
    Auxiliary function that recursively finds the maximum path from the called location

    @param row          The row index in the matrix of where to find the longest path
    @param col          The column index in the matrix of where to find the longest path to
    @param M            The Matrix, as an array
    @param path_lengths The array of lengths to each given index
    @return             The value of the max length at the given index
    @complexity         Time: Worst-case: O(NM) where N and M are the dimensions of the matrix M (and also path_lengths)
                        Space: O(1) as only 9 new items created
    """
    # Check in array
    if row < 0 or row >= len(M) or col < 0 or col >= len(M[0]):
        return 0

    # Check path lengths unassigned
    if path_lengths[row][col] != -1:
        return path_lengths[row][col]

    # Define variables
    pa, pb, pc, pd, pe, pf, pg, ph = -1, -1, -1, -1, -1, -1, -1, -1
    maxlen = 1

    ### Straight horizontal or vertical:

    # Across 1:
    if col < len(M[0]) - 1 and (M[row][col] < M[row][col + 1]):         # If across value exists and is less:
        pa = 1 + longest_path_auxiliary(row, col + 1, M, path_lengths)  # add 1 to the value to there
    if pa > maxlen:                                                     # If this is longer than the max, set max
        maxlen = pa

    # Across -1:
    if col > 0 and (M[row][col] < M[row][col - 1]):
        pb = 1 + longest_path_auxiliary(row, col - 1, M, path_lengths)
    if pb > maxlen:
        maxlen = pb

    # Down 1:
    if row < len(M) - 1 and (M[row][col] < M[row + 1][col]):
        pc = 1 + longest_path_auxiliary(row + 1, col, M, path_lengths)
    if pc > maxlen:
        maxlen = pc

    # Down -1:
    if row > 0 and (M[row][col] < M[row - 1][col]):
        pd = 1 + longest_path_auxiliary(row - 1, col, M, path_lengths)
    if pd > maxlen:
        maxlen = pd


    ### Diagonals

    # Across 1 Down 1:
    if col < len(M[0]) - 1 and row < len(M) - 1 and (M[row][col] < M[row + 1][col + 1]):
        pe = 1 + longest_path_auxiliary(row + 1, col + 1, M, path_lengths)
    if pe > maxlen:
        maxlen = pe

    # Across -1 Down 1:
    if col > 0 and row < len(M) - 1 and (M[row][col] < M[row + 1][col - 1]):
        pf = 1 + longest_path_auxiliary(row + 1, col - 1, M, path_lengths)
    if pf > maxlen:
        maxlen = pf

    # Across 1 Down -1:
    if col < len(M[0]) - 1 and row > 0 and (M[row][col] < M[row - 1][col + 1]):
        pg = 1 + longest_path_auxiliary(row - 1, col + 1, M, path_lengths)
    if pg > maxlen:
        maxlen = pg

    # Across -1 Down -1:
    if col > 0 and row > 0 and (M[row][col] < M[row - 1][col - 1]):
        ph = 1 + longest_path_auxiliary(row - 1, col - 1, M, path_lengths)
    if ph > maxlen:
        maxlen = ph

    # Set value to the mnax length
    path_lengths[row][col] = maxlen

    return path_lengths[row][col]


def pathfinder_auxiliary(row, col, M):
    """
    Find the maximum path from the longest path's location

    @param row          The row index in the matrix of where to find the longest path
    @param col          The column index in the matrix of where to find the longest path to
    @param M            The Matrix, as an array
    @return maxpath     The path taken as a list of tuples
    @complexity         Time: Worst-case - O(NM) where N and M are the dimensions of the matrix M
                        Space: Worst - case - O(NM) (all points in M visited)
    """
    # Initialise the two lists
    pc = []
    maxpath = []

    ### Straight horizontal or vertical:

    # Across 1:
    if col < len(M[0]) - 1 and (M[row][col] < M[row][col + 1]):
        pc = pathfinder_auxiliary(row, col + 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Across -1:
    if col > 0 and (M[row][col] < M[row][col - 1]):
        pc = pathfinder_auxiliary(row, col - 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Down 1:
    if row < len(M) - 1 and (M[row][col] < M[row + 1][col]):
        pc = pathfinder_auxiliary(row + 1, col, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Down -1:
    if row > 0 and (M[row][col] < M[row - 1][col]):
        pc = pathfinder_auxiliary(row - 1, col, M)
    if len(pc) > len(maxpath):
        maxpath = pc


    ### Diagonals

    # Across 1 Down 1:
    if col < len(M[0]) - 1 and row < len(M) - 1 and (M[row][col] < M[row + 1][col + 1]):
        pc = pathfinder_auxiliary(row + 1, col + 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Across -1 Down 1:
    if col > 0 and row < len(M) - 1 and (M[row][col] < M[row + 1][col - 1]):
        pc = pathfinder_auxiliary(row + 1, col - 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Across 1 Down -1:
    if col < len(M[0]) - 1 and row > 0 and (M[row][col] < M[row - 1][col + 1]):
        pc = pathfinder_auxiliary(row - 1, col + 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Across -1 Down -1:
    if col > 0 and row > 0 and (M[row][col] < M[row - 1][col - 1]):
        pc = pathfinder_auxiliary(row - 1, col - 1, M)
    if len(pc) > len(maxpath):
        maxpath = pc

    # Add self to max path (this can also be called the base case in this context)
    maxpath = [(row, col)] + maxpath
    return maxpath

# Basic Tests: (main testing done elsewhere btw, this was just for when I built the function
# mmatrix = [[1]]
# rresult = longest_walk(mmatrix)
# print(rresult)



