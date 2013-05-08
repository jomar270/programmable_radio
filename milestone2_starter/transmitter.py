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
        
        # concatenate silence bits, preamble bits, and databits
        silence_bits = numpy.zeros((self.silence,), dtype=numpy.int)
        preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preamble_bits = numpy.array(preamble)
        databits_with_preamble = numpy.concatenate((silence_bits, preamble_bits, databits))

        return databits_with_preamble


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''

        # convert bits to samples
        # [one] and 0
        # print "self.one:", self.one
        # samples = databits_with_preamble
        # print "samples:", samples
        # print type(samples)

        # print self.spb
        samples_array = []
        for databit in numpy.nditer(databits_with_preamble):
            # print databit
            if (databit == 1):
                # print [self.one] * self.spb
                # print len([self.one] * self.spb)
                # samples_array.append([self.one] * self.spb)
                samples_array.extend([self.one] * self.spb)
            elif (databit == 0):
                # print [0] * self.spb
                # print len([0] * self.spb)
                # samples_array.append([0] * self.spb)
                samples_array.extend([0] * self.spb)
            else:
                print "error"
        # print samples_array
        # samples = numpy.array([])
        samples = numpy.array(samples_array)
        # print "samples:", samples

        return samples
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
