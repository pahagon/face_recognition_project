import cv2
import numpy as np
import os
import glob

def preprocess_photo(image_path, target_size=(160, 160)):
    """
    Carrega e processa uma imagem para ser usada no modelo de reconhecimento facial
    e a salva no mesmo local.

    Parâmetros:
    - image_path: Caminho para a imagem a ser processada.
    - target_size: Tamanho final da imagem (largura, altura) em pixels. O padrão é 160x160.

    Retorna:
    - imagem processada como um array NumPy no formato correto.
    """
    # Carrega a imagem usando OpenCV
    image = cv2.imread(image_path)

    # Verifica se a imagem foi carregada corretamente
    if image is None:
        raise ValueError(f"A imagem em {image_path} não pôde ser carregada.")

    # Converte a imagem para o espaço de cor RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Redimensiona a imagem para o tamanho desejado
    #image = cv2.resize(image, target_size)

    # Converte a imagem para float32 e normaliza os valores de pixel
    image = np.asarray(image, dtype=np.float32)
    mean, std = image.mean(), image.std()
    image = (image - mean) / std  # Normaliza a imagem para zero-mean e unit-variance

    # Expande a dimensão para incluir o batch size (1, largura, altura, canais)
    image_batch = np.expand_dims(image, axis=0)

    # Processa para o modelo
    processed_image = image_batch

    # Prepara a imagem para salvar removendo a normalização
    image_to_save = (image * std + mean)  # Desfaz a normalização para salvar
    image_to_save = np.clip(image_to_save, 0, 255).astype(np.uint8)  # Garante valores de pixel entre 0 e 255
    image_to_save = cv2.cvtColor(image_to_save, cv2.COLOR_RGB2BGR)  # Converte para BGR para salvar com OpenCV

    # Salva a imagem processada no mesmo local
    cv2.imwrite(image_path, image_to_save)
    print(f"Imagem processada salva em: {image_path}")

    return processed_image

for f in glob.glob(os.path.join("photos/", "*.jpg")):
    preprocess_photo(f)
