"""Basic usage example for Minapari."""

import numpy as np


def main():
    from minapari import Viewer

    # Create viewer
    viewer = Viewer(title='Minapari Example')

    # Create sample data
    data = np.random.random((512, 512))

    # Add image layer
    viewer.add_image(data, name='random_image', colormap='viridis')

    # Add multi-channel image
    multichannel = np.random.random((3, 256, 256))
    viewer.add_image(
        multichannel,
        name='multichannel',
        channel_axis=0,
        colormap=['red', 'green', 'blue'],
    )

    # Show viewer (blocking)
    viewer.show(block=True)


if __name__ == '__main__':
    main()
