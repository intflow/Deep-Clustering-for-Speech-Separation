import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils import util as ut
from utils.stft_istft import STFT
import torch



class AudioData(object):
    '''
        Loading wave file
        scp_file: the scp file path
        other kwargs is stft's kwargs
        is_mag: if True, abs(stft)
    '''

    def __init__(self, scp_file, window='hann', nfft=256, window_length=256, hop_length=64, center=False, is_mag=True, is_log=True):
        self.wave = ut.read_scp(scp_file)
        self.wave_keys = [key for key in self.wave.keys()]
        self.STFT = STFT(window=window, nfft=nfft,
                         window_length=window_length, hop_length=hop_length, center=center)
        self.is_mag = is_mag
        self.is_log = is_log

    def __len__(self):
        return len(self.wave_keys)

    def stft(self, wave_path):
        samp = ut.read_wav(wave_path)
        return self.STFT.stft(samp, self.is_mag, self.is_log)

    def __iter__(self):
        for key in self.wave_keys:
            yield self.stft(self.wave[key])

    def __getitem__(self, key):
        if key not in self.wave_keys:
            raise ValueError
        return self.stft(self.wave[key])


if __name__ == "__main__":
    ad = AudioData("/home/likai/data1/create_scp/cv_mix.scp", is_mag=True,is_log=True)
    audio = ad['011a010d_0.54422_20do010c_-0.54422.wav']
    print(audio.shape)
    print(ut.compute_non_silent(audio))
