import streamlit as st
import pandas as pd
from data_processing import DataProcessor
from modeling import ClimateModel
from visualization import Visualizer

# Inicialização das classes
data_processor = DataProcessor()
climate_model = ClimateModel()
visualizer = Visualizer()

# --- UI 1: Administração - Download e Processamento ---

def ui_administracao():
    st.header("📊 Administração - Download e Processamento de Dados")
    
    st.markdown("""
    Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul.
    Os dados serão baixados do INPE e processados para análise.
    """)
    
    # Verificar status atual
    status = data_processor.check_data_status()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Diretório de Dados", data_processor.DATA_DIR, "Existe" if status['dir_exists'] else "Não Existe")
    col2.metric("Arquivo ZIP", data_processor.ZIP_FILENAME, "Existe" if status['zip_exists'] else "Não Existe")
    col3.metric("Log de Processamento", "model_creation.log", "Criado" if status['model_created'] else "Não Criado")
    
    st.markdown("---")
    
    if st.button("🔄 Iniciar/Verificar Processamento de Dados"):
        st.session_state.processar_dados = True
        
    if st.session_state.processar_dados:
        if data_processor.download_and_process_data():
            st.session_state.dados_processados = True
            # Chamada corrigida: passar a instância como argumento
            st.session_state.df_clean = DataProcessor.process_worldclim_data(data_processor)
            st.session_state.processar_dados = False  # Finaliza o processo
            st.rerun()  # Usar st.rerun() em vez de st.experimental_rerun() para versões mais recentes

# --- UI 2: Análise Estatística Exploratória ---

def ui_analise_estatistica():
    st.header("🔍 Análise Estatística Exploratória")
    
    if 'df_clean' not in st.session_state or st.session_state.df_clean is None:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    df_clean = st.session_state.df_clean
    
    st.subheader("Amostra dos Dados Processados")
    st.dataframe(df_clean.head())
    
    st.subheader("Estatísticas Descritivas")
    st.dataframe(df_clean.describe().T)
    
    st.subheader("Matriz de Correlação")
    corr_matrix = df_clean.drop(columns=['row', 'col']).corr()
    st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'))

# --- UI 3: Modelagem: Regressão Linear Múltipla ---

def ui_modelagem():
    st.header("🧠 Modelagem: Regressão Linear Múltipla")
    
    if 'df_clean' not in st.session_state or st.session_state.df_clean is None:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    df_clean = st.session_state.df_clean
    
    st.markdown("""
    Será treinada uma Regressão Linear Múltipla para prever a **Temperatura Média Anual (BIO1)**
    com base na **Precipitação Anual (BIO12)** e na **Sazonalidade da Temperatura (BIO4)**.
    """)
    
    if st.button("🚀 Treinar Modelo"):
        try:
            model, metrics, predictions, test_data = climate_model.train_model(df_clean)
            
            st.session_state.model = model
            st.session_state.metrics = metrics
            st.session_state.predictions = predictions
            st.session_state.test_data = test_data
            
            st.success("✅ Modelo treinado com sucesso!")
            
        except ValueError as e:
            st.error(f"❌ Erro ao treinar o modelo: {e}")
            
    if st.session_state.get('model') is not None:
        visualizer.display_metrics(st.session_state.metrics)

# --- UI 4: Visualização de Dados e Modelo ---

def ui_visualizacao():
    st.header("📊 Visualização de Dados e Modelo")
    
    if 'df_clean' not in st.session_state or st.session_state.df_clean is None:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    df_clean = st.session_state.df_clean
    
    # Visualização dos dados
    visualizer.plot_data_distribution(df_clean)
    
    # Visualização do modelo (se treinado)
    if st.session_state.get('model') is not None:
        visualizer.plot_model_diagnostics(
            st.session_state.test_data['y'], 
            st.session_state.predictions
        )

# --- UI 5: Referências ---

def ui_referencias():
    st.header("📚 Referências Bibliográficas")
    
    st.markdown("""
    ### Base de Dados Utilizada
    
    **WorldClim - South America Climate Data**
    - **Fonte:** INPE (Instituto Nacional de Pesquisas Espaciais)
    - **URL:** [http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip](http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip)
    - **Descrição:** Conjunto de dados bioclimáticos de alta resolução (1km) para a América do Sul, contendo 19 variáveis bioclimáticas derivadas de dados de temperatura e precipitação.
    
    ### Referências Bibliográficas
    
    1. **Fick, S.E. & Hijmans, R.J. (2017)**  
       *WorldClim 2: new 1km spatial resolution climate surfaces for global land areas*  
       International Journal of Climatology
    
    2. **Wickham, H. & Grolemund, G. (2016)**  
       *R for Data Science*  
       O'Reilly Media
    
    3. **McKinney, W. (2017)**  
       *Python for Data Analysis*  
       O'Reilly Media
    
    4. **Streamlit Documentation (2023)**  
       [https://docs.streamlit.io](https://docs.streamlit.io)
    
    ### Variáveis Bioclimáticas (BIO1-BIO19)
    
    As 19 variáveis bioclimáticas representam aspectos anuais e sazonais do clima:
    - **BIO1:** Temperatura média anual
    - **BIO2:** Variação média diurna
    - **BIO3:** Isotermalidade
    - **BIO4:** Sazonalidade da temperatura
    - **BIO5:** Temperatura máxima do mês mais quente
    - **BIO6:** Temperatura mínima do mês mais frio
    - **BIO7:** Amplitude térmica anual
    - **BIO12:** Precipitação anual
    - **BIO13:** Precipitação do mês mais úmido
    - **BIO14:** Precipitação do mês mais seco
    """)

# --- Aplicação Principal ---

def main():
    st.set_page_config(
        page_title="Análise Climática - América do Sul",
        page_icon="🌎",
        layout="wide"
    )
    
    st.title("🌎 Análise Climática da América do Sul - Versão Modularizada (Classes)")
    st.markdown("Análise de dados bioclimáticos do WorldClim usando Python e Streamlit")
    
    # Inicializar session state
    if 'processar_dados' not in st.session_state:
        st.session_state.processar_dados = False
    if 'dados_processados' not in st.session_state:
        st.session_state.dados_processados = False
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'metrics' not in st.session_state:
        st.session_state.metrics = None
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None
    if 'test_data' not in st.session_state:
        st.session_state.test_data = None
    
    # Menu lateral
    st.sidebar.title("Navegação")
    opcoes_menu = [
        "1. Administração - Download e Processamento",
        "2. Análise Estatística Exploratória", 
        "3. Modelagem: Regressão Linear Múltipla",
        "4. Visualização de Dados e Modelo",
        "5. Referências"
    ]
    
    selecao = st.sidebar.radio("Selecione a seção:", opcoes_menu)
    
    # Status do sistema na sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Status do Sistema")
    
    if st.session_state.get('dados_processados', False) and st.session_state.df_clean is not None:
        st.sidebar.success("✅ Dados Processados")
        st.sidebar.write(f"📊 {len(st.session_state.df_clean):,} pontos de dados")
    else:
        st.sidebar.warning("⚠️ Aguardando Processamento")
    
    # Navegação entre seções
    if selecao == opcoes_menu[0]:
        ui_administracao()
    elif selecao == opcoes_menu[1]:
        ui_analise_estatistica()
    elif selecao == opcoes_menu[2]:
        ui_modelagem()
    elif selecao == opcoes_menu[3]:
        ui_visualizacao()
    elif selecao == opcoes_menu[4]:
        ui_referencias()

if __name__ == "__main__":
    main()