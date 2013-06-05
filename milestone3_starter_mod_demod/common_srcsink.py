import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
	
    # truncate longer vector
    l1 = len(s1)
    l2 = len(s2)
    if (l1 > l2):
        s1 = s1[:l2]
    else:
        s2 = s2[:l1]

    # iterate and count difference
    hamming_d = 0
    l = len(s1)
    for x in range(l):
        if (s1[x] != s2[x]):
            hamming_d += 1

    # calculate BER
    ber = float(hamming_d) / l

    return hamming_d, ber
