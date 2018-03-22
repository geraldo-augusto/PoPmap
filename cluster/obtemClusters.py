#encoding:utf-8

from glob import glob
import numpy as np
from sklearn.decomposition import PCA

def leListaIps(arquivoIps):
	listaIps = list()
	arquivo = open(arquivoIps,'r')
	for linha in arquivo:
		linha = linha.strip()
		listaIps.append(linha)
	arquivo.close()
	return listaIps

def leListaCoordenadas(arquivoCoordenadas,nComponentes):
	listaCoordenadas = list()
	arquivo = open(arquivoCoordenadas,'r')
	for linha in arquivo:
		linha = linha.strip().split(' ')
		for i in xrange(len(linha)):
			linha[i] = int(linha[i])
		listaCoordenadas.append(linha)
	arquivo.close()
	
	listaCoordenadas = np.array(listaCoordenadas)
	pca = PCA(n_components=nComponentes)
	pca.fit(listaCoordenadas)
	listaCoordenadas = pca.transform(listaCoordenadas)
	listaCoordenadas = listaCoordenadas.tolist()
	
	return listaCoordenadas

def constroiMapaCoordenadasIps(listaCoordenadas,listaIps):
	'''
		Retorna um dicionário do formato: mapaCoordenadas[ip] = [listaCoordenadas do Ip]
	'''
	mapaCoordenadas = dict()
	for i in xrange(len(listaIps)):
		mapaCoordenadas[listaIps[i]] = listaCoordenadas[i]
	return mapaCoordenadas

def leDiretorioResultados(diretorioResultados,k):
	'''
		Le os resultados e retorna um dicionario na forma:
		d[k] = [inertia,clusterCenters,labels]
	'''

	#Leitura dos centros
	arquivo = open(diretorioResultados+'/clusterCenters.txt','r')
	centros = list()
	for linha in arquivo:
		linha = linha.strip()[1:-1].split(', ')
		for i in xrange(len(linha)):
			linha[i] = float(linha[i])
		centros.append(linha)
	arquivo.close()

	#Leitura da inercia
	arquivo = open(diretorioResultados+'/inertia.txt','r')
	inertia = float(arquivo.readline())
	arquivo.close()

	#Leitura dos labels
	arquivo = open(diretorioResultados+'/labels.txt','r')
	labels = arquivo.readline()
	labels = labels.strip()[1:-1].split(', ')
	for i in xrange(len(labels)):
		labels[i] = int(labels[i])	
	arquivo.close()

	resultados = [inertia,centros,labels]
	return resultados

def obtemClusters(diretorioResultados,arquivoIps,arquivoCoordenadas,k):
	'''
		Para um determinado k, cria uma estrutura na forma: 
			(clusters,mapaCoordenadas) em que
			clusters[cluster] = [centro,[lista de Ips associados ao centro]]
			mapaCoordenadas[ip] = [listaCoordenadas do Ip]
	'''
	resultados = leDiretorioResultados(diretorioResultados,k)
	listaIps = leListaIps(arquivoIps)
	listaCoordenadas = leListaCoordenadas(arquivoCoordenadas,len(resultados[1][0]))
	mapaCoordenadas = constroiMapaCoordenadasIps(listaCoordenadas,listaIps)
	del(listaCoordenadas)
	
	inertia = resultados[0]
	centros = resultados[1]
	labels = resultados[2]
	
	clusters = dict()
	for label in xrange(len(centros)):
		clusters[label] = [centros[label],list()]
	for i in xrange(len(labels)):
		clusters[labels[i]][1].append(listaIps[i])
	
	del(listaIps)
	del(resultados)
	
	return (clusters,mapaCoordenadas)
	




