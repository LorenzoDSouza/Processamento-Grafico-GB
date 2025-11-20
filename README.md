# Processamento Gráfico: Fundamentos 2025/2

Repositório com o projeto desenvolvido para a Atividade Acadêmica **Processamento Gráfico: Fundamentos**, parte do curso de graduação em **Ciência da Computação da Unisinos**.

👥 **Integrantes do grupo:**  
- Arthur Shallemberger  
- Leonardo Fronza  
- Lorenzo de Souza  

---

## 📂 Estrutura do Repositório

| Projeto                  | Linguagem / Biblioteca | Descrição breve |
| ------------------------ | -------------------- | ---------------- |
| `Trabalho Grau B`        | Python / OpenCV + Tkinter | Protótipo de **editor de imagens e vídeo**, inspirado nos “stories” do Instagram. Permite capturar vídeo da webcam, aplicar filtros em tempo real, utilizar stickers e salvar imagens processadas. |

---

## 🧩 Descrição do Projeto — *Editor de Imagem e Vídeo*

O **Editor de Imagem e Vídeo** é uma aplicação desktop desenvolvida em **Python** com **OpenCV** e **Tkinter**, que permite ao usuário:

- Capturar **vídeo em tempo real** da webcam.  
- Carregar imagens estáticas do disco (modo foto).  
- Aplicar **10 filtros diferentes**, incluindo:
  - Blur (Gaussian, Median)  
  - Sharpen  
  - Laplaciano  
  - Canny  
  - Isolamento de canais (R, G, B)  
  - Grayscale  
- Aplicar **stickers** com transparência sobre imagens ou vídeo.  
- Realizar **operações matemáticas** entre imagens (adição, subtração, blending).  
- **Salvar** o resultado da imagem ou frame do vídeo.  
- **Resetar** para a imagem original.  
- (Opcional) Detecção de rosto usando Haar Cascade para posicionamento automático de stickers.  

A interface gráfica é implementada com **Tkinter**, apresentando o vídeo em tempo real e **botões para alternar filtros**, tirar foto e resetar a imagem.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.11+**  
- **OpenCV** (`opencv-python` / `opencv-contrib-python`) — processamento de imagens e vídeo.  
- **Tkinter** — interface gráfica e botões.  
- **Pillow (PIL)** — conversão de imagens para exibição em Tkinter.  

---

## 📂 Estrutura do Projeto

- `main.py` — código principal, responsável pelo loop de vídeo, aplicação de filtros, interface Tkinter e manipulação de imagens.  
- `haarcascade_frontalface_default.xml` — classificador Haar Cascade pré-treinado para detecção de faces (opcional para stickers).  
- `assets/` — pasta com imagens de stickers e outros recursos gráficos.  

---

## 💡 Observações

- Projeto desenvolvido para a disciplina **Processamento Gráfico: Fundamentos**, 2025/2.  
- O sistema foi testado e executado em **Windows** e **Linux** com Python 3.  
- A interface busca equilibrar **simplicidade** com funcionalidade, priorizando o **processamento de imagens** como foco principal.  
- Este repositório deve ser entregue via **link do GitHub** conforme as instruções da disciplina, com README, .gitignore e código organizado.  

> O projeto é modular e pode ser expandido com funcionalidades extras, como stickers animados, múltiplos filtros em sequência ou integração com detecção de rosto para efeitos automáticos.
