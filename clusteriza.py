import os
import sys


if __name__=='__main__':
	if len(sys.argv) < 5:
		print 'uso: python clusteriza.py diretorioColeta hitlistColeta numeroClusters numeroComponentes'
	else:
		diretorioColeta = sys.argv[1]
		hitlistColeta = sys.argv[2]
		k = int(sys.argv[3])
		n = int(sys.argv[4])
		
		if '/' not in sys.argv[0]:
			diretorioScript = '.'
		else:
			diretorioScript = sys.argv[0][:len(sys.argv[0])-len(sys.argv[0].split('/')[-1])-1]
		
		os.system('python '+diretorioScript+'/cluster/obtemMatriz.py %s %s'%(diretorioColeta,hitlistColeta))
		os.system('python '+diretorioScript+'/cluster/cluster.py %s %s %s'%(diretorioScript+'/cluster/matriz.txt',k,n))
