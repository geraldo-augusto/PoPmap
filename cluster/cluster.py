#encoding:utf-8

import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import sys
import os

def leEntrada(fileName):
	arquivo = open(fileName,'r')
	pontos = list()
	for linha in arquivo:
		linha = linha.strip().split(' ')
		for i in xrange(len(linha)):
			linha[i] = int(linha[i])
		pontos.append(linha)
	arquivo.close()
	return np.array(pontos)

if __name__=='__main__':

	if len(sys.argv) < 3:
		print 'uso: python cluster.py fileName k'
	else:
		fileName = sys.argv[1]
		k = int(sys.argv[2])
		
		entrada = leEntrada(fileName)	
		pca = PCA(n_components=25)
		pca.fit(entrada)
		
		'''
		cnt=0
		soma = 0
		for i in pca.explained_variance_ratio_:
			cnt+=1
			soma+=i
			print cnt,i,soma*100
		'''
		entrada = pca.transform(entrada)
		
		kmeans = KMeans(n_clusters=k,init='k-means++',random_state=0,max_iter=1000,n_jobs=1,verbose=1,tol=float(0.0000001),algorithm = 'full',precompute_distances=False,n_init=1).fit(entrada)
		#kmeans = MiniBatchKMeans(n_clusters=k,init='k-means++',random_state=0,max_iter=300,verbose=1).fit(entrada)
		
		os.system("mkdir saida%s"%k)
		
		arquivo = open('saida%s/clusterCenters.txt'%k,'w')
		for center in kmeans.cluster_centers_:
			arquivo.write('%s\n'%str(list(center)))
		arquivo.close()
	
		arquivo = open('saida%s/labels.txt'%k,'w')
		arquivo.write('%s\n'%str(list(kmeans.labels_)))
		arquivo.close()
	
		arquivo = open('saida%s/inertia.txt'%k,'w')
		arquivo.write('%f'%kmeans.inertia_)
		arquivo.close()
		
		
		
