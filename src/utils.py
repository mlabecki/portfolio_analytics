import numpy as np
import math


def set_axis_limits(
    x_min,
    x_max,
    min_n_intervals = 5,
    max_n_intervals = 15
):
    """
    Returns the lower and upper limits for an axis where x_min and x_max are the min/max values.
    max_n_intervals: maximum number of intervals between y-ticks
    units: increments of values at axis ticks, will be scaled to correspond with the
        order of magntitude of x_max - x_min
    """

    if x_min == x_max:
        return x_min, x_max
    
    else:
        units = np.array([0.05, 0.1, 0.2, 0.25, 0.5])
        # intervals = np.array(range(4, max_n_intervals + 1))

        x_maxmax = max(abs(x_max), abs(x_min))
        diff = 2 * x_maxmax
        x_diff = x_max - x_min
        # order = 10 ** round(math.log10(x_maxmax))
        order = 10 ** round(math.log10(x_diff))
        print(f'order = {order}')
        eps = order * 1e-10

        for unit in units:
            unit_scaled = order * unit
            print(f'unit scaled = {unit_scaled}')

            lower_anchor = 0
            increment = unit_scaled
            while lower_anchor - abs(x_min) < eps:
                lower_anchor += increment
            lower_anchor *= np.sign(x_min)
            if x_min > eps:
                lower_anchor -= increment

            diff_lower = abs(lower_anchor - x_min)
            if diff_lower < eps:
                diff_lower = 0

            print(f'\tlower anchor = {lower_anchor}')
            print(f'\tdiff lower = {diff_lower}')

            upper_anchor = lower_anchor
            while (upper_anchor < x_max) & (abs(upper_anchor - x_max) > eps) & (round((upper_anchor - lower_anchor) / increment) < max_n_intervals):
                upper_anchor += unit_scaled
                # print(f'\tupper anchor = {upper_anchor}')
            diff_upper = abs(upper_anchor - x_max)
            if diff_upper < eps:
                diff_upper = 0
            
            print(f'\tupper anchor = {upper_anchor}')
            print(f'\tdiff upper = {diff_upper}')
            n = round((upper_anchor - lower_anchor) / increment)

            if (upper_anchor - x_max > -eps) & (diff_lower + diff_upper < diff) & (n >= min_n_intervals):
                diff = diff_lower + diff_upper
                lower_limit = lower_anchor
                upper_limit = upper_anchor
                delta = increment
                # n_intervals = n

        # print(f'Number of intervals: {n_intervals}')

        return lower_limit, upper_limit, delta


def old_set_axis_limits(
    x_min,
    x_max,
    max_n_intervals = 15
):
    """
    Returns the lower and upper limits for an axis where x_min and x_max are the min/max values.
    max_n_intervals: maximum number of intervals between y-ticks
    units: increments of values at axis ticks, will be scaled to correspond with the
        order of magntitude of x_max - x_min
    """

    if x_min == x_max:
        return x_min, x_max
    
    else:
        units = np.array([0.05, 0.1, 0.2, 0.25, 0.5])
        # intervals = np.array(range(4, max_n_intervals + 1))

        x_maxmax = max(abs(x_max), abs(x_min))
        diff = 2 * x_maxmax
        order = 10 ** round(math.log10(x_maxmax))
        # print(f'order = {order}')
        eps = order * 1e-10

        for unit in units:
            unit_scaled = order * unit
            # print(f'unit scaled = {unit_scaled}')

            lower_anchor = 0
            increment = unit_scaled
            while lower_anchor - abs(x_min) < eps:
                lower_anchor += increment
            lower_anchor *= np.sign(x_min)
            if x_min > eps:
                lower_anchor -= increment

            diff_lower = abs(lower_anchor - x_min)
            if diff_lower < eps:
                diff_lower = 0

            # print(f'\tlower anchor = {lower_anchor}')
            # print(f'\tdiff lower = {diff_lower}')

            upper_anchor = lower_anchor
            while (upper_anchor < x_max) & (abs(upper_anchor - x_max) > eps) & ((upper_anchor - lower_anchor) / unit_scaled <= max_n_intervals):
                upper_anchor += unit_scaled
                # print(f'\tupper anchor = {upper_anchor}')
            diff_upper = abs(upper_anchor - x_max)
            if diff_upper < eps:
                diff_upper = 0
            
            # print(f'\tupper anchor = {upper_anchor}')
            # print(f'\tdiff upper = {diff_upper}')

            if (upper_anchor - x_max > -eps) & (diff_lower + diff_upper < diff):
                diff = diff_lower + diff_upper
                lower_limit = lower_anchor
                upper_limit = upper_anchor
        
        return lower_limit, upper_limit


def upper_limit(x):
    """
    Returns the upper/lower limit for an axis where x is the maximum/minimum value.
    units: increments of values at axis ticks, will be scaled to correspond with the
        order of magntitude of x
    intervals: how many intervals of units between 0 and upper limit do we want to have
    """

    if x == 0:
        return 0
    
    else:
        units = np.array([0.1, 0.2, 0.25, 0.5])
        intervals = np.array([4, 5, 6, 7, 8, 9, 10])

        order = 10 ** round(math.log10(abs(x)))
        units_scaled = order * units
        candidates = np.outer(intervals, units_scaled)
        winner = np.min(candidates[candidates - abs(x) >= 0])

        print(units)
        print(intervals)
        print(order, units_scaled)
        print(f'upper candidates\n{candidates}')

        return np.sign(x) * winner
    

def lower_limit(x):
    """
    Returns the upper limit in magnitude for an axis where x is the maximum positive 
        or minimum negative value.
    units: increments of values at axis ticks, will be scaled to correspond with the
        order of magntitude of x
    intervals: how many intervals of units between 0 and upper limit do we want to have
    """

    if x == 0:
        return 0
    
    else:
        units = np.array([0.1, 0.2, 0.25, 0.5])
        intervals = np.array([4, 5, 6, 7, 8, 9, 10])

        order = 10 ** round(math.log10(abs(x)))
        units_scaled = order * units
        candidates = np.outer(intervals, units_scaled)
        winner = np.max(candidates[candidates - abs(x) <= 0])

        print(units)
        print(intervals)
        print(order, units_scaled)
        print(f'lower candidates\n{candidates}')
        
        return np.sign(x) * winner
    

def map_values(k_list, v_min, v_max, ascending=False):
    """
    Maps numbers from k_list to proportionally spaced values between v_min and v_max.
    Returns a dictionary of k_list elements as keys and the mapped values.
    k_list:     input list of n numerical elements that will serve as dictionary keys
    v_min:      lower bound of mapped values
    v_max:      upper bound of mapped values
    ascending:  a flag indicating whether the order of elements in k_list is ascending or descending
    """
    dict_map = {}
    k_list = sorted(k_list)
    if ascending:
        k_list.reverse()
    k_first = k_list[0]
    k_last = k_list[len(k_list) - 1]
    dict_map.update({k_first: v_min, k_last: v_max})

    k_range = k_last - k_first
    v_range = v_max - v_min
    kv_scale = v_range / k_range

    for k in k_list[1: -1]:
        k_delta = k - k_first
        v = v_min + k_delta * kv_scale
        dict_map.update({k: v})
    
    return dict_map


def squeeze(char: str, s: str):
    """
    Removes repeated instances of character char from string s
    """
    while char*2 in s:
        s = s.replace(char*2, char)
    return s


def add_spaces_html(n: int):
    """
    Add n non-breaking spaces inline in an html markup
    """
    spaces = ''
    i = 0
    while i < n:
        spaces += '&nbsp;'
        i+=1

    return spaces

