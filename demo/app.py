import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field
import io

# --- 1. Configuração de Ambiente ---
# Defina o caminho do seu arquivo.env aqui
ENV_FILE_PATH = "./.env"
# Defina o caminho do seu dataset aqui
DATASET_PATH = "../data/erro" 

# Tenta carregar as variáveis de ambiente
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Recupera a chave da API
API_KEY = os.getenv("GEMINI_API_KEY")

# Lógica para carregar classes
if os.path.exists(DATASET_PATH):
    try:
        ARTIST_CLASSES = os.listdir(DATASET_PATH)
        ARTIST_CLASSES = [name.replace("_", " ") for name in ARTIST_CLASSES]
        ARTIST_CLASSES.sort()
    except Exception as e:
        st.error(f"Erro ao ler diretório para obter classes: {e}")
        ARTIST_CLASSES = []
else:
    # Fallback se a pasta não existir
    ARTIST_CLASSES = [
        "Albrecht Durer", "Alfred Sisley", "Claude Monet", "Edgar Degas", 
        "Francisco Goya", "Frida Kahlo", "Gustav Klimt", "Leonardo da Vinci", 
        "Pablo Picasso", "Paul Gauguin", "Paul Klee", "Pierre-Auguste Renoir", 
        "Rembrandt", "Salvador Dali", "Titian", "Vincent van Gogh"
    ]

# print(ARTIST_CLASSES)
ARTIST_NAMES = ', '.join(ARTIST_CLASSES)

# --- 2. Configuração da Página Streamlit ---
st.set_page_config(
    page_title="Art Curator AI Demo",
    page_icon="🎨",
    layout="wide"
)

# --- 3. Definição do Schema de Saída (Pydantic) ---
class ArtAnalysis(BaseModel):
    artist_name: str = Field(description="Nome do artista identificado")
    art_movement: str = Field(description="Movimento artístico (ex: Impressionismo, Renascimento)")
    confidence_score: float = Field(description="Nível de confiança de 0.0 a 1.0")
    visual_evidence: list[str] = Field(description="Lista de 3 a 5 elementos visuais chave (pinceladas, luz, composição) que justificam a decisão")
    year_approx: str = Field(description="Ano estimado ou período da obra")

# --- 4. Interface Lateral ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png", width=150)
    st.markdown("### Status do Sistema")
    
    # Verifica se a chave foi carregada corretamente
    if API_KEY:
        st.success("API Key carregada com sucesso via.env")
    else:
        st.error("API Key não encontrada!")
        st.info(f"Certifique-se de que o arquivo `.env` existe e contém a variável `GOOGLE_API_KEY`.")
    
    st.markdown("---")
    st.write("**Modelo:** Gemini 2.5 Flash")
    st.write("**Modo:** Thinking + Structured Output")

    st.markdown("---")
    st.markdown("Inspiração de Artistas para Classificar")
    st.markdown(ARTIST_NAMES)

# --- 5. Corpo Principal da Aplicação ---
st.title("🏛️ Classificador de Obras de Arte Zero-Shot")
st.markdown("""
Esta demonstração utiliza o **Gemini 2.5 Flash** para atuar como um historiador da arte.
O modelo analisa a imagem visualmente e utiliza seu conhecimento prévio para classificar o autor e o estilo,
exibindo o **raciocínio passo-a-passo** antes da conclusão.
""")

uploaded_file = st.file_uploader("Faça upload da imagem da pintura", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Layout de duas colunas: Imagem vs. Resultado
    col1, col2 = st.columns([1, 1.2])
    
    # Carregar imagem para visualização e para a API
    image = Image.open(uploaded_file)
    
    with col1:
        st.image(image, caption="Obra para Análise", width='stretch')

    with col2:
        if not API_KEY:
            st.warning("⚠️ Configure o arquivo.env para prosseguir.")
        else:
            analyze_btn = st.button("🔍 Analisar Obra com IA", type="secondary")
            
            if analyze_btn:
                try:
                    with st.spinner('O Gemini está analisando a técnica, paleta e composição...'):
                        
                        # Inicializa o cliente com a chave do.env
                        client = genai.Client(api_key=API_KEY)
                        
                        # # Prompt de especialista
                        prompt = f"""
                        Você é um especialista em história da arte. Analise esta imagem com extrema atenção aos detalhes.
                        Identifique o artista, o movimento e explique o porquê baseado em evidências visuais (pinceladas, luz, tema).
                        Você deve escolhe APENAS UM artista dessa lista:
                        {ARTIST_CLASSES}
                        """
                        
                        # Chamada ao modelo
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[image, prompt],
                            config=types.GenerateContentConfig(
                                thinking_config=types.ThinkingConfig(include_thoughts=True),
                                response_mime_type="application/json",
                                response_schema=ArtAnalysis,
                                temperature=0.0
                            )
                        )
                        
                        # Processamento da resposta (Thinking vs JSON)
                        thought_trace = ""
                        final_json = ""

                        # Itera sobre as partes para separar o pensamento do JSON final
                        for part in response.candidates[0].content.parts:
                            if part.thought:
                                thought_trace += part.text + "\n"
                            else:
                                final_json += part.text

                        # Exibe o Resultado Final
                        try:
                            result = json.loads(final_json)
                        except Exception as e:
                            st.warning(f"⚠️Erro ao converter JSON da imagem. {e}\JSON recebido: {response.text}")
                            # print(f"Erro ao converter JSON da imagem. {e}\JSON recebido: {json_dict}")
                        
                        st.divider()
                        st.subheader(f"🎨 Atribuição: {result['artist_name']}")
                        st.caption(f"Movimento: {result['art_movement']} | Período: {result['year_approx']}")
                        
                        # Métricas visuais
                        score = result['confidence_score']
                        if score > 0.85:
                            st.success(f"Alta Confiança: {score:.1%}")
                        elif score > 0.5:
                            st.warning(f"Média Confiança: {score:.1%}")
                        else:
                            st.error(f"Baixa Confiança: {score:.1%}")

                        st.markdown("#### Evidências Visuais Identificadas:")
                        for evidence in result['visual_evidence']:
                            st.markdown(f"- {evidence}")
                        
                        # Exibe o Raciocínio (Expandable)
                        with st.expander("🧠 Ver Raciocínio do Modelo (Chain-of-Thought)", expanded=True):
                            if thought_trace:
                                st.markdown(thought_trace)
                            else:
                                st.info("O modelo gerou a resposta direta sem trilha de pensamento visível.")

                except Exception as e:

                    st.error(f"Ocorreu um erro na análise: {str(e)}")
