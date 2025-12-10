# 🎨 Art Curator LMM: Anotação Automática com Modelos Multimodais

## 📄 Sobre o Projeto
Este repositório contém o código fonte e os experimentos desenvolvidos para o projeto de **Anotação Automática de Imagens com Modelos Multimodais**.

O objetivo principal é investigar a viabilidade do uso de Grandes Modelos Multimodais (LMMs), especificamente o **Gemini 2.5 Flash**, para atuar como ferramentas de curadoria de dados.

Através de uma abordagem **Zero-Shot** com **Chain-of-Thought** (Cadeia de Pensamento), o sistema classifica obras de arte, identifica movimentos artísticos e fornece justificativas visuais, transformando o papel humano de "anotador" para "revisor".

## ✨ Funcionalidades

* **Pipeline de Classificação Zero-Shot:** Classificação direta via API sem necessidade de treinamento (fine-tuning).
* **Saída Estruturada (JSON):** Garantia de consistência nos dados gerados para fácil integração em bancos de dados.
* **Demo Interativa:** Aplicação web em Streamlit para análise de obras em tempo real.
* **Robustez:** Testado em cenários de alta disponibilidade (10 classes) e cauda longa (47 classes).

## 📊 Resultados dos Experimentos

O projeto utilizou o dataset **Best Artworks of All Time** e foi dividido em dois cenários experimentais:

| Experimento | Qtd. Artistas | Total Imagens | Acurácia | F1-Score (Macro) |
| :--- | :---: | :---: | :---: | :---: |
| **Exp 1 (Top 10)** | 10 | 2.500 | 93.63% | 0.9358 |
| **Exp 2 (Complexo)** | 47 | 2.115 | 83.85% | 0.8373 |

Os resultados demonstram que o modelo é capaz de distinguir nuances estilísticas complexas, alcançando F1-Score de **0.99** para artistas com identidade visual forte como Paul Klee e El Greco.

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.9 ou superior.
* Uma chave de API do Google AI Studio (Gemini).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/larissa3Xavier/multimodal-art-classifier.git](https://github.com/larissa3Xavier/multimodal-art-classifier.git)
    cd multimodal-art-classifier
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione sua chave:
    ```env
    GEMINI_API_KEY="sua_chave_api_aqui"
    ```

### Rodando a Demo (Streamlit)
Para iniciar a interface web de demonstração:

```bash
streamlit run app.py

👩‍💻 Autora
Larissa Silva Xavier Rosa, Universidade Federal de Goiás (UFG).
Projeto desenvolvido sob orientação do Prof. Adriano César Santana.
Este projeto é estritamente acadêmico e utiliza o modelo Gemini via API, sujeito aos termos de uso da Google.
