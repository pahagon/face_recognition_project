# Face Recognition Project

Este é um projeto de reconhecimento facial que utiliza webcam e modelos pré-treinados.

## Funcionalidades

- Carregamento e pré-processamento de imagens faciais.
- Extração de embeddings faciais usando o modelo pré-treinado.
- Comparação de embeddings para autenticação ou verificação de identidade.


## Estrutura do Projeto

```plaintext
face_recognition_project/
│
├── app/                     # Aplicação standalone que usa a webcam para detectar faces
├── face_recognition         # Lib que facilita o uso da dlib
├── photos                   # Diretórios com as fotos que serão usadas para o reconhecimento facial
└── web/                     # Aplicação web que usa a webcam para detectar faces
```
## Criando a imagem Docker base de todos os projetos 

```bash
make build
```

## Contribuição
Contribuições são bem-vindas! 

O Projeto foi desenvolvido usando Ubuntu 24.04.1 LTS

### Requisitos

- **Python 3.9+**
- **Docker**
- **MiniKube**
- **Helm**

Você pode instalar as dependências usando o comando:
```bash
make install-deps
```

A task vai usar uma receita ansible que vc pode usar para instalar todas as dependências para desenvolvimento.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
