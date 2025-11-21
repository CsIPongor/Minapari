"""Example: Loading images from files.

Minapari doesn't include built-in file I/O, so you load images
using standard Python libraries and then add them to the viewer.
"""

import numpy as np
from minapari import Viewer


def load_with_pillow():
    """Load image using Pillow (PIL)."""
    from PIL import Image

    # Load image
    img = Image.open('image.png')
    data = np.array(img)

    viewer = Viewer()
    viewer.add_image(data, name='pillow_image')
    viewer.show(block=True)


def load_with_imageio():
    """Load image using imageio."""
    import imageio.v3 as iio

    # Load image
    data = iio.imread('image.png')

    viewer = Viewer()
    viewer.add_image(data, name='imageio_image')
    viewer.show(block=True)


def load_with_tifffile():
    """Load TIFF stack using tifffile."""
    import tifffile

    # Load multi-page TIFF
    data = tifffile.imread('stack.tif')

    viewer = Viewer()
    viewer.add_image(data, name='tiff_stack')
    viewer.show(block=True)


def load_with_scikit_image():
    """Load image using scikit-image."""
    from skimage import io

    # Load image
    data = io.imread('image.png')

    viewer = Viewer()
    viewer.add_image(data, name='skimage_image')
    viewer.show(block=True)


def load_with_opencv():
    """Load image using OpenCV."""
    import cv2

    # Load image (OpenCV loads as BGR)
    data = cv2.imread('image.png')
    # Convert BGR to RGB
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

    viewer = Viewer()
    viewer.add_image(data, name='opencv_image', rgb=True)
    viewer.show(block=True)


def load_zarr_array():
    """Load zarr array (for large datasets)."""
    import zarr

    # Open zarr array (lazy loading)
    data = zarr.open('data.zarr', mode='r')

    viewer = Viewer()
    viewer.add_image(data, name='zarr_array')
    viewer.show(block=True)


def load_numpy_file():
    """Load numpy .npy file."""
    data = np.load('data.npy')

    viewer = Viewer()
    viewer.add_image(data, name='numpy_data')
    viewer.show(block=True)


# Demo with synthetic data
if __name__ == '__main__':
    print("This example shows how to load images from files.")
    print("Since we don't have actual files, here's a demo with synthetic data:")

    # Create synthetic data
    data = np.random.random((256, 256))

    viewer = Viewer(title='Load Image Example')
    viewer.add_image(data, name='synthetic_data', colormap='viridis')
    viewer.show(block=True)
