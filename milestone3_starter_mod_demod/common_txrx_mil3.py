import numpy
import math
import operator

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''

  s = len(samples)
  mod_samples = numpy.empty(s)
  for n in range(s):
    carrier_signal_sample = math.cos(2 * math.pi * fc / samplerate * n)
    mod_samples[n] = samples[n] * carrier_signal_sample

  return mod_samples


def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  return 0


def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  
  # compute the demodulated samples
  return 0

