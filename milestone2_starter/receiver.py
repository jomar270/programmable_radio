import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)
 
    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        # print "demod_samples:", demod_samples
        # print "thresh:", thresh
        # print "one:", one
        # print "self.spb:", self.spb
        # print type(demod_samples)
        # print demod_samples.size # num samples
        # print demod_samples.size / self.spb # actual bits
        # print demod_samples.size / self.spb - 200 - 118 # actual data bits, minus silence and preamble

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''

        # high-energy check procedure to get energy_offset
        # for each sample, determine if 1-value is reached
        # if so, return energy_offset of that offset
        # else, return energy_offset of -1
        energy_offset = -1
        num_samples = demod_samples.size / self.spb
        for i in range(num_samples):
            index = i * self.spb
            sample = demod_samples[index : index+self.spb]
            average = self.averageSample(sample)

            # print num_samples
            # print sample
            # print sample.size
            # print average
            # print index
            print average

            if average > thresh:
                energy_offset = index
                break
            # break # testing
        print "energy_offset:", energy_offset

        # if energy_offset couldn't be detected
        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''

        # cross-correlation check procedure to get preamble_offset
        # preamble_offset = # fill in the result of the cross-correlation check 
        preamble_offset = 0
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset

    def averageSample(self, sample):
        '''
        Get average of middle half of values in sample.
        '''

        window = self.spb / 2
        # average = numpy.average(sample[self.spb: self.spb+window])
        average = numpy.average(sample[window/2 : window/2+window])

        # print average
        # print sample
        # print type(sample)
        # print window
        # print self.spb
        # print self.spb + window
        # print sample[self.spb : self.spb+window]
        # print window/2
        # print sample[window/2 : window/2+window]
        # print len(sample[window/2 : window/2+window])
        # print type(sample[self.spb: self.spb+window])

        return average

        
    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''

        # demap demod_samples into bits
        # average values of midpoints in samples
        # use ave values and bit values of preamble to get threshold
        # demap
        # check preamble bits and continue if equal
        data_bits = demod_samples
        print "data_bits:", data_bits

        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
