# PoPmap

### Dependências:



### Siga os seguintes passos:

1. Crie um diretorio para guardar uma nova medição do planetLab:

   ```$ mkdir ~/medicaoPl```
	
1. Crie uma lista de IPs para medir, com um IP por linha.

   * Um exemplo de lista de IPs está em [link](exemplos/hitlist.txt)

1. Crie uma lista dos hosts dos computadores usados para medição, com um hostname por linha.
   * Um exemplo de lista de hosts está em exemplos/nodelist.txt

1. Crie uma nova medição para o PlanetLab com:

   * Formato:
	
        ```$ python criaMedicao.py diretorioMedicao arquivoHitlist taxaMedicoes sliceName```

   * Exemplo:
	
       ```$ python criaMedicao.py ~/medicaoPl ./exemplos/hitlist.txt 10 ufmg_cipops```

   * Observações:
	
      1. diretorioMedicao é o diretorio criado no item 1
      1. arquivoHitlist é a lista de IPs do item 2
      1. taxaMedicoes = quantos IPs serão medidos por segundo
      1. sliceName é o nome do usuário que irá logar nas máquinas remotas, no caso do planetLab é o nome do slice
      1. Serão criados dois diretorios. O 'diretorioLocal' guardará as ferramentas e os dados coletados. O 'diretorioRemoto' contém os arquivos que serão copiados para o diretorio remoto.

1. Adicione a sua chave privada no ssh-agent
   
   * Exemplo:

	   ```$ ssh-add ~/.ssh/planetlab/id_rsa```
	
1. Copie os arquivo para os computadores remotos com:

   * Formato:
   
      ```$ diretorioLocal/copy.sh -i NODELIST -l SLICE -d BASEDIR```
   * Exemplo:
   
      ```$ ~/medicaoPl/diretorioLocal/copy.sh -i ./exemplos/nodelist.txt -l ufmg_cipops -d ~/medicaoPl/diretorioRemoto```
   * Observações:
	
       1. NODELIST foi criada no item 3
	   1. SLICE é o nome do usuário que irá logar nas máquinas remotas
	   1. BASEDIR é a pasta 'diretorioLocal' criada dentro da pasta do experimento.

1. Inicie as medições com:

   * Formato:
   
      ```$ diretorioLocal/startrun.sh -i NODELIST -l SLICE```
   
   * Exemplo:
   
      ```$ ~/medicaoPl/diretorioLocal/startrun.sh -i ./exemplos/nodelist.txt -l ufmg_cipops```

1. Depois de terminadas as medições, faça download com:
   
   * Formato:
   
      ```$ diretorioLocal/dldata.sh -i NODELIST -l SLICE -d REMOTEDIR -s DOWNLOADDIR -k RSAKEY -L LOGDIR```
   
   * Exemplo:
	   
       ```$ ~/medicaoPl/diretorioLocal/dldata.sh -i ./exemplos/nodelist.txt -l ufmg_cipops -d /home/ufmg_cipops/resultados -s ~/medicaoPl/diretorioLocal/coleta -k ~/.ssh/planetlab/id_rsa -L ./medicaoPl/diretorioLocal/log```

   * Observações:
   
      1. REMOTEDIR: usar /home/nome_do_slice/resultados
      1. DOWNLOADDIR: usar diretorioLocal/coleta
      1. RSAKEY: a chave privada usada para logar nos computadores via SSH
      1. LOGDIR: usar diretorioLocal/log

1. Dados coletados:
   * Depois de seguir os passos, haverá dentro de diretorioLocal/coleta uma pasta para cada computador remoto. Cada pasta conterá um arquivo com as medições.
   * Cada Linha tem o seguinte formato: ```IP    TTL    TIMESTAMP    RTT```
   * Você também pode criar essa estrutura de diretórios usando outras medições e seguir os próximos passos para fazer o agrupamento.

1. Execute o agrupamento das interfaces:

   * Formato:
      
      ```$ python clusteriza.py diretorioColeta hitlistColeta numeroClusters numeroComponentes```
   
   * Exemplo:
      
      ```$ python clusteriza.py ~/medicaoPl/diretorioLocal/coleta exemplos/hitlist.txt 5 3```
   
   * Observações:
   
      1. numeroCluster: é o valor de k no algoritmo k-Means.
      1. numeroComponentes: é quantidade de componentes principais restantes depois do PCA.
      1. O resultado aparece na pasta out/saidaK em que K é o numero de clusters escolhido.
      1. Deve-se rodar o algoritmo diversas vezes para determinar o K

1. É criado um arquivo chamado clusters.txt na pasta out/saidaK. Cada linha possui o seguinte formato:
   * Formato:
      ```$ (IdCluster)\t(lista de ips separados por vírgula)```
