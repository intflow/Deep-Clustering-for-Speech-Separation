import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from torch.nn.utils.rnn import pack_sequence, pad_sequence
from data_loader import AudioData
import torch
from torch.utils.data import Dataset, DataLoader
from utils import util
import pickle
import numpy as np



class dataset(Dataset):
    def __init__(self, mix_reader, target_readers):
        super(dataset).__init__()
        self.mix_reader = mix_reader
        self.target_readers = target_readers
        self.keys = mix_reader.wave_keys

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, index):
        key = self.keys[index]
        if key not in self.keys:
            raise ValueError
        return (self.mix_reader[key], [target[key] for target in self.target_readers])


class dataloader(object):
    def __init__(self, dataset, batch_size=40, shuffle=True, num_workers=16, cmvn_file='../cmvn.ark'):
        super(dataloader).__init__()
        self.dataload = DataLoader(
            dataset, batch_size=batch_size, num_workers=num_workers, shuffle=shuffle, collate_fn=self.collate)
        self.cmvn = pickle.load(open(cmvn_file, 'rb'))
    
    def __len__(self):
        return len(self.dataload)

    def transform(self, mix_wave, target_waves):
        frames = mix_wave.shape[0]
        non_slient = util.compute_non_silent(mix_wave)
        mix_wave = util.apply_cmvn(mix_wave, self.cmvn)
        target_waves = np.argmax(np.array(target_waves), axis=0)
        return {
            "frames": frames,
            "non_slient": torch.tensor(non_slient, dtype=torch.float32),
            "mix_wave": torch.tensor(mix_wave, dtype=torch.float32),
            "target_waves": torch.tensor(target_waves, dtype=torch.int64)
        }
    
    def collate(self, batchs):
        trans = sorted([self.transform(mix_wave, target_waves)
                        for mix_wave, target_waves in batchs], key=lambda x: x["frames"], reverse=True)
        mix_wave = pack_sequence([t['mix_wave'] for t in trans])
        target_waves = pad_sequence([t['target_waves']
                                     for t in trans], batch_first=True)
        non_slient = pad_sequence([t['non_slient']
                                   for t in trans], batch_first=True)
        return mix_wave, target_waves, non_slient

    def __iter__(self):
        for b in self.dataload:
            yield b


if __name__ == "__main__":
    mix_reader = AudioData(
        "/home/likai/Desktop/create_scp/tr_mix.scp", is_mag=True, is_log=True)
    target_readers = [AudioData("/home/likai/Desktop/create_scp/tr_s1.scp", is_mag=True, is_log=True),
                      AudioData("/home/likai/Desktop/create_scp/tr_s2.scp", is_mag=True, is_log=True)]
    dataset = dataset(mix_reader, target_readers)
    dataloader = dataloader(dataset)
    print(len(dataloader))
