import os
import glob
import requests
import zipfile
import time
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st

NAME_FILE_ZIP="SAmerica_WCLIM.zip"
URL_FILE_ZIP=f"http://www.dpi.inpe.br/amb_data/AmericaSul/{NAME_FILE_ZIP}"

class DataProcessor:
    def __init__(self, data_dir='streamlit_data', zip_url=URL_FILE_ZIP, zip_filename=NAME_FILE_ZIP):
        self.DATA_DIR = data_dir
        self.ZIP_URL = zip_url
        self.ZIP_FILENAME = zip_filename
        self.LOG_FILE = os.path.join(self.DATA_DIR, "model_creation.log")

    def check_data_status(self):
        """Verifica o status dos dados e processamento"""
        dir_exists = os.path.exists(self.DATA_DIR)
        zip_exists = os.path.exists(os.path.join(self.DATA_DIR, self.ZIP_FILENAME))
        log_exists = os.path.exists(self.LOG_FILE)
        
        status = {
            'dir_exists': dir_exists,
            'zip_exists': zip_exists,
            'log_exists': log_exists,
            'model_created': False
        }
        
        if log_exists:
            try:
                with open(self.LOG_FILE, 'r') as f:
                    log_content = f.read()
                status['model_created'] = 'CREATED: TRUE' in log_content.upper()
            except:
                status['model_created'] = False
        
        return status

    def download_zip_file(self):
        """Faz download do arquivo ZIP com feedback de progresso"""
        try:
            os.makedirs(self.DATA_DIR, exist_ok=True)
            
            st.info("🌐 Iniciando download dos dados...")
            progress_bar = st.progress(0)
            
            response = requests.get(self.ZIP_URL, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            chunk_size = 8192
            
            temp_zip = os.path.join(self.DATA_DIR, f"temp_{self.ZIP_FILENAME}")
            
            with open(temp_zip, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = downloaded_size / total_size
                            progress_bar.progress(min(progress, 1.0))
            
            target_zip = os.path.join(self.DATA_DIR, self.ZIP_FILENAME)
            os.rename(temp_zip, target_zip)
            
            progress_bar.progress(1.0)
            st.success("✅ Download realizado com sucesso!")
            return True
            
        except Exception as e:
            st.error(f"❌ Erro durante o download: {e}")
            return False

    def unzip_data_file(self):
        """Descompacta arquivo ZIP com feedback"""
        zip_path = os.path.join(self.DATA_DIR, self.ZIP_FILENAME)
        try:
            st.info("📦 Iniciando descompactação dos dados...")
            progress_bar = st.progress(0)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_list = zf.namelist()
                total_files = len(file_list)
                
                for i, file in enumerate(file_list):
                    zf.extract(file, self.DATA_DIR)
                    progress_bar.progress((i + 1) / total_files)
            
            st.success("✅ Dados descompactados com sucesso!")
            return True
            
        except Exception as e:
            st.error(f"❌ Erro durante descompactação: {e}")
            return False

    def create_model_log(self, status=True):
        """Cria arquivo de log do processamento"""
        try:
            log_content = f"""CREATED: {str(status).upper()}
DATE: {datetime.now()}
DATA_DIR: {self.DATA_DIR}
TIMESTAMP: {int(time.time())}"""
            
            with open(self.LOG_FILE, 'w') as f:
                f.write(log_content)
            
            return True
        except Exception as e:
            st.warning(f"⚠️ Erro ao criar arquivo de log: {e}")
            return False

    def validate_existing_model(self):
        """Valida se o modelo existente está completo"""
        if not os.path.exists(self.LOG_FILE):
            return False
        
        try:
            with open(self.LOG_FILE, 'r') as f:
                log_content = f.read()
            
            model_created = 'CREATED: TRUE' in log_content.upper()
            
            if model_created:
                asc_files = glob.glob(os.path.join(self.DATA_DIR, "*.asc"))
                files_to_process = [f for f in asc_files if os.path.basename(f) not in ['alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt']]
                
                if len(files_to_process) > 10:
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

    def download_and_process_data(self):
        """Função principal para orquestrar download e processamento"""
        status = self.check_data_status()
        
        if status['model_created'] and self.validate_existing_model():
            return True
        
        progress_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        # Etapa 1: Verificar e baixar dados se necessário
        progress_placeholder.info("🔍 Verificando dados existentes...")
        progress_bar.progress(0.1)
        
        if not status['zip_exists'] or not status['dir_exists']:
            progress_placeholder.info("📥 Download necessário. Baixando dados...")
            progress_bar.progress(0.2)
            download_success = self.download_zip_file()
            if not download_success:
                return False
        
        # Etapa 2: Descompactar dados
        progress_placeholder.info("📂 Preparando para descompactar...")
        progress_bar.progress(0.5)
        unzip_success = self.unzip_data_file()
        if not unzip_success:
            return False
        
        # Etapa 3: Criar log do modelo
        progress_placeholder.info("⚙️ Finalizando processamento...")
        progress_bar.progress(0.9)
        self.create_model_log(True)
        
        progress_placeholder.info("✅ Processamento concluído!")
        progress_bar.progress(1.0)
        
        return True

    def read_asc_file(self, filepath):
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
    def process_worldclim_data(_self=None):
        """Processa todos os arquivos WorldClim (.asc) no diretório"""
        # Se _self não for fornecido, use a instância global ou crie uma
        if _self is None:
            _self = DataProcessor()
        
        if not os.path.exists(_self.DATA_DIR):
            st.error(f"Diretório não encontrado: {_self.DATA_DIR}")
            return None
        
        # Listar arquivos .asc, excluindo arquivos não climáticos
        asc_files = glob.glob(os.path.join(_self.DATA_DIR, "*.asc"))
        files_to_process = [f for f in asc_files if os.path.basename(f) not in ['alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt']]
        
        if len(files_to_process) == 0:
            st.warning("Nenhum arquivo .asc de variáveis climáticas encontrado")
            return None
        
        all_data = {}
        
        # Processar primeiro arquivo para obter estrutura
        first_file = files_to_process[0]
        first_result = _self.read_asc_file(first_file)
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
            result = _self.read_asc_file(filepath)
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