"""
Assignment 1 file for FIT2004 by Ian Tongs, 2020. Contains all required functions.
When run, produces no independent outputs as is.

@author         Ian Tongs, 27765369
@since          4 April 2020
"""

# Imports:

import math
# It was mentioned by Nathan in the forums it was fine to import this
import time
# For use timing question 2
import random
import matplotlib.pyplot as plt


# Functions:

########################################################################################################################
# Task 1
########################################################################################################################


def max_ditigs_in_array_in_base(A, base):
    """
    Function to get the maximum number of digits from an integer input in a given base

    @param A        The list we wish to get the max digits of
    @param base     The base in which the # of digits is calculated
    @return dig     The number of digits
    @complexity     O(N) where N is the number of integers in A
    """
    dig = (math.floor(math.log(max(A)) /math.log(base)) + 1)        # + 1 for the 0th digit
    return dig


def get_digit_at_pos(num, base, pos):
    """
    Gets the integer at the given position of the number in a specific base

    @param num      The number we wish to find the converted digit in
    @param base     The base in which the digit is calculated
    @param pos      The position of the digit to be found
    @return         The integer at that digit
    @complexity     O(1)
    """
    return (num // base ** pos) % base


def make_position(A):
    """
    Converts the count array into a position array as part of the count sort

    @param A        the array being converted
    @return A       the now converted array
    @complexity     O(M) where M is the length of A (aka the base called in radix sort
    """
    for j in range(1, len(A)):
        A[j] = A[j] + A[j-1]
    return A


def radix_sort(num_list, b):
    """
    Performs radix sort on the list l with base b

    @param num_list   The list we wish to sort
    @param b          The base we wish to use to sort
    @return output    The sorted list
    @complexity       O((N + b)M) where N is the size of the list, b is the base, and M the max integer length in base b
    """
    base = b
    if num_list == []:                                          # Return empty list for empty list input
        return []
    max_digits = int(max_ditigs_in_array_in_base(num_list, base))      # Max digits of a number in the base given
    output = [0] * len(num_list)                                # Create an output list

    for pos in range(max_digits):                               # Loop for all digit positions, right to left

        count = [0] * base                                      # Count array for stable counting sort

        for i in num_list:                                      # Loop for the count array for each digit
            digit = get_digit_at_pos(i, base, pos)
            count[digit] += 1                                   # Update count for what each element gives

        count = make_position(count)                            # Make the count matrix the position matrix

        for i in reversed(num_list):                            # Update positions in the array based on count sort
                                                                # List reversed for ease of implementation
            digit = get_digit_at_pos(i, base, pos)
            count[digit] -= 1
            new_pos = count[digit]
            output[new_pos] = i                                 # Update position

        num_list = list(output)                                 # Re-point num_list for next loop

    return output


########################################################################################################################
# Task 2
########################################################################################################################


def time_radix_sort():
    """
    Performs radix sort on the list l with base b

    @return output    The sorted list
    @complexity       O((N + b)M) where N is the size of the list, b is the base, and M the max integer length in base b
    """
    test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]

    output = []

    for i in range(1, 21):
        j = 2 ** i
        start = time.time()
        radix_sort(test_data, j)
        end = time.time()

        taken = end - start

        output = output + [(j, taken)]

    return output


# data = time_radix_sort()
#
# x_val = [x[0] for x in data]
# y_val = [x[1] for x in data]
# plt.plot(x_val, y_val)
# plt.plot(x_val, y_val, 'or')
# plt.xlabel('Selected Bases - powers of 2 from 1 to 20')
# plt.ylabel('Time Taken for Radix Sort')
# plt.title('Task 2 Graph')
# plt.grid(True)
# plt.show()


########################################################################################################################
# Task 3
########################################################################################################################


def find_rotations(string_list, p):
    """
    Finds the strings in a list of strings that have their 'p' rotation in that list

    @param string_list      The list of strings to be checked/rotated
    @param p                The number of rotations to check for
    @return result_list     The list of strings whose p-rotations are present
    @complexity             O(NM) as this function is the 'sum' of O(NM) functions
                            NB: for radix sort: as b = 26, the complexity becomes O(NM).
    """
    result_list = []
    result_num_list = []
    if string_list == []:           # Empty list
        return result_list
    if string_list == ['']:         # List with only an empty string
        return ['']

    # Get rotations list: (O(NM))
    rotation_string = do_rotations(string_list, p)

    # Make a num list for base (O(NM))
    base_num = convert_to_numbers(string_list)

    # Make num list for rotations (O(NM))
    rot_num = convert_to_numbers(rotation_string)

    # Append the num lists together (O(2N))
    combined_num_list = base_num + rot_num

    # Order the combined num list (base of 16 as that works well usually) (O(NM + 16M))
    ordered_combined_num_list = radix_sort(combined_num_list, 16)

    # Walk down the ordered num list, and if the numbers of two consecutive number agree, 'return' that number (O(2NM))
    for i in range(1, len(ordered_combined_num_list)):
        current = ordered_combined_num_list[i]
        previous = ordered_combined_num_list[i-1]
        if current == previous:
            result_num_list.append(current)

    # Get the string for each return number (O(NM))
    for i in range(len(result_num_list)):
        string_1 = convert_to_string(result_num_list[i])
        result_list.append(string_1)

    # Re-rotate the return list so it works properly: (O(NM))
    result_list = do_rotations(result_list, -p)

    # Add empty strings if in put to output:
    for i in range(len(string_list)):
        if string_list[i] == '':
            result_list = [''] + result_list

    return result_list


def do_rotations(string_list, p):
    """
    Rotates a list of strings by the given number

    @param string_list      The list of strings to be rotated
    @param p                The integer of the number and 'direction' or rotation
    @return string_list_1   The rotated List
    @complexity             O(NM) where N is the length of the list and M the maximum number of letters in a string
    """
    string_list_1 = ['a'] * len(string_list)
    if p == 0:
        return string_list
    elif p > 0:                         # Left rotations
        for i in range(len(string_list)):
            if string_list[i] != '':
                rot = p % len(string_list[i])
                string_list_1[i] = string_list[i][rot:] + string_list[i][0:rot]
        return string_list_1
    elif p < 0:                         # Right rotations
        for i in range(len(string_list)):
            if string_list[i] != '':
                rot = p % len(string_list[i])
                string_list_1[i] = string_list[i][rot:] + string_list[i][0:rot]
        return string_list_1



def convert_to_numbers(string_list):
    """
    Converts each string to a number as if it were a base 27 number

    @param string_list      The list of strings to convert
    @return num_list        The numbers corresponding to each string
    @complexity             O(NM) where N is the length of the list and M the maximum number of letters in a string
    """
    num_list = [0] * len(string_list)
    for i in range(len(string_list)):           # Loop for each string
        word = string_list[i]
        num = 0
        for j in range(len(word)):              # For each character in each string
            mult = ord(word[-1-j]) % 32
            num = (26**j)*mult + num
        num_list[i] = num
    return num_list


# def convert_to_number(string_a):
#     """
#     Converts a string to a number as if it were a base 26 number
#
#     @param string_a         The string to convert
#     @return num             The number corresponding to the string
#     @complexity             O(M) where M the length of the string
#     """
#     num = 0
#     for j in range(len(string_a)):
#         mult = ord(string_a[-1-j]) % 32
#         num = (26**j)*mult + num
#     return num


def convert_to_string(num):
    """
    Converts a base 27 number back into a string

    @param num                  The number we wish to convert
    @return converted_string    The string of that number
    @complexity                 O(M) where M the length of the string
    """
    converted_string = ""
    while num > 0:                                      # Loop for converting back from number to string, backward:
        converted_string += (chr(97 + (num - 1) % 26))
        num -= 1
        num //= 26
    converted_string = converted_string[::-1]           # Flip the order for return purposes
    return converted_string


#string_list = ["aaa", "abc", "cab", "acb", "wxyz", "yzwx"]
#p = 0
#res = find_rotations(string_list, p)
#print(res)


