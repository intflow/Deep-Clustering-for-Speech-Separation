import torch
from config.option import parse
from sklearn.cluster import KMeans
from data_loader import AudioData
import numpy as np
from utils import util
from config import option
import argparse
from model import model
from utils.stft_istft import STFT
import os
import soundfile as sf
import pickle
from tqdm import tqdm
class Separation(object):
    '''
        test deep clutsering model
        dpcl: model
        scp_file: path of scp file
        opt: parse(yml)
        waves: AudioData file
        kmeans: KMeans
        num_spks: speaker number
    '''
    def __init__(self, dpcl, scp_file, opt, save_file):
        super(Separation).__init__()
        if opt['train']['is_gpu']:
            self.dpcl = dpcl.cuda()
            self.device = torch.device('cuda')
        else:
            self.dpcl = dpcl
        ckp = torch.load('./checkpoint/'+opt['name']+'/best.pt',map_location=self.device)
        self.dpcl.load_state_dict(ckp['model_state_dict'])
        self.dpcl.eval()
        self.waves = AudioData(scp_file, **opt['datasets']['audio_setting'])
        self.keys = AudioData(scp_file, **opt['datasets']['audio_setting']).wave_keys
        self.kmeans = KMeans(n_clusters=opt['num_spks'])
        self.num_spks = opt['num_spks']
        self.save_file = save_file
        self.opt = opt
    def _cluster(self, wave, non_silent):
        '''
            input: T x F
        '''
        # TF x D
        mix_emb = self.dpcl(torch.tensor(
            wave, dtype=torch.float32).to(self.device), is_train=False)
        mix_emb = mix_emb.cpu().detach().numpy()
        # N x D
        mix_emb = mix_emb[non_silent.reshape(-1)]
        # N
        mix_cluster = self.kmeans.fit_predict(mix_emb)
        targets_mask = []
        for i in range(self.num_spks):
            mask = ~non_silent
            mask[non_silent] = (mix_cluster == i)
            targets_mask.append(mask)

        return targets_mask

    def run(self):
        stft_settings = {'window': self.opt['datasets']['audio_setting']['window'],
                         'nfft': self.opt['datasets']['audio_setting']['nfft'],
                         'window_length': self.opt['datasets']['audio_setting']['window_length'],
                         'hop_length': self.opt['datasets']['audio_setting']['hop_length'],
                         'center': self.opt['datasets']['audio_setting']['center']}

        stft_istft = STFT(**stft_settings)
        index = 0
        for wave in tqdm(self.waves):
            # log spk_spectrogram
            EPSILON = np.finfo(np.float32).eps
            log_wave = np.log(np.maximum(np.abs(wave), EPSILON))

            # apply cmvn 
            cmvn = pickle.load(open(self.opt['datasets']['dataloader_setting']['cmvn_file'],'rb'))
            cmvn_wave = util.apply_cmvn(log_wave,cmvn)

            # calculate non silent
            non_silent = util.compute_non_silent(log_wave).astype(np.bool)
            
            target_mask = self._cluster(cmvn_wave, non_silent)
            for i in range(len(target_mask)):
                name = self.keys[index]
                spk_spectrogram = target_mask[i] * wave
                i_stft = stft_istft.istft(spk_spectrogram)
                output_file = os.path.join(
                    self.save_file, self.opt['name'], 'spk'+str(i+1))
                os.makedirs(output_file, exist_ok=True)
                
                #librosa.output.write_wav(output_file+'/'+name, i_stft, 8000)
                sf.write(output_file+'/'+name, i_stft, 8000, 'PCM_16')
            index+=1
        print('Processing {} utterances'.format(index))
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parameters for testing Deep Clustering')
    parser.add_argument('-scp', type=str, help='Path to option scp file.', default='./scp/tt_mix.scp')
    parser.add_argument('-opt', type=str,
                        help='Path to option YAML file.', default='./config/train.yml')
    parser.add_argument('-save_file', type=str,
                        help='Path to save file.', default='/DL_data_big/AIGC_3rd_track3/DC_results')
    args = parser.parse_args()
    opt = option.parse(args.opt)
    dpcl = model.DPCL(**opt['DPCL'])
    
    opt['datasets']['audio_setting']['is_mag'] = False
    opt['datasets']['audio_setting']['is_log'] = False
    separation = Separation(dpcl, args.scp, opt, args.save_file)
    separation.run()
