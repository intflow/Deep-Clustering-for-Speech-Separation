import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

def waveform(x, pic_path):
    if pic_path == None:
        pic_path = ".wav.tmp"
    plt.figure()
    plt.plot(x)
    plt.savefig(pic_path + ".png", bbox_inches='tight')
    plt.show()
    plt.close()

def spectrogram(X, pic_path=None): 
    if pic_path == None:
        pic_path = "spec.tmp."
    logX_feat = np.log10(X+0.0001)
    zmin = logX_feat.min()
    zmax = logX_feat.max()
    plt.figure()
    plt.contourf(logX_feat, cmap='inferno', vmin=zmin, vmax=zmax)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    
    if pic_path == None:
        plt.show()
        plt.close()
    else:
        try:
            plt.savefig(pic_path + ".png", bbox_inches='tight')
            plt.close()
        except:
            return 0

def spectrogram_batch(X, pic_path): 
    X = np.squeeze(X)
    b,f,t = X.shape
    if b > 32:
        b = 32
        X = X[:b,:,:] #BHW
    X = np.transpose(X,(0,2,1))#BWH

    X = np.reshape(X,(b*t,f)).T
    if pic_path == None:
        pic_path = "spec.tmp."
    logX_feat = np.log10(X+0.0001)
    zmin = logX_feat.min()
    zmax = logX_feat.max()
    plt.figure()
    plt.contourf(logX_feat, cmap='inferno', vmin=zmin, vmax=zmax)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    
    if pic_path == None:
        plt.show()
        plt.close()
    else:
        try:
            plt.savefig(pic_path + ".png", bbox_inches='tight')
            plt.close()
        except:
            return 0            

def contour (X, pic_path): 
    if pic_path == None:
        pic_path = "cont.tmp."
    zmin = X.min()
    zmax = X.max()
    plt.figure()
    plt.contourf(X, cmap='inferno', vmin=zmin, vmax=zmax)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Rank')
    plt.colorbar()
    plt.savefig(pic_path + ".png", bbox_inches='tight')
    plt.show()
    plt.close()