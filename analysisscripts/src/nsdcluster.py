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

nsdfile='nsd.npy'

datapath = '/mntdirect/_users/brennich/barbaramaria/DnaKcGrpEAMPPPNP/20140925_15mg/dammifP2/gnomv2/'

def sumcluster(linkage,node):
    nodes = []
    cluster = []
    print node
    print linkage[node]
    Nleafs = linkage.shape[0] + 1
    if linkage[node][0] < Nleafs: 
        cluster += [linkage[node][0]]
        nodes += [node]
    else: 
        clust, nod = sumcluster(linkage,linkage[node][0]-Nleafs)
        cluster += clust
        nodes += nod
    if linkage[node][1] < Nleafs: 
        cluster += [linkage[node][1]]
        nodes += [node]
    else: 
        clust, nod =  sumcluster(linkage,linkage[node][1]-Nleafs)
        cluster += clust
        nodes += nod   
    print cluster, nodes
    return cluster, nodes

def linkageToCluster(linkage, maxnsd = 1.0):
    Nleafs = linkage.shape[0] + 1
    clusters = []
    clustered = []
    print Nleafs
    for node in  reversed(range(Nleafs-1)):
        print linkage[node]
        if linkage[node][2] > maxnsd and (linkage[node][0:2]< Nleafs).all():
            print 'Found binary cluster'
            clusters.append(linkage[node][0:2].tolist())
            clustered += linkage[node][0:2].tolist()
            
        if linkage[node][2] < maxnsd and node not in clustered: #:and (linkage[node][0] not in  clustered):
            clustered.append(node)
            print node
            clust, Nodes = sumcluster(linkage,node)#linkage[node][0])
            #rightSide, rightNodes = sumcluster(linkage,linkage[node][1])
            
            clusters.append(clust)
            clustered += Nodes
            #clustered += rightNodes
                  
    print clusters  
    print clustered      

#matrix = np.array([[0,0.1,3],[0.1,0,0.1],[3,0.1,0]], dtype=np.float)

#print matrix

nsd = None

models = glob.glob(datapath + '*-1.pdb')
modelnames = [model.split('/')[-1] for model in models]

if op.exists(nsdfile): 
    nsd = np.load(nsdfile)
    if nsd.shape[0] != len(models):
        nsd = None

if nsd is None:
    nsd = np.zeros((len(models),len(models)))
    
    for i in range(len(models)):
        model1 = models[i]
        for j in range(i):
            model2 = models[j]
            #Note: for parallet processing each model supcomb need its own folder. In serial processing this needs less diskspace.
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
            np.save(nsdfile,nsd)

#print nsd               

assert (nsd.transpose()==nsd).all()
 
 
#linkage =  sch.ward(nsd)
linkage =  sch.linkage(nsd,method='ward')
print linkage
#print modelnames

linkageToCluster(linkage, maxnsd = 1.5)


 
plt.subplot(1, 2, 1)
ddata = sch.dendrogram(linkage, labels=modelnames, orientation='left')

 
plt.show()
