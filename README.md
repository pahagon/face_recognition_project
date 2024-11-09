# Face Recognition Project

Este é um projeto de reconhecimento facial que utiliza webcam e modelos pré-treinados.

## Funcionalidades

- Carregamento e pré-processamento de imagens faciais.
- Extração de embeddings faciais usando o modelo pré-treinado.
- Comparação de embeddings para autenticação ou verificação de identidade.

## Requisitos

- **Python 3.8+**
- **Docker** 
- **Bibliotecas Python**:
  - `face_recognition`
  - `psycopg2`
  - `opencv-python-headless`
  - `dlib`

## Estrutura do Projeto

```plaintext
face_recognition_project/
│
├── app/
│   ├── face_recognition     # Lib que facilita o uso da dlib
│   ├── photos               # Diretórios com as fotos que serão usadas para o reconhecimento facial
│   ├── Dockerfile           # Dockerfile para a aplicação Python
│   ├── Makefile             # Automatização o processo de construção dos contêiners Docker 
│   ├── main.py              # Código principal da aplicação Python
│   ├── preprocess_photo.py  # Código que préprocessa as fotos que serão usadas durante o excecussão da aplicação principal
│   └── requirements.txt     # Dependências Python
└── README.md                # Documentação do projeto
```

## Executando o Projeto com Docker

Este projeto inclui um `Makefile` que automatiza o processo de construção e execução dos contêineres Docker para a aplicação.

P.S Projeto desenvolvido no Ubuntu 24.04.1 LTS

### Passos para Executar com Docker

1. **Construir a Imagem Docker**:

   ```bash
   make build-base-img build
   ```
   
2. **Pre-processar as fotos**:
   Copie as fotos que deseja usar para fazer o reconhecimento facil para o diretório photos, depois execute:
   
   ```bash
   make preprocess-photo
   ```
  
3. **Iniciar a Aplicação Python**:

   ```bash
   make xhost run-dev
   ```

. **Parar e Limpar os Contêineres**:

   ```bash
   make stop
   ```

. **Limpar Tudo (Contêineres, Volumes e Imagens)**:

   ```bash
   make clean
   ```
   
## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Commit suas alterações (`git commit -m 'Adiciona minha feature'`).
4. Faça um push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
