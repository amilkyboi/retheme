# module main
'''
A simple Python script that rethemes images.
'''

from PIL import Image
import numpy as np

COLORS = np.array([[22,  22,  29,  255], [30,  31,  40,  255], [42,  42,  55,  255],
                   [54,  54,  70,  255], [84,  84,  109, 255], [220, 215, 186, 255],
                   [34,  50,  73,  255], [45,  79,  103, 255], [147, 138, 169, 255],
                   [149, 127, 184, 255], [126, 156, 216, 255], [122, 168, 159, 255],
                   [210, 126, 153, 255], [232, 36,  36,  255], [127, 180, 202, 255],
                   [152, 187, 108, 255], [228, 104, 118, 255], [255, 160, 102, 255],
                   [106, 149, 137, 255], [230, 195, 132, 255], [192, 163, 110, 255],
                   [255, 93,  98,  255], [156, 171, 202, 255], [101, 133, 148, 255]])

def process(file_name: str) -> Image.Image:
    '''
    Process image data and return the themed image.

    Args:
        file_name (str): path to original image

    Returns:
        Image.Image: new image object
    '''

    with Image.open(f'../img/{file_name}') as img:
        # crude handling of palettised images
        if img.mode == 'P':
            img = img.convert('RGB')

        # 3d array: row, col, rgba
        pixels = np.array(img)

    # remove the alpha channel from the theme colors if the file format doesn't support it
    if img.mode == 'RGB':
        colors = COLORS[:, :3]
    else:
        colors = COLORS

    # numpy black magic: adds an extra dimension to each column before the rgba arrays that
    # correspond to each pixel; basically needed so we can compare the 2d array of theme colors to
    # each pixel

    # if the pixels were left as-is, each pixel's rgba array would only be 1-dimensional, meaning
    # that it couldn't be compared to the 2d theme color array
    expand_pixels = pixels[:, :, np.newaxis, :]

    # get the l2 norm from each pixel to each theme color

    # summing along axis 3 just denotes that we're subtracting the rgba of each theme color from
    # the rgba of each pixel
    distances = np.sqrt(np.sum((expand_pixels - colors)**2, axis=3))

    # each pixel now has a distances array with a length equal to the size of the theme colors
    # array

    # the index of the smallest distance is selected, which corresponds to the closest color
    closest_idx = np.argmin(distances, axis=2)

    # change the values of each pixel to their corresponding closest color
    pixels = colors[closest_idx]

    # ensure that the pixel values are unsigned 8-bit integers before trying to construct the image
    new_img = Image.fromarray(np.uint8(pixels))

    return new_img

def main():
    '''
    Runs the program.
    '''

    file_name = input('filename: ')

    # lazy error handling
    try:
        new_img = process(file_name)
        save_as = f'{file_name.split('.')[0]}_proc.png'

        new_img.save(f'../img/{save_as}')
        print(f'file saved as: {save_as}')

    except FileNotFoundError:
        print('file not found.')

if __name__ == '__main__':
    main()
