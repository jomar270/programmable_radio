# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
from PIL import Image # import Python Imaging Library        
from scipy.misc import toimage # scipy


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.

        # get header bits and read header
        header_bits = recd_bits[0:18]
        srctype, payload_length = self.read_header(header_bits)

        # we return rcd_payload but convert a copy of it 
        # which we pas to image_from_bits and convert to 255s and 0s for our image
        rcd_payload = recd_bits[18:]
        rcd_payload_copy = list(rcd_payload)

        # based on source type, get bits
        if (srctype == 'monotone'):
            pass
        elif (srctype == 'text'):
            # print text if text
            print self.bits2text(rcd_payload)
        else:
            # save image if image
            self.image_from_bits(rcd_payload_copy, "rcd-image.png")
        
        # return the received payload for comparison purposes
        return rcd_payload

    # Convert the received payload to text (string)
    def bits2text(self, bits):

        # convert binary to characters
        chars = []
        for b in range(len(bits) / 8):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        text = ''.join(chars)

        return text

    # Convert the received payload to an image and save it
    # No return value required.
    def image_from_bits(self, bits, filename):

        # declare pixels matrix (list of lists)
        pixels = []

        # turning list of bits to matrix of bits
        for y in range(0,32):
            i = y * 32
            pixels.append(bits[i:i+32])

        # convert to 0's and 255's
        for y in range(len(pixels)):
            row = pixels[y]
            for x in range(len(row)):
                val = row[x]
                if val == 1:
                    val = 255
                pixels[y][x] = val

        # convert pixels to image and save
        imd = numpy.array(pixels)
        im = toimage(imd)
        im = im.convert('RGB')
        im.save(filename, 'PNG')

        pass 

    # Given the header bits, compute the payload length
    # and source type (compatible with get_header on source)
    def read_header(self, header_bits):

        # assigned values
        srctype = ''
        l = (header_bits[0:2]).tolist()
        if l[0] == 0 and l[1] == 0:
            srctype = 'monotone'
        elif l[0] == 0 and l[1] == 1:
            srctype = 'text'
        else:
            srctype = 'image'

        # get header bits and payload length
        p = header_bits[2:]
        p = p.astype(numpy.int64) # converted numpy array of float64 to int64 (so it's 1's and 0's)
        payload_length = int("".join(str(i) for i in p), 2)

        # print values
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length