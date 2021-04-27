import numpy as np


def _scale_range(input_, min_, max_):
    input_ += -(np.min(input_))
    input_ /= np.max(input_) / (max_ - min_)
    input_ += min_
    return input_


def _sub_psi(e_perc, a_perc):
    '''Calculate the actual PSI value from comparing the values.
        Update the actual value to a very small number if equal to zero
    '''
    if a_perc == 0:
        a_perc = 0.0001
    if e_perc == 0:
        e_perc = 0.0001

    value = (e_perc - a_perc) * np.log(e_perc / a_perc)
    return(value)


def _psi(expected_array, actual_array, buckets, buckettype='bins'):
    '''Calculate the PSI for a single variable
    Args:
        expected_array: numpy array of original values
        actual_array: numpy array of new values, same size as expected
        buckets: number of percentile ranges to bucket the values into
    Returns:
        psi_value: calculated PSI value
    '''
    breakpoints = np.arange(0, buckets + 1) / (buckets) * 100

    if buckettype == 'bins':
        breakpoints = _scale_range(breakpoints,
                                   np.min(expected_array),
                                   np.max(expected_array))
    elif buckettype == 'quantiles':
        breakpoints = np.stack([np.percentile(expected_array, b) for b in breakpoints])

    expected_percents = np.histogram(expected_array,
                                     breakpoints)[0] / len(expected_array)
    actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)

    psi_value = np.sum(_sub_psi(
        expected_percents[i], actual_percents[i])
        for i in range(0, len(expected_percents)))
    return(psi_value)


def _calculate_psi(expected, actual, buckettype='bins', buckets=10, axis=0):
    '''Calculate the PSI (population stability index) across all variables
    Args:
       expected: numpy matrix of original values
       actual: numpy matrix of new values, same size as expected
       buckettype: type of strategy for creating buckets, bins splits
       into even splits, quantiles splits into quantile buckets
       buckets: number of quantiles to use in bucketing variables
       axis: axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       psi_values: ndarray of psi values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    '''

    if len(expected.shape) == 1:
        psi_values = np.empty(len(expected.shape))
    else:
        psi_values = np.empty(expected.shape[axis])

    for i in range(0, len(psi_values)):
        if len(psi_values) == 1:
            psi_values = _psi(expected,
                              actual,
                              buckets,
                              buckettype=buckettype)
        elif axis == 0:
            psi_values[i] = _psi(expected[:, i],
                                 actual[:, i],
                                 buckets,
                                 buckettype=buckettype)
        elif axis == 1:
            psi_values[i] = _psi(expected[i, :],
                                 actual[i, :],
                                 buckets,
                                 buckettype=buckettype)

    return(psi_values)
