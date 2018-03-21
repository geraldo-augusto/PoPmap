#encoding:utf-8

import sys
import subprocess
import threading
from collections import defaultdict
from time import sleep

def ping(ip,nTentativas,dicionario,sinal,trava):
	#Faz nTentativas de medir o ttl reverso do ip dado, seja ipv4 ou ipv6. Ao conseguir uma
	#medição bem sucedida, as tentativas param.
	#O resultado é salvo em dicionario[ip].
	#sinal: avisa que a medição para o IP terminou
	#trava: usada para escrever com segurança no dicionário.
	
	#Define a versão do IP
	if ':' in ip:
		versaoIp = 6
	else:
		versaoIp = 4
	
	tentativa=1
	while tentativa<=nTentativas:
		#Realiza a medição
		if versaoIp==4:
			retorno = subprocess.Popen(['ping -c 1 -w 1 %s'%ip],shell=True,stdout=subprocess.PIPE).communicate()[0]
		if versaoIp==6:
			retorno = subprocess.Popen(['ping6 -c 1 -w 1 %s'%ip],shell=True,stdout=subprocess.PIPE).communicate()[0]
		retorno = retorno.strip().split('\n')
		retorno = retorno[1]
		
		#Determina o timeStamp da medição
		timeStamp = subprocess.Popen(['date -u +"%Y%m%d%H%M%S"'],shell=True,stdout=subprocess.PIPE).communicate()[0]
		timeStamp = timeStamp.strip().split('\n')
		timeStamp = timeStamp[0]
		
		#Extrai o ttl da medicão
		if retorno=='' or retorno.startswith('From'):
			if tentativa==nTentativas:
				ttl = '#'
				rtt = '#'
				break
			else:
				tentativa+=1
				continue
		else:
			ttl = retorno[retorno.index('ttl=')+4:retorno.index('time=')-1]
			rtt = retorno[retorno.index('time=')+5:]
			break
	del(retorno)
	
	#Escreve o ttl no dicionário, usando uma trava por segurança.
	trava.acquire()
	dicionario[ip] = (ttl,timeStamp,rtt)
	trava.release()
	#Retorna avisando que terminou com o sinal.
	sinal.set()
	return

def medicaoConjunto(listaIps,nTentativas,taxaMedicoes,dicionario):
	#Realiza as medições para um subconjunto dos IPs, foi criada para limitar o número de threads.
	#O resultado é escrito diretamente no dicionário principal.
	
	threads = []
	sinais = []
	trava = threading.Lock()
	intervalo = float(1)/float(taxaMedicoes)
	
	#n=1
	for ip in listaIps:
		#print '>>>>>' + str(n) + '>>>>>' + ip
		#Cria uma nova thread para realizar a medição.
		sinal = threading.Event()
		t = threading.Thread(target=ping,args=(ip,nTentativas,dicionario,sinal,trava))
		threads.append(t)
		sinais.append(sinal)
		t.start()
		sleep(intervalo)
		#n+=1
	
	#Espera as threads terminarem.
	for sinal in sinais:
		sinal.wait(timeout=5*nTentativas)
	return
		

def fazMedicoes(fileNameHitlist,fileNameSaida,taxaMedicoes,nTentativas):
	#Cria lista de ips na RAM para evitar acessar o disco o tempo todo.
	arquivoEntrada = open(fileNameHitlist,'r')
	todosIps = []
	for ip in arquivoEntrada:
		ip = ip.strip()
		todosIps.append(ip)
	arquivoEntrada.close()
	
	#Realiza as medições
	resultados = dict()
	listaIps = []
	tamanhoLista = 2*taxaMedicoes
	for ip in todosIps:
		ip = ip.strip()
		listaIps.append(ip)
		if len(listaIps) == tamanhoLista:
			medicaoConjunto(listaIps,nTentativas,taxaMedicoes,resultados)
			#Escrever no arquivo de saída e reinicia o dicionário resultados.
			escreveSaida(resultados,fileNameSaida)
			resultados.clear()
			listaIps = []
	if len(listaIps) > 0:
		medicaoConjunto(listaIps,nTentativas,taxaMedicoes,resultados)
		#Escrever no arquivo de saída e reinicia o dicionário resultados.
		escreveSaida(resultados,fileNameSaida)
		resultados.clear()
		listaIps = []
	
	return

def escreveSaida(resultados,fileNameSaida):
	arquivo = open(fileNameSaida,'a')
	for ip in resultados:
		arquivo.write('%s\t%s\t%s\t%s\n'%(ip,resultados[ip][0],resultados[ip][1],resultados[ip][2]))
	arquivo.close()


if __name__=='__main__':
	if len(sys.argv)<4:
		print 'Uso: python fazMedicoes.py fileHitList fileSaida taxaMedicoes'
	else:
		fileNameHitlist = sys.argv[1]
		fileNameSaida = sys.argv[2]
		taxaMedicoes = int(sys.argv[3])
		fazMedicoes(fileNameHitlist,fileNameSaida,taxaMedicoes,3)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
