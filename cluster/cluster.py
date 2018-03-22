#encoding:utf-8

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import sys
import os
from time import sleep
from obtemClusters import *

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
		print 'uso: python cluster.py fileName k nComponentes'
	else:
		fileName = sys.argv[1]
		k = int(sys.argv[2])
		nComponentes = int(sys.argv[3])
		
		entrada = leEntrada(fileName)	
		pca = PCA(n_components=nComponentes)
		pca.fit(entrada)
		
		print 'variancia acumulada'
		cnt=0
		soma = 0
		for i in pca.explained_variance_ratio_:
			cnt+=1
			soma+=i
			print cnt,i,soma*100
		sleep(2)
		
		entrada = pca.transform(entrada)
		
		if '/' not in sys.argv[0]:
			diretorioScript = '.'
		else:
			diretorioScript = sys.argv[0][:len(sys.argv[0])-len(sys.argv[0].split('/')[-1])-1]
		
		kmeans = KMeans(n_clusters=k,init='k-means++',random_state=0,max_iter=1000,n_jobs=-1,verbose=1,tol=float(0.0000001),algorithm = 'full',precompute_distances=False,n_init=10).fit(entrada)
		os.system("mkdir "+diretorioScript+"/../out")
		os.system("mkdir "+diretorioScript+"/../out/saida%s"%k)
		
		arquivo = open(diretorioScript+'/../out/saida%s/clusterCenters.txt'%k,'w')
		for center in kmeans.cluster_centers_:
			arquivo.write('%s\n'%str(list(center)))
		arquivo.close()
	
		arquivo = open(diretorioScript+'/../out/saida%s/labels.txt'%k,'w')
		arquivo.write('%s\n'%str(list(kmeans.labels_)))
		arquivo.close()
	
		arquivo = open(diretorioScript+'/../out/saida%s/inertia.txt'%k,'w')
		arquivo.write('%f'%kmeans.inertia_)
		arquivo.close()
		
		resultados = leDiretorioResultados(diretorioScript+'/../out/saida%s'%k,k)
		clusters = obtemClusters(diretorioScript+'/../out/saida%s'%k,diretorioScript+'/listaIps.txt',diretorioScript+'/matriz.txt',k)[0]
		
		arquivo = open(diretorioScript+'/../out/saida%s/clusters.txt'%k,'w')
		for cluster in clusters:
			listaIps = clusters[cluster][1]
			linha = '%s\t'%cluster
			for ip in listaIps:
				linha = linha+ip+','
			linha = linha[:-1]+'\n'
			arquivo.write(linha)			
		arquivo.close()
		
		
		
		
		
		
		
		
		
		
		
		
