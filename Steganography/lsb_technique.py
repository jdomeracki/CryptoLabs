from PIL import Image
from base64 import b64encode, b64decode


class LSB:
    def __init__(self):
        pass

    def encode_message(self, plaintext):
        return ''.join([format(ord(char), '08b') for char in plaintext]) + '00000011'

    def hide_message(self, image, plaintext):
        binarystream = self.encode_message(plaintext)
        binarystream_length = len(binarystream)
        image = Image.open(image)
        width, height = image.size
        pixels = image.load()
        counter = 0
        for row in range(height):
            for col in range(width):
                r, g, b, a = [format(x, '08b') for x in pixels[row, col]]
                if int(a, 2) == 255:
                    if binarystream_length - counter >= 3:
                        pixels[row, col] = tuple([int(r[:-1] + binarystream[counter], 2), int(g[:-1] + binarystream[counter+1], 2), int(b[:-1] + binarystream[counter+2], 2), int(a, 2)])
                        counter += 3
                    elif binarystream_length - counter == 2:
                        pixels[row, col] = tuple([int(r[:-1] + binarystream[counter], 2), int(g[:-1] + binarystream[counter+1], 2), int(b, 2), int(a, 2)])
                        break
                    elif binarystream_length - counter == 1:
                        pixels[row, col] = tuple([int(r[:-1] + binarystream[counter], 2), int(g, 2), int(b, 2), int(a, 2)])
                        break
                    else:
                        break
        image.save('altered.png')

    def decode_message(self, binarycode):
        message = ''
        for i in range(0, len(binarycode), 8):
            ascii_value = int(binarycode[i: i + 8], 2)
            # EXT ASCII character
            if ascii_value == 3:
                break
            else:
                message += chr(ascii_value)
        print(message)

    def read_meesage(self, image):
        image = Image.open(image)
        width, height = image.size
        pixels = image.load()
        counter = 0
        binarystream = ''
        for row in range(height):
            for col in range(width):
                r, g, b, a = [format(x, '08b') for x in pixels[row, col]]
                if int(a, 2) == 255:
                    binarystream += f'{r[-1]}{g[-1]}{b[-1]}'
        self.decode_message(binarystream)


if __name__ == '__main__':
    message = '''Who cares that it makes plants grow
Who cares what it does
Since you broke my heart
Who loves the wind
Who cares that it makes breezes
Who cares what it does
Since you broke my heart
Not everyone
Who loves the rain
Who cares that it makes flowers
Who cares that it makes showers
Since you broke my heart
Who cares that it is shining
Who cares what it does
Since you broke my heart
Not everyone
Not everyone'''

    lsb = LSB()
    lsb.hide_message('sun.png', message)
    lsb.read_meesage('altered.png')
