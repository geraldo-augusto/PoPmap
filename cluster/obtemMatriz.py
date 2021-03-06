#encoding:utf-8

from coleta import *
import numpy as np
import sys

def completaCoordenadas(coordenadas):
	copia = list(coordenadas)
	while -1 in copia:
		copia.remove(-1)
	while -1 in coordenadas:
		posicao = coordenadas.index(-1)
		mediana = int(np.median(copia))
		coordenadas[posicao] = mediana

if __name__=='__main__':
	if len(sys.argv) < 3:
		print 'uso: python obtemMatriz.py diretorioColeta hitlistColeta'
	else:
		diretorio = sys.argv[1]
		hitlist = sys.argv[2]
		
		experimento = leDiretorio(diretorio,hitlist)
		hitlist=experimento[1]
		hosts = experimento[0].keys()
		ttlParaHops(experimento)
		pontosValidos = list()
		ipsCorrespondentes = list()
	
		for ip in hitlist:
			ip = inteiroParaIp(ip)
			valido = True
			coordenadas = list()
			for host in hosts:
				coordenadas.append(numeroHops(experimento,host,ip))
			if coordenadas.count(-1) <=3:
				if -1 in coordenadas:
					completaCoordenadas(coordenadas)
				pontosValidos.append(coordenadas)
				ipsCorrespondentes.append(ip)
		
		if '/' not in sys.argv[0]:
			diretorioSaida = '.'
		else:
			diretorioSaida = sys.argv[0][:len(sys.argv[0])-len(sys.argv[0].split('/')[-1])-1]
			
		arquivo = open(diretorioSaida+'/listaIps.txt','w')
		for ip in ipsCorrespondentes:
			arquivo.write('%s\n'%ip)
		arquivo.close()
	
		arquivo = open(diretorioSaida+'/matriz.txt','w')
		for ponto in pontosValidos:
			linha = ''
			for coordenada in ponto:
				linha = linha+str(coordenada)+' '
			linha = linha[:-1]
			arquivo.write('%s\n'%linha)
		arquivo.close()
