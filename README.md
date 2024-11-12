# Face Recognition Project

Este é um projeto de reconhecimento facial que utiliza webcam e modelos pré-treinados.

## Funcionalidades

- Carregamento e pré-processamento de imagens faciais.
- Extração de embeddings faciais usando o modelo pré-treinado.
- Comparação de embeddings para autenticação ou verificação de identidade.

## Requisitos

- **Python 3.9+**
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

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Commit suas alterações (`git commit -m 'Adiciona minha feature'`).
4. Faça um push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
