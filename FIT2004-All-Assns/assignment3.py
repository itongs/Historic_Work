"""
Assignment 3 file for FIT2004 by Ian Tongs, 2020. Contains all required functions.
When run, produces no independent outputs as is. All complexities are optimal.

@author         Ian Tongs, 27765369
@since          17 May 2020
"""

# Imports:
# Carried over from assignment 1
# import math                         # Not used
# import time                         # Not used
# import random                       # Not used
# import matplotlib.pyplot as plt     # Not used


# Functions and Classes:

########################################################################################################################
# Task 1-4:
########################################################################################################################

class alphabet_nodes:
    """
    Class for a linked array implementation. This is done to make implementation of the questions easier.
    """

    def __init__(self):
        self.dollar = False                 # Indicates if end of string
        self.next_letters = [None] * 26     # Array. Should be obvious what for.
        self.count = 0                      # Counts occurrences of string
        self.prefix_count = 0               # Counts for the number of strings with this as a prefix


class Trie:
    """
    Class for tries, as required in the questions, using linked arrays.
    """

    def __init__(self, text):
        """
        Initialising function for the trie

        @param self                 The trie we are creating
        @param text                 The text (strings list) we are inserting into the trie
        @complexity                 O(T) where T is the total length of the strings in the list combined
        """
        # Initialise the class
        self.root = alphabet_nodes()

        # Call the insert method for each string:
        for stri in text:
            self.insert(stri)

    def insert(self, stri):
        """
        Inserts strings into the trie

        @param self                 The trie we are referencing
        @param stri                 The text individual string we are inserting into the trie
        @complexity                 0(n) where n is the length of the string
        """
        # Start at the origin
        origin = self.root
        origin.prefix_count += 1

        # Iterate through all characters
        i = 0
        while i < len(stri):
            char_num = int(ord(stri[i]) - ord('a'))         # Convert charcter to a 0-25 index number

            # Test if need to add a 'child':
            if origin.next_letters[char_num] == None:
                origin.next_letters[char_num] = alphabet_nodes()

            # Move down
            origin = origin.next_letters[char_num]
            origin.prefix_count += 1

            # Iterate
            i += 1

        # Set end of word equal to true
        origin.dollar = True
        origin.count += 1

    def string_freq(self, query_str):
        """
        Function that gets the number of times a string is in the trie

        @param self                 The trie we are referencing
        @param query_str            The text individual string we are searching for in the trie
        @return origin.count        The number of times a string is in the trie
        @complexity                 0(q) where q is the length of the string
        """
        # Start at the origin
        origin = self.root

        # Iterate through all characters
        i = 0
        while i < len(query_str):
            char_num = int(ord(query_str[i]) - ord('a'))  # Convert charcter to a 0-25 index number

            # Test if a child doesn't exist:
            if origin.next_letters[char_num] == None:
                return 0

            # Move down
            origin = origin.next_letters[char_num]

            # Iterate
            i += 1

        # Return the count at the final point:
        return origin.count

    def prefix_freq(self, query_str):
        """
        Function that gets the number of times a prefix is in the trie

        @param self                     The trie we are referencing
        @param query_str                The text individual prefix we are searching for in the trie
        @return origin.prefix_count     The number of times a prefix is 'in' the referenced trie
        @complexity                     0(q) where q is the length of the prefix
        """
        # Start at the origin
        origin = self.root

        # Iterate through all characters
        i = 0
        while i < len(query_str):
            char_num = int(ord(query_str[i]) - ord('a'))  # Convert charcter to a 0-25 index number

            # Test if appropriate child doesn't exist:
            if origin.next_letters[char_num] == None:
                return 0

            # Move down
            origin = origin.next_letters[char_num]

            # Iterate
            i += 1

        # Return the prefix count at the final point:
        return origin.prefix_count

    def wildcard_prefix_freq(self, query_str):
        """
        Function that gets the list of words in a Trie with a given wildcard prefix

        @param self                 The trie we are referencing
        @param query_str            The text individual prefix we are searching for in the trie
        @return return_list         The list of words in the trie with the wildcard prefix
        @complexity                 0(q + S) where q is the length of the prefix and S is the total characters in all
                                    the found strings.
        """
        # Start at the origin
        origin = self.root

        # Initialise list for strings to return:
        return_list = []

        # Iterate through all characters
        i = 0
        while i < len(query_str):
            if query_str[i] == '?':
                ex_count = 0  # Used to keep track of how many word found

                # For all possible wildcards, test until broken:
                for j in range(0, 26):
                    # Test if need to add a 'child':
                    if origin.next_letters[j] != None:
                        pref_str = query_str[0:i]+chr(j + 97)

                        # Early breaker
                        ex_count += origin.next_letters[j].count

                        # If ? is the last string:
                        if i + 1 == len(query_str):
                            new_origin = origin.next_letters[j]
                            extra_list = self.wildcard_auxiliary(pref_str, new_origin)
                            return_list.extend(extra_list)
                            continue

                        # Iterate for characters after the wildcard if not the last character
                        k = i + 1
                        new_origin = origin.next_letters[j]
                        while k < len(query_str):
                            char_num = int(ord(query_str[k]) - ord('a'))  # Convert charcter to a 0-25 index number

                            # Test if need to add a 'child':
                            if new_origin.next_letters[char_num] == None:
                                break
                            # Move down
                            new_origin = new_origin.next_letters[char_num]
                            pref_str = pref_str + query_str[k]

                            # Iterate
                            k += 1

                            if k == len(query_str):
                                # Call Auxiliary function
                                extra_list = self.wildcard_auxiliary(pref_str, new_origin)

                                # Add auxiliary function to return list
                                return_list.extend(extra_list)

                    # Early breaker if all populated children have been visited
                    if ex_count == origin.prefix_count - origin.count:
                        break

                # All necessary places visited by now
                break
            else:
                char_num = int(ord(query_str[i]) - ord('a'))  # Convert charcter to a 0-25 index number

                # Test if need to add a 'child':
                if origin.next_letters[char_num] == None:
                    return return_list
            # Move down
            origin = origin.next_letters[char_num]

            # Iterate
            i += 1

        # Return the prefix count at the final point:
        return return_list

    def wildcard_auxiliary(self, prefix, prefix_end_node):
        """
        Auxiliary function that gets the list of words in a Trie with a given prefix

        @param self                 The trie we are referencing
        @param prefix               The text individual prefix we are searching for in the trie
        @param prefix_end_node      The node the prefix we are checking starts from
        @return full_strings        The list of strings with the given prefix
        @complexity                 0(q + S') where q is the length of the prefix and S' is the total characters in all
                                    the found strings for this prefix
        """
        full_strings = []
        print(prefix)

        # Add present position if appropriate:
        if prefix_end_node.dollar == True:
            n = prefix_end_node.count
            full_strings += [prefix] * n

        # Return if a terminal node of trie
        if prefix_end_node.count == prefix_end_node.prefix_count:
            return full_strings

        # Definitions:
        breaker = 0

        for i in range(0, 26):
            # Use recursion to add to this list:
            if prefix_end_node.next_letters[i] != None:
                string_copy = prefix + chr(i + 97)
                new_origin = prefix_end_node.next_letters[i]
                extra_list = self.wildcard_auxiliary(string_copy, new_origin)
                full_strings.extend(extra_list)
                breaker += new_origin.prefix_count

            # Breaker if statement
            if breaker == (prefix_end_node.prefix_count - prefix_end_node.count):
                break

        return full_strings





# Basic Tests: (main testing done elsewhere btw, this was just for when I built the function)

# text = ['aa', 'aab', 'aaab', 'abaa', 'aa', 'abba', 'aaba', 'aaa', 'aa', 'aaab', 'abbb', 'baaa', 'baa', 'bba', 'bbab']

# text = [
#             'aa',
#             'aab',
#             'aaab',
#             'abaa',
#             'aa',
#             'abba',
#             'aaba',
#             'aaa',
#             'aa',
#             'aaab',
#             'abbb',
#             'baaa',
#             'baa',
#             'bba',
#             'bbab'
#         ]
#
# test_trie = Trie(text)
#
# tester = test_trie.wildcard_prefix_freq('?b')
# print(tester)

# print(test_trie.prefix_freq("ccc"))
# print(test_trie.prefix_freq("ab"))
# print(test_trie.prefix_freq("aa"))

# print(test_trie.string_freq('aa'))
# print(test_trie.string_freq('aba'))
# print(test_trie.string_freq('ab'))
# print(test_trie.string_freq('b'))


# print(test_trie.root.dollar)
# print(test_trie.root.next_letters)
# print(test_trie.root.next_letters[0].dollar)
# print(test_trie.root.next_letters[0].next_letters)
