
import numpy as  np

import matplotlib.pylab as plt
import glob 
import subprocess as sp






def rescale(files):
    for file in files:
        outFile = file.split('.')[0] + '_scaled.dat'
        q,I,s = np.loadtxt(file, unpack=True)
        maxI = I.mean()
        m = np.vstack((q, I / maxI, s / maxI))
        with open(outFile, "w") as outfile:
            np.savetxt(outfile, m.T)
     
def makeArrayPlot(array, filename=None, close=True,discrete = True, alphaGreen = 0.9, alphaRed = 0.1):
    fig = plt.figure(figsize=(15, 10))
    ax1 = fig.add_subplot(1, 2, 1)
    if discrete:
        np.where(array>=alphaGreen,array, 1)
        array[np.where(((alphaGreen>array) & (alphaRed<array)) == True)] = 0.25
        np.where(alphaRed>=array,array,0.0)
    ax1.imshow(array, interpolation="nearest", origin="upper",cmap='brg')
    ax1.set_title(u"datcmp correlation table")
    ax1.set_xticks(range(array.shape[0]))
    ax1.set_xticklabels([str(i) for i in range(1, 1 + array.shape[0] )])
    ax1.set_xlim(-0.5, array.shape[0] - 0.5)
    ax1.set_ylim(-0.5, array.shape[0] - 0.5)
    ax1.set_yticks(range(array.shape[0]))
    ax1.set_yticklabels([str(i) for i in range(1, 1 + array.shape[0])])
    ax1.set_xlabel(u"File number")
    ax1.set_ylabel(u"File number")
    fig.savefig(filename)
    if close:
        fig.clf()
        plt.close(fig)
    else:
        return fig

files = glob.glob('*_sub.dat')
nfiles = len(files)

rescale(files)
    
dcmp = np.zeros((nfiles, nfiles))

process = sp.Popen(['datcmp', '--PXSOFT_VERSION', 'v2.6.0', '*_scaled.dat'], stdout=sp.PIPE, stderr=sp.PIPE)
output, error = process.communicate()



for line in output.split('\n'):
    words = line.split()
    if  'vs.' in words:
        file1 = int(words[0])
        file2 = int(words[2])
        p12 = float(words[-1].strip("*"))
        dcmp[file1-1,file2-1] = dcmp[file2-1,file1-1] =  p12
        

makeArrayPlot(dcmp, filename = 'datcmp.png', close=False)     
#    