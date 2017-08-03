"""Apply an iterated function system to an arbitrary image.

"""

from PIL import Image
from matplotlib import pyplot as plt
from math import sqrt
from math import cos
from math import sin
from math import pi
import logging

from .utils import raise_value_error

logger = logging.getLogger('ifs_pascal.Image_IFS')

DEFAULT_SIZE = 512


class Image_IFS(object):
    """Applies an iterated function system to a seed image

    The default seed image is a white square. 
    
    IFS transformations can be added manually using add_function(). 
    Alternatively, parametrized IFS can be loaded using 
    n_sierpinski() or polygon_ifs()

    Attributes:
        seed_image (PIL.Image): Image to be iterated under the IFS.
        image_size (int): Size of the output image.
        center_origin (bool): Controls if origin is at bottom left of image
            or in the center.
        functions (iterable of iterable of int): Each function is represented
            as a 2-tuple (scaling factor (x_offset, y_offset)).
        image (PIL.Image): Output image that the IFS has been applied to.

    """

    def __init__(self, 
                 seed_image=None, 
                 image_size=DEFAULT_SIZE, 
                 center_origin=False):
        """Constructor.

        Args:
            seed_image (PIL.Image): Image to be iterated under the IFS.
            image_size (int): Size of the output image.
            center_origin (bool): Controls if origin is at bottom left of image
                or in the center.

        Returns:
            image_ifs (Image_IFS): Constructed Image_IFS object.

        """
        logger.debug('Creating new Image_IFS')

        if seed_image == None:
            # Use default seed image
            logger.debug('Using default seed image')
            seed_image = _default_seed(image_size)
        else:
            # Resize given seed image
            seed_image = seed_image.resize((image_size, image_size))
        self.seed_image = seed_image

        self.image = self.seed_image

        self.image_size = image_size
        self.center_origin = center_origin
        self.functions = []


    def add_function(self, scale, translation):
        """Add function to the IFS.

        Args:
            scale (int): Positive integer scaling factor.
            transformation (tuple of int): 2-tuple (x-offset, y-offset)

        Returns: 
            None.

        """
        self.functions.append((scale, translation))


    def iterate(self, n_iterations, first_call=True):
        """Apply the IFS to the current image and save to self.image.

        To display the resulting image, use display_image()

        Args:
            n_iterations (int): Number of times to apply the IFS.
            first_call (bool): If this is the first time iterate is called,
                image needs to be flipped so origin is at bottom left,

        Returns:
            None.

        """
        image_size = self.image_size
        size_tuple = (image_size, image_size)

        if (n_iterations > 0):
            center_origin = self.center_origin

            if first_call:
                # If this is the first iteration, flip the image
                start_image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                start_image = self.image

            # Create new transparent base image to put transformed copies on
            new_image = Image.new('RGBA', size_tuple, (0,) * 4)

            # Apply each contraction in the IFS and combine results
            for contraction in self.functions:
                scale = int(contraction[0] * image_size)
                current_image = start_image.resize((scale, scale))

                # Optionally move origin to center
                x_offset = scale if center_origin else 0
                y_offset = scale if center_origin else 0

                # Apply translation
                x_offset += int(contraction[1][0] * image_size)
                y_offset += int(contraction[1][1] * image_size)

                # In order to have transparency mask so corners of the image 
                # Don't cover parts of the attractor, we paste scaled image 
                # onto a full size transparency and then paste that onto
                # the actual image
                transparency = Image.new('RGBA', size_tuple, (0,) * 4)
                transparency.paste(current_image, (x_offset, y_offset))
                new_image.paste(transparency, mask=transparency)

            self.image = new_image

            # Recursively apply IFS for desired number of iterations
            self.iterate(n_iterations - 1, first_call=False)
        elif (n_iterations == 0 and first_call == False):
            # Last iteration
            # Fill in transparency with black
            background = Image.new('RGBA', size_tuple, (0, 0, 0, 255))
            background.paste(self.image, mask=self.image)

            # Un-flip vertical axis
            background = background.transpose(Image.FLIP_TOP_BOTTOM)
            self.image = background


    def display_image(self):
        """Display current image using pyplot.

        Returns:
            None.

        """
        plt.imshow(self.image)
        plt.axis('off')
        plt.show()


def n_sierpinski(seed_image=None, image_size=512, n=2):
    """Create an Image_IFS object for an n-row Sierpinski gasket.

    Args:
        seed_image (PIL.Image): Image to be iterated under the IFS.
        image_size (int): Size of the output image.
        n (int): Number of rows in each basic structure of the triangle.

    Returns:
        n_sierpinski (Image_IFS): Image_IFS object with IFS for n-row 
            Sierpinski gasket.

    """
    logging.debug('Creating n_sierpinski Image_IFS')

    n_sierpinski = Image_IFS(seed_image=seed_image,
                             image_size=image_size,
                             center_origin=False)
    scale = 1 / n
    # Precompute 2n, sqrt(3), and i*sqrt(3) for efficiency
    n2 = 2 * n
    sqrt3 = sqrt(3)
    for i in range(0, n):
        isqrt3 = i * sqrt3
        for j in range(0, n - i):
            x_offset = (i + (2 * j)) / n2 
            y_offset = isqrt3 / n2 
            n_sierpinski.add_function(scale, (x_offset, y_offset))
    
    return n_sierpinski


def polygon_ifs(seed_image=None, 
                image_size=512, 
                n_vertices=6, 
                include_center=False):
    """Create an Image_IFS with IFS based on vertices of a regular polygon.

    Args:
        seed_image (PIL.Image): Image to be iterated under the IFS.
        image_size (int): Size of the output image.
        n_vertices (int): Number of vertices for the polygon IFS.
        include_center (bool): Controls whether or not a transformation is
            added to the IFS for the center of the polygon.

    Returns:
        polygon_ifs (Image_IFS): Image_IFS object with IFS for regular
            polygon.

    """
    logging.debug('Creating polygon_ifs with %d vertices' % n_vertices)

    polygon_ifs = Image_IFS(seed_image=seed_image,
                            image_size=image_size,
                            center_origin=True)

    scale = 2 / n_vertices
    # omega = (2*pi) / n_vertices
    omega = pi * scale
    for k in range(0, n_vertices):
        polygon_ifs.add_function(scale, 
                            (scale * cos(omega * k), scale * sin(omega * k)))
    if include_center:
        polygon_ifs.add_function(scale, (0, 0))

    return polygon_ifs


def _default_seed(image_size):
    """Create image of white square.

    Args:
        image_size (int): Size of the image.

    Returns:
        image (PIL.Image): Image of all white pixels. 

    """
    return Image.new("RGBA", (image_size, image_size), (255,) * 4)
