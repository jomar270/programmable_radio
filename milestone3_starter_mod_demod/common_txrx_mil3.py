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

  s = len(samples)
  demod_samples = numpy.empty(s)
  for n in range(s):

    #change the inverse_sample to use exponential
    inverse_sample = math.cos(2 * math.pi * fc / samplerate * n)
    # inverse_sample = math.exp(1j * 2 * math.pi * fc / samplerate * n)
    # print abs(1j * 2 * math.pi * fc / samplerate * n)
    # inverse_sample = math.exp(abs(1j * 2 * math.pi * fc / samplerate * n))
    # inverse_sample = math.e**abs(1j * 2 * math.pi * fc / samplerate * n)

    demod_samples[n] = samples[n] * inverse_sample

  omega_cut = math.pi * fc / samplerate
  lpf_samples = lpfilter(demod_samples, omega_cut)

  # return numpy.empty(len(lpf_samples))
  return lpf_samples


def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''

  # set the filter unit sample response
  L = 50
  filter_length = L * 2 + 1
  unit_sample_response = numpy.empty(filter_length)
  for n in range(-L, L + 1):
    if n != 0:
      val = math.sin(omega_cut * n) / (math.pi * n)
    else:
      val = omega_cut / math.pi
    unit_sample_response[n] = val

  # compute the demodulated samples
  s = len(samples_in)
  lpf_samples = numpy.empty(s)
  for n in range(s):
    input_samples = numpy.empty(filter_length)
    i = 0
    for m in range(n-L, n+L+1):
      if m < 0 or m >= s:
        input_samples[i] = 0
      else:
        input_samples[i] = samples_in[m]
      i += 1
    lpf_samples[n] = numpy.dot(unit_sample_response, input_samples[::-1])

  return numpy.absolute(lpf_samples)

