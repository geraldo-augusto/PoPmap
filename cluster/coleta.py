#encoding:utf-8

from collections import defaultdict
from glob import glob


#Cria uma estrutura de dados para armazenar os dados de uma medição de forma eficiente.
#Tambem define função para ler os TTLs de de cada par (node,ip)
#As duas funções que devem ser usadas pelo usuário são:
#	experimento = leDiretorio(diretorio,hitlist,maximo=1000000)
#	ttlParaHops(experimento)
#	ttl = buscaTtl(experimento,host,ip)
#	nHops = numeroHops(experimento,host,ip)


def ipParaInteiro(ip):
	#Transforma o ip em seu equivalente inteiro.
	partes = ip.split('.')
	binarioIp = ''
	#print ip
	for parte in partes:
		binario = bin(int(parte))[2:]
		if len(binario)<8:
			zeros = '0'*(8-len(binario))
			binario = zeros+binario
		binarioIp = binarioIp+binario
	inteiroIp = int(binarioIp,2)
	return inteiroIp

def inteiroParaIp(inteiro):
	#Transforma o intero no ip original.
	binarioIp = bin(inteiro)[2:]
	if len(binarioIp) < 32:
		zeros = '0'*(32-len(binarioIp))
		binarioIp = zeros+binarioIp
	
	partes = []
	inicio=0
	fim=8
	cnt=0
	while cnt<4:
		partes.append(binarioIp[inicio:fim])
		fim+=8
		inicio+=8
		cnt+=1
	
	ip = ''
	for parte in partes:
		inteiroParte = int(parte,2)
		ip = ip+str(inteiroParte)+'.'
	ip = ip[0:-1]
	
	return ip
	
def criaListaReferencia(fileName):
	#Cria a lista de referência para a estrutura de dados a partir do arquivo de hitlist
	#que contém todos os ips do experimento.
	arquivo = open(fileName,'r')
	listaReferencia = list()
	for linha in arquivo:
		ip = linha.strip()
		listaReferencia.append(ipParaInteiro(ip))
	arquivo.close()
	return listaReferencia

def criaDicionarioPosicoes(listaReferencia):
	#Cria um dicionário no formato posicoes[InteiroIp]=PosicaoListaReferencia
	#Serve para fazer busca em O(1) pelo ttl requisitado.
	
	posicoes = dict()
	posicao = 0
	while posicao<len(listaReferencia):
		posicoes[listaReferencia[posicao]] = posicao
		posicao+=1
	return posicoes

def leArquivo(fileName,posicoes):
	#Le o arquivo e cria uma lista de ttls na ordem em que estão os ips na lista de referência.
	#-1 significa que a sonda não respondeu.
	#-2 significa que a medição não foi feita.
	
	#Inicializa a lista de ttls
	listaTtls = list()
	cnt = 0
	while cnt<len(posicoes):
		cnt+=1
		listaTtls.append(-2)
	
	arquivo = open(fileName,'r')
	for linha in arquivo:
		linha = linha.strip().split('\t')
		inteiroIp = ipParaInteiro(linha[0])
		try:
			if linha[1] != '#':
				ttl = int(linha[1])
			else:
				ttl = -1
		except:
			print linha
		del(linha)
		posicao = posicoes[inteiroIp]
		listaTtls[posicao] = ttl
	arquivo.close()
	return listaTtls

def leDiretorio(diretorio,hitlist,maximo=1000000):
	#Le todos os arquivos de uma coleta e os organiza em uma estrura de dados do tipo
	#(coleta,listaReferencia)
	#coleta[node] = listaTtls
	
	coleta = dict()
	arquivos = glob(diretorio+'/*/*')
	listaReferencia = criaListaReferencia(hitlist)
	posicoes = criaDicionarioPosicoes(listaReferencia)
	
	cnt = 0
	for arquivo in arquivos:
		cnt+=1
		if cnt>maximo:
			break
		node = arquivo.split('/')[-2]
		print node
		coleta[node] = leArquivo(arquivo,posicoes)
	return (coleta,posicoes)

def calculaNumeroHops(ttl):
	#Calcula o número de hops do caminho reverso baseado no valor do ttl.
	#Olha a distancia para a maior potência de 2 maior que o ttl.
	
	nHops = 1
	while nHops<ttl:
		nHops = nHops*2
	nHops = nHops-ttl
	return nHops

def ttlParaHops(experimento):
	#Transforma os Ttls medidos nos experimentos em número de Hops do caminho reverso.
	coleta = experimento[0]
	posicoes = experimento[1]
	
	for node in coleta:
		pos = 0
		while pos<len(coleta[node]):
			ttl = coleta[node][pos]
			if ttl>=0: #Verifica se não houve erros.
				nHops = calculaNumeroHops(ttl)
				coleta[node][pos] = nHops
			pos+=1
	return

def buscaTtl(experimento,host,ip):
	#Busca o Ttl medido pelo par (host,ip)
	inteiroIp = ipParaInteiro(ip)
	posicao = experimento[1][inteiroIp]
	return experimento[0][host][posicao]

def numeroHops(experimento,host,ip):
	#Busca o número de Hops medido pelo par (host,ip).
	#A função é uma cópia de buscaTtl(), mas assume que os ttls já foram
	#transformados em número de Hops na estrutura de dados.
	
	inteiroIp = ipParaInteiro(ip)
	posicao = experimento[1][inteiroIp]
	return experimento[0][host][posicao]

if __name__=='__main__':
	pass
	#Testes de desenvolvimento
	
	'''
	diretorio = '/scratch/geraldo/ic/planetLab/final3/minhaMaquina/coleta'
	hitlist = '/scratch/geraldo/ic/planetLab/final3/analise/hitlist.txt'
	experimento = leDiretorio(diretorio,hitlist,maximo=3)
	ttlParaHops(experimento)
	
	
	print buscaTtl(experimento,'whitefall.planetlab.cs.umd.edu','12.87.83.218')
	print buscaTtl(experimento,'whitefall.planetlab.cs.umd.edu','192.168.20.133')
	print buscaTtl(experimento,'whitefall.planetlab.cs.umd.edu','134.222.104.173')
	print buscaTtl(experimento,'whitefall.planetlab.cs.umd.edu','167.236.64.1')
	print buscaTtl(experimento,'whitefall.planetlab.cs.umd.edu','1.208.149.41')
	'''
	
	
	
