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

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''

        # high-energy check procedure to get energy_offset
        # for each sample, determine if 1-value is reached
        # if so, return energy_offset of that offset
        # else, return energy_offset of -1
        energy_offset = -1
        num_bits = demod_samples.size / self.spb
        for i in range(num_bits):
            index = i * self.spb
            sample = demod_samples[index : index+self.spb]
            average = self.averageSample(sample)
            if average > thresh:
                energy_offset = index
                break

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
        # starting with preamble_search, compute cross correlation between preamble and signal
        # preamble_offset is where correlation is highest
        preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preamble_samples = self.createPreambleSamples(preamble, one)
        preamble_length = preamble_samples.size
        preamble_search = demod_samples[energy_offset:]
        preamble_search_size = preamble_search.size - preamble_length
        scores = []
        for i in range(preamble_search_size):
            sample = preamble_search[i : i+preamble_length]
            scores.append(self.crossCorrelation(sample, preamble_samples))
        preamble_offset = numpy.argmax(scores)
        
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
        average = numpy.average(sample[window/2 : window/2+window])

        return average

    def crossCorrelation(self, samples, preamble_samples):
        '''
        Given samples, compute the cross-correlation between it and the preamble.
        '''

        score = numpy.dot(samples, preamble_samples)

        return score

    def createPreambleSamples(self, preamble, one):
        '''
        Convert preamble bits to samples.
        '''
        preamble_bits = numpy.array(preamble)
        samples_array = []
        for databit in numpy.nditer(preamble_bits):
            if (databit == 1):
                samples_array.extend([one] * self.spb)
            elif (databit == 0):
                samples_array.extend([0] * self.spb)
            else:
                print "error in sampling"
        preamble_samples = numpy.array(samples_array)

        return preamble_samples
        
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

        # average values of midpoints in samples
        samples = demod_samples[preamble_start:]
        averages = []
        num_bits = samples.size / self.spb
        for i in range(num_bits):
            index = i * self.spb
            sample = samples[index : index+self.spb]
            averages.append(self.averageSample(sample))

        # get new threshold
        preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preamble_length = len(preamble)
        ones = []
        zeros = []
        for i in range(preamble_length):
            if preamble[i] == 1:
                ones.append(samples[i])
            elif preamble[i] == 0:
                zeros.append(samples[i])
        threshold = (numpy.average(ones) + numpy.average(zeros)) / 2
        
        # check if preamble bits are equal to preamble using new threshold
        preamble_test = averages[:preamble_length]
        preamble_mapped = []
        for bit in preamble_test:
            if bit > threshold:
                preamble_mapped.append(1)
            elif bit < threshold:
                preamble_mapped.append(0)

        # set data bits
        data_bits = averages[preamble_length:]

        # exit if preamble doesn't match
        if numpy.array_equal(preamble, preamble_mapped) == False:
            print '*** ERROR: Could not detect preamble. ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
