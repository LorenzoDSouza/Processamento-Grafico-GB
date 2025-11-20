# Processamento Gráfico: Fundamentos 2025/2

Repositório com o projeto desenvolvido para a Atividade Acadêmica **Processamento Gráfico: Fundamentos**, parte do curso de graduação em **Ciência da Computação da Unisinos**.

👥 **Integrantes do grupo:**  
- Arthur Shallemberger  
- Leonardo Fronza  
- Lorenzo de Souza  

---

## 📂 Estrutura do Repositório

| Projeto             | Engine / Linguagem | Descrição breve |
| ------------------- | ------------------ | ---------------- |
| `Trabalho Grau A`   | C++ / OpenGL       | Desenvolvimento do jogo **“Jogo do Gênio”**, utilizando OpenGL, GLFW, GLAD e shaders personalizados. O projeto aplica conceitos de renderização 2D, texturas e detecção de colisões em tempo real. |

---

## 🧩 Descrição do Projeto — *Jogo do Gênio*

O **Jogo do Gênio** é um jogo 2D desenvolvido em **C++** com **OpenGL**, onde o jogador controla um gênio posicionado na parte inferior da tela e deve **coletar lâmpadas que caem do topo**.

Cada lâmpada coletada **incrementa a pontuação** do jogador.  
Quando o gênio atinge **20 lâmpadas coletadas**, o jogo reconhece a vitória e exibe a mensagem correspondente.

O sistema utiliza:  
- **OpenGL** para renderização das texturas e sprites.  
- **GLFW** para controle da janela e entrada do teclado.  
- **GLAD** para o carregamento de funções modernas do OpenGL.  
- **stb_image** para carregamento das imagens (texturas dos sprites e fundo).  
- **Shaders (GLSL)** para controle da renderização e efeitos gráficos.

A estrutura do projeto é dividida em módulos:  
- `assets/` — imagens e texturas (background, jogador, lâmpadas).  
- `include/` e `Common/` — cabeçalhos e dependências externas.  
- `src/` — código-fonte principal (controle do jogo, renderização e lógica).  
- `shaders/` — arquivos de vertex e fragment shader.  

---

## 💡 Observações

- Trabalho desenvolvido para a disciplina **Processamento Gráfico: Fundamentos**, ministrada em 2025/2.  
- Projeto implementado em **C++17** com o sistema de build **CMake**.  
- O jogo foi testado e executado em ambiente **Windows** utilizando **Visual Studio Code** e **MinGW**.

> Este repositório deverá permanecer **público** até o final da disciplina para fins de avaliação.  
> Organização e clareza são essenciais, podendo este projeto ser expandido como parte de um **portfólio pessoal**.
