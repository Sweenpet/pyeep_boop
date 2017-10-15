import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import math as math
import winsound

A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def get_pitch(freq):
    h = round(12 * math.log(freq / C0, 2))
    octave = h // 12
    n = int(h % 12)
    return name[n] + str(octave)


def fft_test_noncontinuous():
    fs = 4000
    total_seconds = 2
    total_points = int(fs * total_seconds)
    t_range = [t * 1 / float(fs) for t in range(0, total_points)]
    t_normal = [t for t in t_range]
    s = []
    interval = 4
    step = total_points / interval

    for i in range(0, interval):
        s[i * step: step * (i + 1)] = [math.sin(2 * math.pi * ((i + 1) * 10) * t) for t in t_range[i * step: step * (i + 1)]]

    plt.plot(t_range, s)

    for i in range(0, interval):
        sub_s = s[i * step : step * (i + 1)]

        y = abs(np.fft.fft(sub_s))
        freqs = [f * fs for f in np.fft.fftfreq(step)]

        freqs = freqs[0:step / 2 + 1]
        y = y[0:step / 2 + 1]

        max_index = np.argmax(y)
        max_value = freqs[max_index]
        sub_normal = t_normal[i * step: (i + 1) * step]
        plt.plot(sub_normal, sub_s)

        plt.figure()
        plt.stem(freqs, y, linefmt='b-', markerfmt='bo', basefmt='r-')


def fft_test_continuous():
    fs = 4000
    total_seconds= 2
    total_points= int(fs * total_seconds)
    t_range = [t * 1/ float(fs) for t in range(0, total_points)]
    t_normal = [t for t in t_range]
    s = [.7 * math.sin(2 * math.pi * 20 * t) + .9 * math.sin(2 * math.pi * 45 * t) + .9 * math.sin(2 * math.pi * 90 * t) for t in t_range]
    y = abs(np.fft.fft(s))
    freqs = [f * fs for f in np.fft.fftfreq(total_points)]

    freqs = freqs[0:total_points/2 + 1]
    y = y[0:total_points/2 + 1]

    max_index = np.argmax(y)
    max_value = freqs[max_index]

    plt.plot(t_normal, s)

    plt.figure()
    plt.stem(freqs, y, linefmt='b-', markerfmt='bo', basefmt='r-')


# largest = 0;
# second = 1; etc...
def get_largest_index(array, n):
    sorted_list = [i[0] for i in sorted(enumerate(array), key=lambda x: x[1])]
    return sorted_list[len(sorted_list) - 1 - n]


def main():
    rate, data = wavfile.read('krtheme.wav')
    print 'rate: {0}'.format(rate)
    nframes = len(data)
    print 'song length: {0} seconds'.format(nframes/rate)

    mono = [(int(val[0]) + int(val[1]))/2 for val in data]
    notes = []
    dom_freqs = []
    beat_samp = 4
    slow_down = 2
    n_largest = 3
    for i in (range(0, nframes/rate)):

       sec_interval = mono[i * rate: rate * (i + 1)]
        # its usually 8 beats per second
       beat_rate= rate/ beat_samp

       for beat in range(0, beat_samp):
            beat_interval = sec_interval[beat_rate * beat: beat_rate * (beat + 1)]
            complex_amp = abs(np.fft.fft(beat_interval))
            freqs = [f * rate for f in np.fft.fftfreq(beat_rate)]

            freqs = freqs[0: beat_rate/2]
            complex_amp = complex_amp[0: beat_rate/2]

            max_index = get_largest_index(complex_amp, n_largest)
            max_freq = int(freqs[max_index])

            if max_freq < 37:
                max_freq = 37

            dom_freqs.append(max_freq)
            pitch = get_pitch(max_freq)
            notes.append(pitch)

            print 'the most dominant note is {0}'.format(pitch)

    for freq in dom_freqs:
       winsound.Beep(freq, 1000 * slow_down / beat_samp)

    print 'complete'

if __name__ == '__main__':
    #fft_test_noncontinuous()
    #fft_test_continuous()
    main()