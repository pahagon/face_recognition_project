# Face Recognition Web

Aplicação web que usa a webcam para detectar faces

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

2. **Subir servidor que serve os assets**:

   ```bash
   make dev-web-server
   ```

2. **Executa a Aplicação**:

   ```bash
   make run-dev
   ```
   
Abrir no browser http://localhost:8000

Por padrão, se vc colocar uma foto do obama na frente da webcam a aplicação irá reconhecer e colocar o nome obama na tela.

Para reconhecer mais faces, você pode adicinar fotos no diretório photos e execute o comando, ```make preprocess-photo``` que está disponível no diretório app no diretório raiz.
