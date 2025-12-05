import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import requests
import zipfile
import io
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import time
from datetime import datetime

# Diretório para armazenar os dados descompactados
DATA_DIR = 'streamlit_data'
ZIP_URL = "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME = "SAmerica_WCLIM.zip"
LOG_FILE = os.path.join(DATA_DIR, "model_creation.log")

# --- Sistema de Download e Processamento (Atualizado) ---

def check_data_status(data_dir, zip_filename):
    """Verifica o status dos dados e processamento"""
    dir_exists = os.path.exists(data_dir)
    zip_exists = os.path.exists(os.path.join(data_dir, zip_filename))
    log_exists = os.path.exists(LOG_FILE)
    
    status = {
        'dir_exists': dir_exists,
        'zip_exists': zip_exists,
        'log_exists': log_exists,
        'model_created': False
    }
    
    # Verificar se o modelo já foi criado
    if log_exists:
        try:
            with open(LOG_FILE, 'r') as f:
                log_content = f.read()
            status['model_created'] = 'CREATED: TRUE' in log_content.upper()
        except:
            status['model_created'] = False
    
    return status

def download_zip_file(url, target_dir, zip_filename):
    """Faz download do arquivo ZIP com feedback de progresso"""
    try:
        # Criar diretório se não existir
        os.makedirs(target_dir, exist_ok=True)
        
        st.info("🌐 Iniciando download dos dados...")
        progress_bar = st.progress(0)
        
        # Download
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        chunk_size = 8192
        
        temp_zip = os.path.join(target_dir, f"temp_{zip_filename}")
        
        with open(temp_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress = downloaded_size / total_size
                        progress_bar.progress(min(progress, 1.0))
        
        # Mover para nome final
        target_zip = os.path.join(target_dir, zip_filename)
        os.rename(temp_zip, target_zip)
        
        progress_bar.progress(1.0)
        st.success("✅ Download realizado com sucesso!")
        return True
        
    except Exception as e:
        st.error(f"❌ Erro durante o download: {e}")
        return False

def unzip_data_file(zip_path, target_dir):
    """Descompacta arquivo ZIP com feedback"""
    try:
        st.info("📦 Iniciando descompactação dos dados...")
        progress_bar = st.progress(0)
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            total_files = len(file_list)
            
            for i, file in enumerate(file_list):
                zf.extract(file, target_dir)
                progress_bar.progress((i + 1) / total_files)
        
        st.success("✅ Dados descompactados com sucesso!")
        return True
        
    except Exception as e:
        st.error(f"❌ Erro durante descompactação: {e}")
        return False

def create_model_log(data_dir, status=True):
    """Cria arquivo de log do processamento"""
    try:
        log_content = f"""CREATED: {str(status).upper()}
DATE: {datetime.now()}
DATA_DIR: {data_dir}
TIMESTAMP: {int(time.time())}"""
        
        with open(LOG_FILE, 'w') as f:
            f.write(log_content)
        
        return True
    except Exception as e:
        st.warning(f"⚠️ Erro ao criar arquivo de log: {e}")
        return False

def validate_existing_model(data_dir):
    """Valida se o modelo existente está completo"""
    if not os.path.exists(LOG_FILE):
        return False
    
    try:
        with open(LOG_FILE, 'r') as f:
            log_content = f.read()
        
        model_created = 'CREATED: TRUE' in log_content.upper()
        
        if model_created:
            # Verificar se os arquivos ASC existem
            asc_files = glob.glob(os.path.join(data_dir, "*.asc"))
            files_to_process = [f for f in asc_files if os.path.basename(f) not in ['alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt']]
            
            if len(files_to_process) > 10:  # Espera-se mais de 10 arquivos climáticos
                st.info("✅ Modelo existente validado. Utilizando dados pré-processados.")
                return True
            else:
                st.warning("⚠️ Log encontrado, mas arquivos de dados incompletos. Reprocessando.")
                return False
        else:
            return False
            
    except Exception as e:
        st.warning(f"⚠️ Erro ao validar modelo existente: {e}")
        return False

def download_and_process_data(url, target_dir, zip_filename):
    """Função principal para orquestrar download e processamento"""
    # Verificar status atual
    status = check_data_status(target_dir, zip_filename)
    
    # Se modelo já foi criado e validado, retornar TRUE
    if status['model_created'] and validate_existing_model(target_dir):
        return True
    
    # Barra de progresso principal
    progress_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    # Etapa 1: Verificar e baixar dados se necessário
    progress_placeholder.info("🔍 Verificando dados existentes...")
    progress_bar.progress(0.1)
    
    if not status['zip_exists'] or not status['dir_exists']:
        progress_placeholder.info("📥 Download necessário. Baixando dados...")
        progress_bar.progress(0.2)
        download_success = download_zip_file(url, target_dir, zip_filename)
        if not download_success:
            return False
    
    # Etapa 2: Descompactar dados
    progress_placeholder.info("📂 Preparando para descompactar...")
    progress_bar.progress(0.5)
    zip_path = os.path.join(target_dir, zip_filename)
    unzip_success = unzip_data_file(zip_path, target_dir)
    if not unzip_success:
        return False
    
    # Etapa 3: Criar log do modelo
    progress_placeholder.info("⚙️ Finalizando processamento...")
    progress_bar.progress(0.9)
    log_success = create_model_log(target_dir, True)
    
    progress_placeholder.info("✅ Processamento concluído!")
    progress_bar.progress(1.0)
    
    return True

# --- Funções de Processamento de Dados (Mantidas) ---

def read_asc_file(filepath):
    """Lê um arquivo ASCII Grid (.asc) e retorna os metadados e os dados"""
    try:
        # Ler cabeçalho (6 linhas)
        with open(filepath, 'r') as con:
            header_lines = [con.readline().strip() for _ in range(6)]
        
        header = {}
        for line in header_lines:
            parts = line.split()
            key = parts[0]
            value = int(parts[1]) if key in ['ncols', 'nrows'] else float(parts[1])
            header[key] = value
        
        # Ler dados
        data = np.loadtxt(filepath, skiprows=6)
        
        return {'header': header, 'data': data}
    except Exception as e:
        st.error(f"Erro ao ler arquivo {os.path.basename(filepath)}: {e}")
        return None

@st.cache_data
def process_worldclim_data(data_dir):
    """Processa todos os arquivos WorldClim (.asc) no diretório"""
    if not os.path.exists(data_dir):
        st.error(f"Diretório não encontrado: {data_dir}")
        return None
    
    # Listar arquivos .asc, excluindo arquivos não climáticos
    asc_files = glob.glob(os.path.join(data_dir, "*.asc"))
    files_to_process = [f for f in asc_files if os.path.basename(f) not in ['alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt']]
    
    if len(files_to_process) == 0:
        st.warning("Nenhum arquivo .asc de variáveis climáticas encontrado")
        return None
    
    all_data = {}
    
    # Processar primeiro arquivo para obter estrutura
    first_file = files_to_process[0]
    first_result = read_asc_file(first_file)
    if first_result is None:
        return None
    
    rows = first_result['header']['nrows']
    cols = first_result['header']['ncols']
    nodata_value = first_result['header'].get('NODATA_value', -9999)
    
    # Adicionar primeiro conjunto de dados
    var_name = os.path.splitext(os.path.basename(first_file))[0]
    all_data[var_name] = first_result['data'].flatten()
    
    # Processar arquivos restantes
    for filepath in files_to_process[1:]:
        result = read_asc_file(filepath)
        if result is None:
            continue
        
        # Verificar dimensões
        if result['header']['nrows'] != rows or result['header']['ncols'] != cols:
            st.warning(f"Dimensões não correspondem para {os.path.basename(filepath)}")
            continue
        
        var_name = os.path.splitext(os.path.basename(filepath))[0]
        all_data[var_name] = result['data'].flatten()
    
    # Criar DataFrame
    df = pd.DataFrame(all_data)
    
    # Adicionar coordenadas
    df['row'] = np.repeat(range(1, rows + 1), cols)
    df['col'] = np.tile(range(1, cols + 1), rows)
    
    # Reordenar colunas
    df = df[['row', 'col'] + [col for col in df.columns if col not in ['row', 'col']]]
    
    # Remover valores NODATA
    df_clean = df[~(df == nodata_value).any(axis=1)]
    
    return df_clean

# --- UI 1: Administração - Download e Processamento (Atualizada) ---

def ui_administracao():
    st.header("📊 Administração - Download e Processamento de Dados")
    
    st.markdown("""
    Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul.
    Os dados serão baixados do INPE e processados para análise.
    """)
    
    # Verificar status atual
    status = check_data_status(DATA_DIR, ZIP_FILENAME)
    
    if status['model_created'] and validate_existing_model(DATA_DIR):
        st.success("✅ Modelo e dados prontos para serem visualizados")
        st.info("Os dados já foram processados e estão disponíveis para análise nas outras seções.")
        
        if st.button("🔄 Reprocessar Dados", type="secondary"):
            # Remove diretório existente para forçar novo processamento
            if os.path.exists(DATA_DIR):
                import shutil
                shutil.rmtree(DATA_DIR)
            st.session_state.dados_processados = False
            st.session_state.df_clean = None
            st.session_state.model = None
            st.session_state.metrics = None
            st.rerun()
    else:
        st.warning("⚠️ Dados não encontrados. É necessário processar os dados para continuar.")
        
        if st.button("🚀 Processar Dados", type="primary"):
            st.session_state.processar_dados = True
    
    # Processamento de dados
    if st.session_state.get('processar_dados', False):
        if download_and_process_data(ZIP_URL, DATA_DIR, ZIP_FILENAME):
            df_clean = process_worldclim_data(DATA_DIR)
            if df_clean is not None:
                st.session_state.df_clean = df_clean
                st.session_state.dados_processados = True
                st.session_state.processar_dados = False
                st.rerun()
            else:
                st.error("❌ Falha ao processar os dados climáticos.")
        else:
            st.error("❌ Falha ao baixar ou descompactar os dados.")

# --- UI 2: Análise Estatística Exploratória (Atualizada) ---

def ui_analise_estatistica():
    st.header("📈 Análise Estatística Exploratória")
    
    if 'df_clean' not in st.session_state:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    df_clean = st.session_state.df_clean
    
    st.subheader("Visão Geral dos Dados")
    st.write(f"Número total de pontos de grade válidos: **{len(df_clean):,}**")
    
    # Estatísticas descritivas COMPLETAS com NAs
    st.subheader("Estatísticas Descritivas (Completas)")
    st.write("Estatísticas descritivas para todas as variáveis bioclimáticas incluindo valores NA:")
    
    bio_cols = [col for col in df_clean.columns if col.startswith('bio')]
    
    # Calcular estatísticas descritivas avançadas
    desc_stats_list = []
    for col in bio_cols:
        stats = {
            'Variável': col,
            'N': df_clean[col].count(),
            'N_NA': df_clean[col].isna().sum(),
            'Porcentagem_NA': round(df_clean[col].isna().mean() * 100, 2),
            'Média': round(df_clean[col].mean(), 3),
            'Mediana': round(df_clean[col].median(), 3),
            'DP': round(df_clean[col].std(), 3),
            'Min': round(df_clean[col].min(), 3),
            'Q1': round(df_clean[col].quantile(0.25), 3),
            'Q3': round(df_clean[col].quantile(0.75), 3),
            'Max': round(df_clean[col].max(), 3)
        }
        desc_stats_list.append(stats)
    
    desc_stats_df = pd.DataFrame(desc_stats_list)
    st.dataframe(desc_stats_df, use_container_width=True)
    
    # Correlação entre variáveis bioclimáticas
    st.subheader("Análise de Correlação")
    
    if bio_cols:
        corr_matrix = df_clean[bio_cols].corr()
        
        # Correlação com BIO1
        st.markdown("**Correlação de BIO1 (Temperatura Média Anual) com Outras Variáveis:**")
        corr_bio1 = corr_matrix['bio1'].sort_values(ascending=False).drop('bio1')
        st.dataframe(corr_bio1.to_frame().style.format('{:.4f}'), use_container_width=True)
        
        # Heatmap de correlação
        st.markdown("**Mapa de Calor de Correlações:**")
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Matriz de Correlação - Variáveis Bioclimáticas')
        st.pyplot(fig)

# --- UI 3: Modelagem (Atualizada com Métricas Avançadas) ---

def ui_modelagem():
    st.header("🤖 Modelagem: Regressão Linear Múltipla")
    st.markdown("**Modelo:** BIO1 (Temperatura Média Anual) ~ BIO12 (Precipitação Anual) + BIO4 (Sazonalidade da Temperatura)")
    
    if 'df_clean' not in st.session_state:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    if st.button("🎯 Treinar Modelo", type="primary"):
        with st.spinner("Treinando modelo..."):
            df_clean = st.session_state.df_clean
            
            # Preparar dados
            model_df = df_clean[['bio1', 'bio12', 'bio4']].dropna()
            
            # Dividir dados
            X = model_df[['bio12', 'bio4']]
            y = model_df['bio1']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Armazenar conjuntos
            st.session_state.train_data = {'X': X_train, 'y': y_train}
            st.session_state.test_data = {'X': X_test, 'y': y_test}
            
            # Treinar modelo
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Fazer previsões
            y_pred = model.predict(X_test)
            
            # Calcular métricas avançadas
            r_squared = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            
            # Armazenar resultados
            st.session_state.model = model
            st.session_state.predictions = y_pred
            
            st.session_state.metrics = {
                'r_squared': r_squared,
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'coefficients': {
                    'bio12': model.coef_[0],
                    'bio4': model.coef_[1],
                    'intercept': model.intercept_
                },
                'n_train': len(X_train),
                'n_test': len(X_test),
                'n_total': len(model_df)
            }
        
        st.success("✅ Modelo treinado com sucesso!")
    
    # Exibir resultados se o modelo foi treinado
    if st.session_state.get('model') is not None:
        metrics = st.session_state.metrics
        
        # Métricas de Avaliação
        st.subheader("📊 Métricas de Avaliação do Modelo")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("R²", f"{metrics['r_squared']:.4f}", 
                     help="Coeficiente de Determinação - Proporção da variância explicada pelo modelo")
        
        with col2:
            st.metric("MSE", f"{metrics['mse']:.2f}", 
                     help="Erro Quadrático Médio - Média dos quadrados dos erros")
        
        with col3:
            st.metric("RMSE", f"{metrics['rmse']:.2f}", 
                     help="Raiz do Erro Quadrático Médio - Na mesma unidade da variável resposta")
        
        with col4:
            st.metric("MAE", f"{metrics['mae']:.2f}", 
                     help="Erro Absoluto Médio - Média dos valores absolutos dos erros")
        
        # Estatísticas dos Conjuntos de Dados
        st.subheader("📈 Estatísticas dos Conjuntos de Dados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Conjunto de Treino", f"{metrics['n_train']:,}", 
                     help="Observações para treinamento")
        
        with col2:
            st.metric("Conjunto de Teste", f"{metrics['n_test']:,}", 
                     help="Observações para teste")
        
        with col3:
            st.metric("Total (Após Limpeza)", f"{metrics['n_total']:,}", 
                     help="Observações válidas para modelagem")
        
        # Coeficientes do Modelo
        st.subheader("🔧 Coeficientes do Modelo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Coeficiente BIO12", f"{metrics['coefficients']['bio12']:.4f}", 
                     help="Precipitação Anual")
        
        with col2:
            st.metric("Coeficiente BIO4", f"{metrics['coefficients']['bio4']:.4f}", 
                     help="Sazonalidade da Temperatura")
        
        with col3:
            st.metric("Intercepto", f"{metrics['coefficients']['intercept']:.4f}", 
                     help="Termo constante")
        
        # Interpretação do Modelo
        st.subheader("📋 Interpretação do Modelo")
        
        interpretation_text = f"""
        O modelo explica **{metrics['r_squared']*100:.2f}%** da variância na Temperatura Média Anual (BIO1).
        
        📈 Um aumento de 1 unidade em BIO12 (Precipitação Anual) está associado a uma mudança de **{metrics['coefficients']['bio12']:.4f}** na BIO1.
        
        🌡️ Um aumento de 1 unidade em BIO4 (Sazonalidade da Temperatura) está associado a uma mudança de **{metrics['coefficients']['bio4']:.4f}** na BIO1.
        
        🎯 O RMSE de **{metrics['rmse']:.2f}** indica o erro médio de previsão do modelo.
        """
        
        st.info(interpretation_text)

# --- UI 4: Visualização de Dados e Modelo (Atualizada) ---

def ui_visualizacao():
    st.header("📊 Visualização de Dados e Modelo")
    
    if 'df_clean' not in st.session_state:
        st.warning("⚠️ Por favor, processe os dados primeiro na seção 'Administração'.")
        return
    
    df_clean = st.session_state.df_clean
    
    st.subheader("Visualização dos Dados Climáticos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma BIO1
        st.markdown("**Distribuição da Temperatura Média Anual (BIO1)**")
        fig1, ax1 = plt.subplots()
        sns.histplot(df_clean['bio1'], kde=True, ax=ax1, color='skyblue')
        ax1.set_title('Distribuição de BIO1 (Temperatura Média Anual)')
        ax1.set_xlabel('BIO1 (x 10 °C)')
        ax1.set_ylabel('Densidade')
        st.pyplot(fig1)
    
    with col2:
        # Dispersão BIO1 vs BIO12
        st.markdown("**Relação entre BIO1 e BIO12**")
        sample_data = df_clean.sample(n=min(5000, len(df_clean)), random_state=42)
        fig2, ax2 = plt.subplots()
        sns.scatterplot(x='bio12', y='bio1', data=sample_data, alpha=0.5, ax=ax2, color='darkred')
        ax2.set_title('BIO1 vs BIO12 (Amostra)')
        ax2.set_xlabel('BIO12 (mm)')
        ax2.set_ylabel('BIO1 (x 10 °C)')
        st.pyplot(fig2)
    
    # Gráficos do modelo (se treinado)
    if st.session_state.get('model') is not None:
        st.subheader("Visualização do Modelo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição dos resíduos
            residuals = st.session_state.test_data['y'] - st.session_state.predictions
            st.markdown("**Distribuição dos Resíduos do Modelo**")
            fig3, ax3 = plt.subplots()
            sns.histplot(residuals, kde=True, ax=ax3, color='lightgreen')
            ax3.set_title('Distribuição dos Resíduos')
            ax3.set_xlabel('Resíduos (y_test - y_pred)')
            ax3.set_ylabel('Densidade')
            st.pyplot(fig3)
        
        with col2:
            # Valores reais vs preditos
            st.markdown("**Valores Reais vs Preditos**")
            fig4, ax4 = plt.subplots()
            ax4.scatter(st.session_state.test_data['y'], st.session_state.predictions, 
                       alpha=0.5, color='purple')
            ax4.plot([st.session_state.test_data['y'].min(), st.session_state.test_data['y'].max()], 
                    [st.session_state.test_data['y'].min(), st.session_state.test_data['y'].max()], 
                    'r--', lw=2)
            ax4.set_xlabel('Valores Reais')
            ax4.set_ylabel('Valores Preditos')
            ax4.set_title('Valores Reais vs Preditos')
            st.pyplot(fig4)

# --- UI 5: Referências (Mantida) ---

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

# --- Aplicação Principal (Atualizada) ---

def main():
    st.set_page_config(
        page_title="Análise Climática - América do Sul",
        page_icon="🌎",
        layout="wide"
    )
    
    st.title("🌎 Análise Climática da América do Sul - Versão Integrada")
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
    
    if st.session_state.get('dados_processados', False):
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