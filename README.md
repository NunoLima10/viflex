# Viflex 

## Baixe vídeos e musicas do You Tube pelo seu terminal

### Instalação 

> - Baixe o executável  
> - Descomprimir o arquivo 
> - Coloque o endereço da pasta na [variável de ambiente](https://knowledge.autodesk.com/pt-br/support/navisworks-products/troubleshooting/caas/sfdcarticles/sfdcarticles/PTB/Adding-folder-path-to-Windows-PATH-environment-variable.html) ``PATH`` (opcional)
 
 --- 
 
 ### Como usar
 > - Abra o terminal no diretório onde deseja guardar o arquivo 
 > - Siga a seguinte estrutura para baixar apenas o video 
 >```
 >viflex -v "link do vídeo entre aspas"
> ```
>
> - Siga a seguinte estrutura para baixar apenas o áudio 
>```
>viflex -a "link do vídeo entre aspas"
> ```
--- 
### Observações 
> - Video será baixado automaticamente com melhor qualidade disponível 
> - Caso não tenha colocado o endereço da pasta na variável de ambiente você apenas pode executar os comandos no mesmo diretório  do executável 
> - Se omitir os parâmetros -v e -a  automaticamente será baixado apenas o video  
>```
>viflex "link do vídeo entre aspas"
>```
 
