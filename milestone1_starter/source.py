# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
from PIL import Image # import Python Imaging Library

class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
            # Form the databits, from the filename

            p = []
            h = []

            print "self.fname:", self.fname

            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    # Its an image
                    print "image"
                    p = self.bits_from_image(self.fname)
                    h = self.get_header(len(p), 'image')
                    self.image_from_bits(p)
                else:
                    # Assume it's text
                    print "text"
                    p = self.text2bits(self.fname)
                    h = self.get_header(len(p), 'text')
            else:               
                # Send monotone (the payload is all 1s for 
                # monotone bits)
                print "monotone"
                p = [1] * self.monotone
                h = self.get_header(self.monotone, 'monotone')

            # append header and payload as numpy array
            header = numpy.array(h)
            payload = numpy.array(p)
            databits = numpy.append(header, payload)
            # print "header:", header
            # print "payload:", payload
            # print "databits:", databits

            return payload, databits

    def image_from_bits(self, bits):

        pixels = []
        for y in range(0,31):
            i = y * 32
            pixels.append(bits[i:i+31])
        # print pixels
        for y in range(len(pixels)):
            row = pixels[y]
            for x in range(len(row)):
                val = row[x]
                if val == 1:
                    val = 255
                pixels[y][x] = val
        # print pixels

        imd = numpy.array(pixels)
        
        from scipy.misc import toimage
        im = toimage(imd)

        im = im.convert('RGB')
        im.show()

    def bits2text(self, bits):

        # convert bits to text
        chars = []
        for b in range(len(bits) / 8):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        text = ''.join(chars)

        return text

    def text2bits(self, filename):
        # Given a text file, convert to bits

        # convert file to string
        f = open(filename, 'r')
        s = str(f.read())
        f.close()

        # print "string:", s

        # converts string to binary
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])

        return result

    def bits_from_image(self, filename):
        # Given an image, convert to bits

        # opens image using PIL
        im = Image.open(filename)

        # converts image to 8-bit numpy array
        im = im.convert('L')
        imd = numpy.array(im)

        # convert numpy array to lists and convert to binary
        # and if any number is greater than 0, converts to 1
        bits = []
        l = imd.tolist()
        for y in l:
            for x in y:
                if (x > 0):
                    x = 1
                bits.append(x)

        return bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header

        header = []
        
        # srctype to header
        if (srctype == 'monotone'):
            header = [0,0]
        elif (srctype == 'text'):
            header = [0,1]
        elif (srctype == 'image'):
            header = [1,0]

        # payload to header
        payload = [int(x) for x in bin(payload_length)[2:]]
        header.extend(payload)

        return header
