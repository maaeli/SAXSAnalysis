import scipy.cluster.hierarchy as sch
import numpy as  np
import matplotlib as mpl
import matplotlib.pylab as plt
import glob 
import subprocess as sp
import os
import os.path as op

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


datapath = '/mntdirect/_users/brennich/barbaramaria/DnaKcGrpEAMPPPNP/20140925_15mg/dammifP2/gnomv2/'



#matrix = np.array([[0,0.1,3],[0.1,0,0.1],[3,0.1,0]], dtype=np.float)

#print matrix

models = glob.glob(datapath + '*-1.pdb')


nsd = np.zeros((len(models),len(models)))

for i in range(len(models)):
    model1 = models[i]
    for j in range(i):
        model2 = models[j]
        sp.call(['supcomb', model1, model2], stdout=DEVNULL)
        repmodel = ''.join(model2.split('.')[:-1]) + 'r.pdb'
        if op.exists(repmodel):
            with open(repmodel,'r') as result:
                for line in result.readlines():
                    if 'REMARK 265  Final distance (NSD)' in line:
                        mnsd = line.split()[-1]
                        print mnsd
                        break
        nsd[i,j] = nsd [j,i] = mnsd

print nsd               

assert (nsd.transpose()==nsd).all()
 
 
linkage =  sch.ward(matrix)
print linkage
 
print sch.dendrogram(linkage)#
 
plt.subplot(1, 2, 1)
ddata = dendrogram(linkage)
 
plt.show()
