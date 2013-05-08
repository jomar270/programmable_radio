import math
import common_txrx as common
import numpy

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        print 'Transmitter: '
    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        
        # silence bits
        silence_bits = numpy.zeros((self.silence,), dtype=numpy.int)
        # print "silence:", silence_bits
        # print type(silence_bits)
        # print self.silence
        # print silence_bits.size

        # preamble bits
        preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preamble_bits = numpy.array(preamble)
        # print "preamble_bits:", preamble_bits
        # print len(preamble)
        # print preamble_bits.size

        # data bits
        # print "databits:", databits
        # print type(databits)
        # print databits.size

        # concatenate silence bits, preamble bits, and databits
        # databits_with_preamble = numpy.concatenate((silence_bits, preamble_bits))
        databits_with_preamble = numpy.concatenate((silence_bits, preamble_bits, databits))
        # print "databits_with_preamble:", databits_with_preamble
        # print databits_with_preamble.size

        return databits_with_preamble


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''

        # convert bits to samples
        # [one] and 0
        samples = databits_with_preamble
        print "samples:", samples
        print type(samples)
        
        return samples
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
