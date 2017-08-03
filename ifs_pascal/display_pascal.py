"""Create images of Pascal's triangle modulo m

"""

import logging
import numpy as np
from matplotlib import pyplot as plt

from .utils import choose
from .utils import raise_value_error

logger = logging.getLogger('ifs_pascal.display_pascal')


def display_pascal(modulus=2, 
                   n_rows=128,
                   scale=2, 
                   mode="binary", 
                   display=True,
                   colormap='inferno'):
    """Display image of Pascal's triangle modulo m

    This works best when the size parameter is an integer power of the modulus.

    Args:
        modulus (int): Image creates is Pascal's triangle modulo this number.
        n_rows (int): Number of rows of Pascal's triangle to draw.
        scale (int): Must be an even number. Each number of the triangle takes 
            up a square of (scale) x (scale) pixels. Image size will be 
            (n_rows*scale) x (n_rows*scale).
        mode (str): Must be either "binary" or "continuous"
            "binary" mode has two colors; one for numbers congruent to 0 mod m
            and another for numbers that are nonzero mod m
            "continuous" mode colors each congruence class differently.
        display (bool): If True, display the image using matplotlib.pyplot.
        colormap (str): Colormap for the image. For a list of options, see 
            http://matplotlib.org/examples/color/colormaps_reference.html

    Returns:
        image (np.ndarray): Square image of Pascal's triangle modulo m.

    """
    if (scale % 2) != 0:
        raise_value_error('Scale must be an even number, but it was %d' % scale)
    # Create the image
    image_size = scale * n_rows

    logger.debug("Creating image of Pascal's triangle mod %d of size " \
                 "%d." % (modulus, image_size))

    image = np.zeros((image_size, image_size))
    for n in range(0, n_rows + 1):
        row_start = scale * n
        # nth row of Pascal's triangle is nCk for k = 0, 1, ..., n
        for k in range(0, n + 1):
            num = choose(n, k)
            color = num % modulus
            if mode == "binary":
                # Only two colors in binary mode
                color = (color != 0)
            # Calculate where in the image the current entry should be
            left_end = \
                (image_size // 2) - ((scale // 2) * (n + 1)) + (scale * k)
            # Fill square of pixels with color for current entry
            image[row_start : row_start + scale, \
                  left_end : left_end + scale] = color
    
    # Display the image
    if display:
        logger.debug('Displaying image.')

        plt.imshow(image)
        plt.axis('off')
        plt.set_cmap(colormap)
        plt.colorbar()
        plt.show()
    else:
        logger.debug('Image will not be displayed.')

    return image
