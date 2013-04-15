# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
from PIL import Image # need Python Imaging Library for images      
from scipy.misc import toimage # need scipy for images 

class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    # form the databits, from filename
    def process(self):

            # declare initial payload and header bit arrays
            p = []
            h = []

            # if filename is provided, operate on PNG or TXT files
            if self.fname is not None:
                # operate on PNG file
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    p = self.bits_from_image(self.fname)
                    h = self.get_header(len(p), 'image')
                # operate on TXT file
                else:
                    p = self.text2bits(self.fname)
                    h = self.get_header(len(p), 'text')
            # else, send a monotone
            else:
                # send a monotone (payload of all 1s for monotone bits)
                p = [1] * self.monotone
                h = self.get_header(self.monotone, 'monotone')
                # print "header:", h

            # append header and payload as numpy array
            header = numpy.array(h)
            payload = numpy.array(p)
            databits = numpy.append(header, payload)

            return payload, databits

    # given a text file, convert to bits
    def text2bits(self, filename):

        # convert file to string
        f = open(filename, 'r')
        s = str(f.read())
        f.close()

        # converts string to binary
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])

        return result

    # given an image, convert to bits
    def bits_from_image(self, filename):

        # opens image using PIL, convert to 8-bit numpy array
        im = Image.open(filename)
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

    # given payload length and the type of source
    # (image, text, monotone)
    # form the header
    def get_header(self, payload_length, srctype):

        # declare header bit array
        header = []
        
        # create header's sourcetype bits
        if (srctype == 'monotone'):
            header = [0,0]
        elif (srctype == 'text'):
            header = [0,1]
        elif (srctype == 'image'):
            header = [1,0]

        # create header's payload bits
        payload = [int(x) for x in bin(payload_length)[2:]]
        num_pad = 16 - len(payload)
        header.extend([0] * num_pad)
        header.extend(payload)

        return header
