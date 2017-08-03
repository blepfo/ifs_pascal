"""Utilities for studying Pascal's triangle mod m

"""

import logging
import numpy as np

from math import factorial

logger = logging.getLogger('ifs_pascal.utils')


def choose(n, k):
    """Compute the binomial coefficient nCk. Requires n > k.

    Uses the multiplicative formula found at 
    https://en.wikipedia.org/wiki/Binomial_coefficient#Multiplicative_formula

    Args:
        n (int): Positive integer.
        k (int): Positive integer.

    Returns:
        nCk (int): n choose k.

    """
    if n < k:
        raise_value_error("Need n<k but n=%d, k=%d" % (n, k))
    if n < 0:
        raise_value_error("Need n>0 but n=%d" % n)
    if k < 0:
        raise_value_error("Need k>0 but k=%d" %d)

    return int(factorial(n) // (factorial(k) * factorial(n - k)))


def raise_value_error(msg):
    """Raise exception and log the exception.

    Args:
        msg (str): Error message.

    Returns:
        None.

    """
    logger.exception(msg)
    raise ValueError(msg)
