# PoPmap (Em construção..., pronto até 22/04)


Siga os seguintes passos:

1)Crie um diretorio para guardar uma nova medição do planetLab:  
	*>>> mkdir ~/medicaoPl  
	
2)Crie uma lista de IPs para medir, com um IP por linha.  
	>>> Um exemplo de lista de IPs está em exemplos/hitlist.txt  

3)Crie uma lista dos hosts dos computadores usados para medição, com um hostname por linha.  
	>>> Um exemplo de lista de hosts está em exemplos/nodelist.txt  

4)Crie uma nova medição para o PlanetLab com:  
	Formato:  
	>>> python criaMedicao.py diretorioMedicao arquivoHitlist taxaMedicoes sliceName  
	Exemplo:  
	>>> python criaMedicao.py ~/medicaoPl ./exemplos/hitlist.txt 10 ufmg_cipops  
	Observações:  
	a)diretorioMedicao é o diretorio criado no item 1  
	b)arquivoHitlist é a lista de IPs do item 2  
	c)taxaMedicoes = quantos IPs serão medidos por segundo  
	d)sliceName é o nome do usuário que irá logar nas máquinas remotas, no caso do planetLab é o nome do slice  
	e)Serão criados dois diretorios. O 'diretorioLocal' guardará as ferramentas e os dados coletados. O 'diretorioRemoto' contém os arquivos que serão copiados para o diretorio remoto.  

5)Adicione a sua chave privada no ssh-agent  
	Exemplo:  
	>>> ssh-add ~/.ssh/planetlab/id_rsa  
	
5)Copie os arquivo para os computadores remotos com:  
	Formato:  
	>>> diretorioLocal/copy.sh -i NODELIST -l SLICE -d BASEDIR  
	Exemplo:  
	>>> ~/medicaoPl/diretorioLocal/copy.sh -i ./exemplos/nodelist.txt -l ufmg_cipops -d ~/medicaoPl/diretorioRemoto  
	Observações:  
	a)NODELIST foi criada no item 3  
	b)SLICE é o nome do usuário que irá logar nas máquinas remotas  
	c) BASEDIR é a pasta 'diretorioLocal' criada dentro da pasta do experimento.  

6)Inicie as medições com:  
	Formato:  
	>>> diretorioLocal/startrun.sh -i NODELIST -l SLICE  
	Exemplo:  
	~/medicaoPl/diretorioLocal/startrun.sh -i ./exemplos/nodelist.txt -l ufmg_cipops  

7)Depois de terminadas as medições, faça download com:  
	Formato:  
	>>> diretorioLocal/dldata.sh -i NODELIST -l SLICE -d REMOTEDIR -s DOWNLOADDIR -k RSAKEY -L LOGDIR  
	Exemplo:  
	>>> ~/medicaoPl/diretorioLocal/dldata.sh -i ./exemplos/nodelist.txt -l ufmg_cipops -d /home/ufmg_cipops/resultados -s ~/medicaoPl/diretorioLocal/coleta -k ~/.ssh/planetlab/id_rsa -L ./medicaoPl/diretorioLocal/log  
	Observações:  
	a)REMOTEDIR: usar /home/nome_do_slice/resultados  
	b)DOWNLOADDIR: usar diretorioLocal/coleta  
	c)RSAKEY: a chave privada usada para logar nos computadores via SSH  
	d)LOGDIR: usar diretorioLocal/log  

8)Depois de seguir os passos, haverá dentro de diretorioLocal/coleta uma pasta para cada computador remoto. Cada pasta conterá um arquivo com as medições.  
Cada Linha tem o seguinte formato: IP    TTL    TIMESTAMP    RTT  
Você também pode criar essa estrutura de diretórios usando outras medições e seguir os próximos passos para fazer o agrupamento.  

9)Obter a matriz necessária para o algoritmo de agrupamento  
	Formato:  
	>>> python ./cluster/obtemMatriz.py diretorioColeta hitlistColeta diretorioSaida  
	Exemplo:  
	>>> python ./cluster/obtemMatriz.py ~/medicaoPl/diretorioLocal/coleta ./exemplos/hitlist.txt ./cluster  




































