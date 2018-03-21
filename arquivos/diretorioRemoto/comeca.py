#encoding:utf-8

import os
import sys

if __name__=='__main__':
	if len(sys.argv)<5:
		print 'Uso: python comeca.py hitlist taxaDeMedicoes diretorioResultados diretorioTmp'
	else:
		fileNameHitlist = sys.argv[1]
		taxaMedicoes = int(sys.argv[2])
		diretorioResultados = sys.argv[3]
		diretorioTmp = sys.argv[4]
		
		#Define o nome do arquivo, que será um timeStamp da data de criação
		arquivoComando = os.popen('date -u +"%Y%m%d%H%M%S"')
		fileNameSaida = arquivoComando.read().strip()
		arquivoComando.close()
		
		#Coloca o hitlist em ordem aleatória antes de começar.
		os.system('sort -R %s > %s.random'%(fileNameHitlist,fileNameHitlist))
		fileNameHitlist = fileNameHitlist+'.random'
		
		#Executa o experimento.
		os.system('python fazMedicoes.py %s %s %d'%(fileNameHitlist,diretorioTmp+'/'+fileNameSaida,taxaMedicoes))
		
		#Copia o arquivo para o diretório definitivo.
		os.system('mv %s %s'%(diretorioTmp+'/'+fileNameSaida,diretorioResultados+'/'+fileNameSaida))
