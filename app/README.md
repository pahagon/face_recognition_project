# Face Recognition App 

Aplicação standalone que usa a webcam para detectar faces

## Executando o Projeto com Docker

Este projeto inclui um `Makefile` que automatiza o processo de construção e execução dos contêineres Docker para a aplicação.

P.S Projeto desenvolvido no Ubuntu 24.04.1 LTS

### Passos para Executar com Docker

Antes gere a img base do projeto, existe uma task para isso no diretório pai
```bash
make build
```

1. **Construir a Imagem Docker**:

   ```bash
   make build
   ```
   
2. **Pre-processar as fotos**:
   Copie as fotos que deseja usar para fazer o reconhecimento facil para o diretório photos, depois execute:
   
   ```bash
   make preprocess-photo
   ```
  
3. **Executa a Aplicação**:

   ```bash
   make xhost run-dev
   ```

4. **Parar e Limpar os Contêineres**:

   ```bash
   make stop
   ```

5. **Limpar Tudo (Contêineres, Volumes e Imagens)**:

   ```bash
   make clean
   ```
 
Por padrão, se vc colocar uma foto do obama na frente da webcam a aplicação irá reconhecer e colocar o nome obama na tela.

Se quiser, vc pode adicinar mais fotos no diretório photos e execute o comando, ```make preprocess-photo```
