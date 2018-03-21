import sys
import os

def constroiDiretorio(localDiretorio,arquivoHitlist,taxaMedicoes,sliceName):
	os.system('mkdir %s/diretorioRemoto'%localDiretorio)
	os.system('mkdir %s/diretorioLocal'%localDiretorio)
	os.system('cp -r arquivos/diretorioRemoto/* %s/diretorioRemoto'%localDiretorio)
	os.system('cp -r arquivos/diretorioLocal/* %s/diretorioLocal'%localDiretorio)
	os.system('chmod 777 -R %s/diretorioLocal'%localDiretorio)
	os.system('cp %s %s/diretorioRemoto/listas/hitlist.txt'%(arquivoHitlist,localDiretorio))
	
	arquivo = open('%s/diretorioRemoto/inicia.sh'%localDiretorio,'w')
	arquivo.write('#!/bin/bash\n\ncd /home/%s\npython comeca.py ./listas/hitlist.txt %d ./resultados ./tmp\ncd -'%(sliceName,taxaMedicoes))
	arquivo.close()
	
	os.system('chmod +x %s/diretorioRemoto/inicia.sh'%localDiretorio)
	
if __name__=='__main__':
	if len(sys.argv) < 5:
		print 'uso: python criaDiretorioRemoto.py diretorioMedicao arquivoHitlist taxaMedicoes sliceName'
	else:
		localDiretorio = sys.argv[1]
		arquivoHitlist = sys.argv[2]
		taxaMedicoes = int(sys.argv[3])
		sliceName = sys.argv[4]
		constroiDiretorio(localDiretorio,arquivoHitlist,taxaMedicoes,sliceName)
