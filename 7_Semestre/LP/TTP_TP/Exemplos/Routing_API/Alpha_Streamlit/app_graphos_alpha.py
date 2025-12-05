import streamlit as st
import pandas as pd
import sqlite3
import os
import heapq
import plotly.express as px
import plotly.graph_objects as go
from math import radians, sin, cos, sqrt, atan2, log
import numpy as np
from typing import Dict, List, Tuple, Optional
import pygwalker as pyg
import requests
from functools import lru_cache

st.set_page_config(layout="wide", page_title="🌍 Sistema de Roteamento Hierárquico Global")
st.title("🌍 Sistema de Roteamento Hierárquico Global Otimizado")
st.markdown("**Complexidade O(log m * n) → O(1) - 7 Níveis Hierárquicos com Cache e Índices**")

# Configurações globais
DB_PATH = "global_hierarchical_router_optimized.db"
CACHE_SIZE = 10000
REQUIRED_CSV_COLUMNS = ['city', 'lat', 'lng', 'country', 'id']
DATA_URL = "https://raw.githubusercontent.com/kasshinokun/Q3_Q4_2025_Public/refs/heads/main/data_world_graphos/worldcities.csv"

HIERARCHY_LEVELS = {
    'city': 0, 'municipality': 1, 'state': 2, 
    'country': 3, 'regional_block': 4, 'continent': 5, 'global': 6
}

REGIONAL_BLOCKS = {
    "MERCOSUL": ["Argentina", "Brazil", "Paraguay", "Uruguay", "Venezuela", "Chile", "Bolivia"],
    "EU": ["Germany", "France", "Italy", "Spain", "Netherlands", "Belgium", "Portugal", "Sweden"],
    "ASEAN": ["Thailand", "Malaysia", "Singapore", "Indonesia", "Vietnam", "Philippines"],
    "NAFTA": ["United States", "Canada", "Mexico"],
    "AFRICAN_UNION": ["Nigeria", "South Africa", "Egypt", "Kenya", "Ethiopia"],
    "MIDDLE_EAST": ["Saudi Arabia", "Iran", "Israel", "Turkey", "United Arab Emirates"]
}

CONTINENT_CODES = {
    "AF": "Africa", "AS": "Asia", "EU": "Europe", 
    "NA": "North America", "SA": "South America", 
    "OC": "Oceania", "AN": "Antarctica"
}

# Cache global para rotas
route_cache = {}

# ---------- FUNÇÕES UTILITÁRIAS OTIMIZADAS ----------
@lru_cache(maxsize=50000)
def haversine_cached(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula distância em km usando fórmula de Haversine com cache"""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float('inf')
        
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Wrapper para haversine com cache"""
    return haversine_cached(lat1, lon1, lat2, lon2)

@lru_cache(maxsize=1000)
def get_continent(country: str) -> str:
    """Mapeamento país → continente com cache"""
    COUNTRY_CONTINENT = {
        "Argentina":"SA","Brazil":"SA","Chile":"SA","Colombia":"SA","Peru":"SA",
        "Venezuela":"SA","Ecuador":"SA","Bolivia":"SA","Paraguay":"SA","Uruguay":"SA",
        "United States":"NA","Canada":"NA","Mexico":"NA",
        "Germany":"EU","France":"EU","Italy":"EU","Spain":"EU","United Kingdom":"EU",
        "Netherlands":"EU","Belgium":"EU","Portugal":"EU","Sweden":"EU","Switzerland":"EU",
        "China":"AS","Japan":"AS","India":"AS","South Korea":"AS","Thailand":"AS",
        "Malaysia":"AS","Singapore":"AS","Indonesia":"AS","Vietnam":"AS","Philippines":"AS",
        "Nigeria":"AF","South Africa":"AF","Egypt":"AF","Kenya":"AF","Ethiopia":"AF",
        "Australia":"OC","New Zealand":"OC",
        "Russia":"EU", "Turkey":"AS", "Egypt":"AF", "South Africa":"AF", "Morocco":"AF",
        "Japan":"AS", "South Korea":"AS", "Israel":"AS", "Iran":"AS"
    }
    return COUNTRY_CONTINENT.get(country, "UN")

@lru_cache(maxsize=1000)
def get_regional_block(country: str) -> str:
    """Retorna o bloco regional do país com cache"""
    for block, countries in REGIONAL_BLOCKS.items():
        if country in countries:
            return block
    return "OTHER"

def check_db_exists():
    return os.path.exists(DB_PATH)

def get_database_stats(conn):
    """Retorna estatísticas do banco"""
    stats = {}
    tables = ['cities', 'municipalities', 'states', 'countries', 'regional_blocks', 'continents']
    
    for table in tables:
        try:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            stats[table] = count
        except sqlite3.OperationalError:
            stats[table] = 0
    return stats

@lru_cache(maxsize=1)
def get_all_cities_cached(db_path):
    """Retorna lista de todas as cidades com cache"""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT id, name, country FROM cities ORDER BY name", conn)
        conn.close()
        return df
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError) as e:
        st.error(f"Erro ao carregar cidades: {e}")
        return pd.DataFrame()

def get_all_cities(conn):
    """Wrapper para get_all_cities com cache"""
    return get_all_cities_cached(DB_PATH)

# ---------- ESTRUTURA DO BANCO OTIMIZADA ----------
def create_optimized_database_structure():
    """Cria estrutura completa do banco hierárquico com otimizações"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Configurações de performance do SQLite
    c.execute("PRAGMA journal_mode = WAL")
    c.execute("PRAGMA synchronous = NORMAL")
    c.execute("PRAGMA cache_size = 10000")
    c.execute("PRAGMA temp_store = MEMORY")
    
    c.executescript("""
    DROP TABLE IF EXISTS cities;
    DROP TABLE IF EXISTS municipalities;
    DROP TABLE IF EXISTS states;
    DROP TABLE IF EXISTS countries;
    DROP TABLE IF EXISTS regional_blocks;
    DROP TABLE IF EXISTS continents;
    DROP TABLE IF EXISTS global;
    DROP TABLE IF EXISTS hierarchical_edges;
    DROP TABLE IF EXISTS precomputed_distances;
    DROP TABLE IF EXISTS route_cache;
    
    -- Tabelas principais otimizadas
    CREATE TABLE cities(
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        municipality_id INTEGER NOT NULL,
        state_id INTEGER NOT NULL,
        country_id INTEGER NOT NULL,
        regional_block_id INTEGER NOT NULL,
        continent_id INTEGER NOT NULL
    );
    
    CREATE TABLE municipalities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        centroid_lat REAL NOT NULL,
        centroid_lng REAL NOT NULL,
        state_id INTEGER NOT NULL
    );
    
    CREATE TABLE states(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_id INTEGER NOT NULL,
        centroid_lat REAL NOT NULL,
        centroid_lng REAL NOT NULL
    );
    
    CREATE TABLE countries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        regional_block_id INTEGER NOT NULL,
        continent_id INTEGER NOT NULL,
        centroid_lat REAL NOT NULL,
        centroid_lng REAL NOT NULL
    );
    
    CREATE TABLE regional_blocks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        continent_id INTEGER NOT NULL,
        centroid_lat REAL NOT NULL,
        centroid_lng REAL NOT NULL
    );
    
    CREATE TABLE continents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        centroid_lat REAL NOT NULL,
        centroid_lng REAL NOT NULL
    );
    
    CREATE TABLE hierarchical_edges(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT NOT NULL,
        source_id TEXT NOT NULL,
        target_id TEXT NOT NULL,
        source_type TEXT NOT NULL,
        target_type TEXT NOT NULL,
        weight REAL NOT NULL DEFAULT 0,
        bidirectional BOOLEAN NOT NULL DEFAULT TRUE
    );
    
    -- Tabela de distâncias pré-computadas para O(1) lookup
    CREATE TABLE precomputed_distances(
        city1_id TEXT NOT NULL,
        city2_id TEXT NOT NULL,
        distance REAL NOT NULL,
        PRIMARY KEY (city1_id, city2_id)
    );
    
    -- Cache de rotas para O(1) lookup
    CREATE TABLE route_cache(
        start_id TEXT NOT NULL,
        end_id TEXT NOT NULL,
        route_json TEXT NOT NULL,
        distance REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (start_id, end_id)
    );
    
    -- Índices otimizados para performance O(log n)
    CREATE INDEX idx_cities_geo ON cities(lat, lng);
    CREATE INDEX idx_cities_country ON cities(country);
    CREATE INDEX idx_cities_municipality ON cities(municipality_id);
    CREATE INDEX idx_cities_state ON cities(state_id);
    CREATE INDEX idx_cities_country_id ON cities(country_id);
    
    CREATE INDEX idx_hierarchical_level ON hierarchical_edges(level);
    CREATE INDEX idx_hierarchical_source ON hierarchical_edges(source_id, source_type);
    CREATE INDEX idx_hierarchical_target ON hierarchical_edges(target_id, target_type);
    CREATE INDEX idx_hierarchical_composite ON hierarchical_edges(source_id, source_type, target_id, target_type);
    
    CREATE INDEX idx_precomputed_city1 ON precomputed_distances(city1_id);
    CREATE INDEX idx_precomputed_city2 ON precomputed_distances(city2_id);
    
    CREATE INDEX idx_route_cache_start ON route_cache(start_id);
    CREATE INDEX idx_route_cache_end ON route_cache(end_id);
    """)
    
    conn.commit()
    conn.close()

def download_and_load_data():
    """Baixa e carrega os dados do CSV"""
    if not os.path.exists('worldcities.csv'):
        with st.spinner('Baixando dados de cidades...'):
            try:
                response = requests.get(DATA_URL)
                response.raise_for_status()
                with open('worldcities.csv', 'wb') as f:
                    f.write(response.content)
                st.success('Dados baixados com sucesso!')
            except Exception as e:
                st.error(f"Erro ao baixar dados: {e}")
                return None
    
    try:
        df = pd.read_csv('worldcities.csv')
        if 'id' not in df.columns:
            df['id'] = df.index.astype(str)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar CSV: {e}")
        return None

def create_optimized_clusters(df: pd.DataFrame, progress_bar, status_text):
    """Cria clusters em 7 níveis hierárquicos com otimizações"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Configurar para inserção em lote
    c.execute("BEGIN TRANSACTION")
    
    status_text.text("Passo 1/5: Criando hierarquia e clusters...")
    
    country_id_map = {}
    regional_block_id_map = {}
    continent_id_map = {}
    municipality_clusters = {}
    
    total_rows = len(df)
    for i, (_, row) in enumerate(df.iterrows()):
        row_dict = row.to_dict()
        country_name = row_dict['country']
        
        if country_name not in country_id_map:
            continent_code = get_continent(country_name)
            if continent_code not in continent_id_map:
                c.execute("INSERT INTO continents(code, name, centroid_lat, centroid_lng) VALUES(?, ?, 0, 0)", 
                         (continent_code, CONTINENT_CODES.get(continent_code, "Unknown")))
                continent_id_map[continent_code] = c.lastrowid
            
            regional_block_name = get_regional_block(country_name)
            if regional_block_name not in regional_block_id_map:
                c.execute("INSERT INTO regional_blocks(name, continent_id, centroid_lat, centroid_lng) VALUES(?, ?, 0, 0)",
                         (regional_block_name, continent_id_map[continent_code]))
                regional_block_id_map[regional_block_name] = c.lastrowid
            
            c.execute("INSERT INTO countries(name, regional_block_id, continent_id, centroid_lat, centroid_lng) VALUES(?, ?, ?, 0, 0)",
                     (country_name, regional_block_id_map[regional_block_name], continent_id_map[continent_code]))
            country_id_map[country_name] = c.lastrowid
        
        municipality_key = f"{country_name}_{round(row_dict['lat'], 2)}_{round(row_dict['lng'], 2)}"
        municipality_clusters.setdefault(municipality_key, []).append(row_dict)
        
        if i % 1000 == 0:
            progress_bar.progress(10 + int(15 * i / total_rows))
            
    c.execute("COMMIT")
    
    status_text.text("Passo 2/5: Criando estados e municípios...")
    progress_bar.progress(25)
    
    c.execute("BEGIN TRANSACTION")
    state_id_map = {}
    
    for municipal_key, cities in municipality_clusters.items():
        country = cities[0]['country']
        state_key = f"{country}_{round(cities[0]['lat'], 1)}_{round(cities[0]['lng'], 1)}"
        if state_key not in state_id_map:
            centroid_lat_s = np.mean([c['lat'] for c in cities])
            centroid_lng_s = np.mean([c['lng'] for c in cities])
            c.execute("INSERT INTO states(country_id, centroid_lat, centroid_lng) VALUES(?, ?, ?)",
                     (country_id_map[country], centroid_lat_s, centroid_lng_s))
            state_id_map[state_key] = c.lastrowid

    municipality_id_map = {}
    for municipal_key, cities in municipality_clusters.items():
        centroid_lat = np.mean([c['lat'] for c in cities])
        centroid_lng = np.mean([c['lng'] for c in cities])
        country = cities[0]['country']
        state_key = f"{country}_{round(cities[0]['lat'], 1)}_{round(cities[0]['lng'], 1)}"
        state_id = state_id_map[state_key]
        
        c.execute("INSERT INTO municipalities(centroid_lat, centroid_lng, state_id) VALUES(?, ?, ?)",
                  (centroid_lat, centroid_lng, state_id))
        municipality_id_map[municipal_key] = c.lastrowid
    
    c.execute("COMMIT")
    
    status_text.text("Passo 3/5: Inserindo cidades...")
    progress_bar.progress(50)

    c.execute("BEGIN TRANSACTION")
    cities_to_insert = []
    for municipal_key, cities in municipality_clusters.items():
        municipality_id = municipality_id_map[municipal_key]
        
        country = cities[0]['country']
        state_key = f"{country}_{round(cities[0]['lat'], 1)}_{round(cities[0]['lng'], 1)}"
        state_id = state_id_map[state_key]
        
        for city in cities:
            cities_to_insert.append((
                city['id'], city['city'], city['country'], city['lat'], city['lng'],
                municipality_id, state_id, country_id_map[country],
                regional_block_id_map[get_regional_block(city['country'])],
                continent_id_map[get_continent(city['country'])]
            ))
            
    c.executemany("""
        INSERT INTO cities (id, name, country, lat, lng, municipality_id, state_id, country_id, regional_block_id, continent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cities_to_insert)
    c.execute("COMMIT")

    status_text.text("Passo 4/5: Criando conexões hierárquicas...")
    progress_bar.progress(75)
    create_hierarchical_connections(conn)

    status_text.text("Passo 5/5: Pré-computando distâncias para cidades próximas...")
    progress_bar.progress(85)
    precompute_nearby_distances(conn)

    conn.close()
    progress_bar.progress(100)
    status_text.text("Sistema hierárquico otimizado construído com sucesso!")
    
    # Limpar cache
    get_all_cities_cached.cache_clear()
    haversine_cached.cache_clear()
    
    st.rerun()

def create_hierarchical_connections(conn):
    """Cria conexões entre todos os níveis hierárquicos"""
    c = conn.cursor()
    
    c.execute("BEGIN TRANSACTION")

    # Conexões hierárquicas
    connections = [
        ("city_to_municipality", "cities", "municipalities", "municipality_id"),
        ("municipality_to_state", "municipalities", "states", "state_id"),
        ("state_to_country", "states", "countries", "country_id"),
        ("country_to_regional_block", "countries", "regional_blocks", "regional_block_id"),
        ("regional_block_to_continent", "regional_blocks", "continents", "continent_id")
    ]
    
    for level, source_table, target_table, join_field in connections:
        c.execute(f"""
            INSERT INTO hierarchical_edges(level, source_id, target_id, source_type, target_type, weight, bidirectional)
            SELECT '{level}', T1.id, T2.id, '{source_table[:-1]}', '{target_table[:-1]}', 0, TRUE
            FROM {source_table} AS T1
            JOIN {target_table} AS T2 ON T1.{join_field} = T2.id
        """)

    # Conexão global
    c.execute("INSERT OR IGNORE INTO global VALUES(1)")
    c.execute("""
        INSERT INTO hierarchical_edges(level, source_id, target_id, source_type, target_type, weight, bidirectional)
        SELECT 'continent_to_global', id, '1', 'continent', 'global', 0, TRUE
        FROM continents
    """)
    
    c.execute("COMMIT")

def precompute_nearby_distances(conn):
    """Pré-computa distâncias entre cidades próximas para O(1) lookup"""
    c = conn.cursor()
    
    # Buscar todas as cidades
    cities = c.execute("SELECT id, lat, lng FROM cities").fetchall()
    
    c.execute("BEGIN TRANSACTION")
    distances_to_insert = []
    
    for i, (city1_id, lat1, lng1) in enumerate(cities):
        if i % 1000 == 0:
            st.write(f"Pré-computando distâncias: {i}/{len(cities)}")
            
        # Encontrar cidades próximas (dentro de 2 graus)
        nearby = c.execute("""
            SELECT id, lat, lng FROM cities 
            WHERE id != ? AND 
            abs(lat - ?) < 2 AND abs(lng - ?) < 2
            ORDER BY (lat-?)*(lat-?) + (lng-?)*(lng-?) LIMIT 20
        """, (city1_id, lat1, lng1, lat1, lat1, lng1, lng1)).fetchall()
        
        for city2_id, lat2, lng2 in nearby:
            dist = haversine(lat1, lng1, lat2, lng2)
            if dist < 200:  # Apenas distâncias menores que 200km
                distances_to_insert.append((city1_id, city2_id, dist))
                distances_to_insert.append((city2_id, city1_id, dist))  # Bidirecional
    
    c.executemany("INSERT OR REPLACE INTO precomputed_distances VALUES (?, ?, ?)", distances_to_insert)
    c.execute("COMMIT")

# ---------- ALGORITMO DE BUSCA OTIMIZADO ----------
class OptimizedHierarchicalRouter:
    def __init__(self, conn):
        self.conn = conn
        self.node_cache = {}

    def find_path(self, start_id: str, end_id: str, status_text, progress_bar) -> Optional[List[str]]:
        """A* hierárquico otimizado com cache e pré-computação"""
        
        # Verificar cache de rotas primeiro (O(1))
        cache_key = f"{start_id}_{end_id}"
        cached_route = self._get_cached_route(start_id, end_id)
        if cached_route:
            status_text.text("Rota encontrada no cache!")
            progress_bar.progress(100)
            return cached_route
        
        # Verificar distância pré-computada (O(1))
        precomputed_dist = self._get_precomputed_distance(start_id, end_id)
        if precomputed_dist is not None:
            status_text.text("Rota direta encontrada!")
            progress_bar.progress(100)
            route = [start_id, end_id]
            self._cache_route(start_id, end_id, route, precomputed_dist)
            return route
        
        start_node = self._get_node_info(start_id, 'city')
        end_node = self._get_node_info(end_id, 'city')
        
        if not start_node or not end_node:
            st.error("Cidade de origem ou destino não encontrada.")
            return None
        
        # A* otimizado com heurística melhorada
        def enhanced_heuristic(node_id: str, node_type: str) -> float:
            end_lat, end_lng = end_node['lat'], end_node['lng']
            
            if node_type == 'city':
                node_info = self._get_node_info(node_id, 'city')
                if not node_info:
                    return float('inf')
                lat, lng = node_info['lat'], node_info['lng']
            else:
                lat, lng = self._get_centroid(node_id, node_type)
            
            base_dist = haversine(lat, lng, end_lat, end_lng)
            
            # Penalizar níveis hierárquicos mais altos
            level_penalty = HIERARCHY_LEVELS.get(node_type, 0) * 100
            return base_dist + level_penalty
        
        pq = [(0, f"{start_id}::city")]
        g_scores = {f"{start_id}::city": 0}
        came_from = {}
        visited = set()
        
        iteration = 0
        while pq:
            f_score, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            visited.add(current)
            
            node_id, node_type = current.split('::')
            
            if iteration % 50 == 0:
                status_text.text(f"Explorando {node_type}: {node_id[:10]}...")
                progress = min(95, int(iteration / 10))
                progress_bar.progress(progress)
            iteration += 1

            if node_id == end_id and node_type == 'city':
                progress_bar.progress(100)
                route = self._reconstruct_path(came_from, current)
                total_distance = self._calculate_route_distance(route)
                self._cache_route(start_id, end_id, route, total_distance)
                return route
                
            neighbors = self._get_neighbors_optimized(node_id, node_type)
            
            for neighbor_id, neighbor_type, weight in neighbors:
                neighbor_key = f"{neighbor_id}::{neighbor_type}"
                
                if neighbor_key in visited:
                    continue
                
                current_g = g_scores[current]
                tentative_g_score = current_g + weight
                
                if tentative_g_score < g_scores.get(neighbor_key, float('inf')):
                    g_scores[neighbor_key] = tentative_g_score
                    f_score = tentative_g_score + enhanced_heuristic(neighbor_id, neighbor_type)
                    heapq.heappush(pq, (f_score, neighbor_key))
                    came_from[neighbor_key] = current
                        
        return None

    def _get_cached_route(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """Busca rota no cache (O(1))"""
        try:
            result = self.conn.execute(
                "SELECT route_json FROM route_cache WHERE start_id = ? AND end_id = ?",
                (start_id, end_id)
            ).fetchone()
            
            if result:
                import json
                return json.loads(result[0])
        except Exception:
            pass
        return None

    def _cache_route(self, start_id: str, end_id: str, route: List[str], distance: float):
        """Armazena rota no cache"""
        try:
            import json
            route_json = json.dumps(route)
            self.conn.execute(
                "INSERT OR REPLACE INTO route_cache (start_id, end_id, route_json, distance) VALUES (?, ?, ?, ?)",
                (start_id, end_id, route_json, distance)
            )
            self.conn.commit()
        except Exception:
            pass

    def _get_precomputed_distance(self, city1_id: str, city2_id: str) -> Optional[float]:
        """Busca distância pré-computada (O(1))"""
        try:
            result = self.conn.execute(
                "SELECT distance FROM precomputed_distances WHERE city1_id = ? AND city2_id = ?",
                (city1_id, city2_id)
            ).fetchone()
            return result[0] if result else None
        except Exception:
            return None

    @lru_cache(maxsize=10000)
    def _get_node_info_cached(self, node_id: str, node_type: str) -> Optional[Dict]:
        """Obtém info de um nó com cache"""
        try:
            if node_type == 'city':
                query = "SELECT * FROM cities WHERE id = ?"
                result = self.conn.execute(query, (node_id,)).fetchone()
                if result:
                    col_names = [desc[0] for desc in self.conn.execute(query, (node_id,)).description]
                    return dict(zip(col_names, result))
            return None
        except Exception:
            return None

    def _get_node_info(self, node_id: str, node_type: str) -> Optional[Dict]:
        """Wrapper para _get_node_info com cache"""
        return self._get_node_info_cached(node_id, node_type)

    @lru_cache(maxsize=5000)
    def _get_centroid_cached(self, node_id: str, node_type: str) -> Tuple[float, float]:
        """Obtém o centróide de um cluster com cache"""
        query_map = {
            'municipality': "SELECT centroid_lat, centroid_lng FROM municipalities WHERE id = ?",
            'state': "SELECT centroid_lat, centroid_lng FROM states WHERE id = ?",
            'country': "SELECT centroid_lat, centroid_lng FROM countries WHERE id = ?",
            'regional_block': "SELECT centroid_lat, centroid_lng FROM regional_blocks WHERE id = ?",
            'continent': "SELECT centroid_lat, centroid_lng FROM continents WHERE id = ?"
        }
        
        if node_type in query_map:
            try:
                result = self.conn.execute(query_map[node_type], (node_id,)).fetchone()
                if result:
                    return result
            except Exception:
                pass
        return (0.0, 0.0)

    def _get_centroid(self, node_id: str, node_type: str) -> Tuple[float, float]:
        """Wrapper para _get_centroid com cache"""
        return self._get_centroid_cached(node_id, node_type)

    def _get_neighbors_optimized(self, node_id: str, node_type: str) -> List[Tuple]:
        """Obtém vizinhos otimizado com índices e cache"""
        neighbors = []
        
        # Busca hierárquica otimizada com índices
        hierarchical_query = """
            SELECT target_id, target_type, weight FROM hierarchical_edges 
            WHERE source_id = ? AND source_type = ?
            UNION
            SELECT source_id, source_type, weight FROM hierarchical_edges 
            WHERE target_id = ? AND target_type = ?
        """
        
        try:
            hierarchical_neighbors = self.conn.execute(
                hierarchical_query, (node_id, node_type, node_id, node_type)
            ).fetchall()
            
            neighbors.extend([(str(n[0]), n[1], n[2]) for n in hierarchical_neighbors])
        except Exception:
            pass
        
        # Para cidades, usar distâncias pré-computadas
        if node_type == 'city':
            try:
                nearby_cities = self.conn.execute("""
                    SELECT city2_id, distance FROM precomputed_distances 
                    WHERE city1_id = ? ORDER BY distance LIMIT 10
                """, (node_id,)).fetchall()
                
                for near_city_id, dist in nearby_cities:
                    neighbors.append((near_city_id, 'city', dist))
            except Exception:
                pass
        
        return neighbors

    def _reconstruct_path(self, came_from: Dict, current: str) -> List[str]:
        """Reconstrói o caminho do A*"""
        path = []
        while current in came_from:
            node_id, node_type = current.split('::')
            if node_type == 'city':
                path.append(node_id)
            current = came_from[current]
        
        start_id, start_type = current.split('::')
        if start_type == 'city':
            path.append(start_id)
            
        return path[::-1]

    def _calculate_route_distance(self, route: List[str]) -> float:
        """Calcula distância total da rota"""
        if len(route) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(len(route) - 1):
            # Tentar usar distância pré-computada primeiro
            dist = self._get_precomputed_distance(route[i], route[i+1])
            if dist is None:
                # Calcular usando coordenadas
                city1 = self._get_node_info(route[i], 'city')
                city2 = self._get_node_info(route[i+1], 'city')
                if city1 and city2:
                    dist = haversine(city1['lat'], city1['lng'], city2['lat'], city2['lng'])
                else:
                    dist = 0.0
            total_distance += dist
        
        return total_distance

# ---------- INTERFACE CESIUM 3D ----------
def create_cesium_3d_map(route_df):
    """Cria mapa 3D usando Cesium via HTML/JavaScript"""
    
    # Preparar dados para Cesium
    cities_data = []
    for _, row in route_df.iterrows():
        cities_data.append({
            'name': row['name'],
            'lat': row['lat'],
            'lng': row['lng'],
            'country': row['country']
        })
    
    # HTML com Cesium 3D
    cesium_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cesium.com/downloads/cesiumjs/releases/1.95/Build/Cesium/Cesium.js"></script>
        <link href="https://cesium.com/downloads/cesiumjs/releases/1.95/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
        <style>
            html, body, #cesiumContainer {{
                width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div id="cesiumContainer"></div>
        <script>
            Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlYWE1OWUxNy1mMWZiLTQzYjYtYTQ0OS1kMWFjYmFkNjc5YzciLCJpZCI6NTc3MzMsImlhdCI6MTYyNzg0NTE4Mn0.XcKpgANiY19MC4bdFUXMVEBToBmqS8kuYpUlxJHYZxk';
            
            const viewer = new Cesium.Viewer('cesiumContainer');
            const cities = {cities_data};
            
            // Adicionar pontos das cidades
            cities.forEach((city, index) => {{
                viewer.entities.add({{
                    position: Cesium.Cartesian3.fromDegrees(city.lng, city.lat),
                    point: {{
                        pixelSize: 10,
                        color: index === 0 ? Cesium.Color.GREEN : (index === cities.length - 1 ? Cesium.Color.RED : Cesium.Color.YELLOW),
                        outlineColor: Cesium.Color.BLACK,
                        outlineWidth: 2
                    }},
                    label: {{
                        text: city.name,
                        font: '12pt sans-serif',
                        pixelOffset: new Cesium.Cartesian2(0, -40)
                    }}
                }});
            }});
            
            // Adicionar linha da rota
            if (cities.length > 1) {{
                const positions = cities.map(city => Cesium.Cartesian3.fromDegrees(city.lng, city.lat));
                viewer.entities.add({{
                    polyline: {{
                        positions: positions,
                        width: 3,
                        material: Cesium.Color.CYAN,
                        clampToGround: true
                    }}
                }});
            }}
            
            // Ajustar câmera para mostrar toda a rota
            viewer.zoomTo(viewer.entities);
        </script>
    </body>
    </html>
    """
    
    return cesium_html

# ---------- INTERFACE PYGWALKER ----------
def show_pygwalker_analysis(conn):
    """Mostra análise interativa com pygwalker"""
    st.subheader("📊 Análise Interativa de Dados com PyGWalker")
    
    # Carregar dados para análise
    query = """
    SELECT 
        c.name as city_name,
        c.country,
        c.lat,
        c.lng,
        co.name as continent_name,
        rb.name as regional_block_name
    FROM cities c
    JOIN countries ct ON c.country_id = ct.id
    JOIN continents co ON c.continent_id = co.id
    JOIN regional_blocks rb ON c.regional_block_id = rb.id
    LIMIT 5000
    """
    
    df_analysis = pd.read_sql_query(query, conn)
    
    if not df_analysis.empty:
        # Configurar PyGWalker
        pyg_html = pyg.to_html(df_analysis, spec="./gw_config.json", use_kernel_calc=True)
        st.components.v1.html(pyg_html, height=800, scrolling=True)
    else:
        st.warning("Não há dados suficientes para análise.")

# ---------- INTERFACE PRINCIPAL ----------
def show_admin_interface():
    """Interface de administração"""
    st.header("🛠️ Configurações do Sistema")
    
    if not check_db_exists():
        st.error("❌ Banco de dados não encontrado.")
        
        if st.button("📥 Baixar Dados e Criar Banco"):
            df = download_and_load_data()
            if df is not None:
                if not all(col in df.columns for col in REQUIRED_CSV_COLUMNS):
                    st.error(f"Colunas obrigatórias: {', '.join(REQUIRED_CSV_COLUMNS)}")
                    return
                
                create_optimized_database_structure()
                progress_bar = st.progress(0)
                status_text = st.empty()
                create_optimized_clusters(df, progress_bar, status_text)
    else:
        conn = sqlite3.connect(DB_PATH)
        stats = get_database_stats(conn)
        conn.close()
        
        st.success("✅ Sistema ativo!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cidades", f"{stats['cities']:,}")
        with col2:
            st.metric("Países", f"{stats['countries']:,}")
        with col3:
            st.metric("Continentes", f"{stats['continents']:,}")
        
        if st.button("🔄 Recriar Banco (Apaga atual)"):
            os.remove(DB_PATH)
            st.rerun()

def show_routing_interface(conn):
    """Interface de roteamento otimizada"""
    st.header("🚀 Roteamento Otimizado O(log n) → O(1)")
    
    cities_df = get_all_cities(conn)
    
    if cities_df.empty:
        st.warning("Carregue os dados primeiro.")
        return

    cities_list = cities_df.apply(lambda row: f"{row['name']} ({row['country']})", axis=1).tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        start_city_name = st.selectbox("🏁 Cidade de Origem:", cities_list, index=0)
    with col2:
        end_city_name = st.selectbox("🎯 Cidade de Destino:", cities_list, index=min(1, len(cities_list)-1))
    
    col3, col4 = st.columns(2)
    with col3:
        use_cesium = st.checkbox("🌍 Usar Cesium 3D", value=True)
    with col4:
        show_analysis = st.checkbox("📊 Mostrar Análise PyGWalker", value=False)
        
    if st.button("🔍 Encontrar Rota Otimizada"):
        start_id = cities_df.loc[cities_df['name'] + ' (' + cities_df['country'] + ')' == start_city_name, 'id'].iloc[0]
        end_id = cities_df.loc[cities_df['name'] + ' (' + cities_df['country'] + ')' == end_city_name, 'id'].iloc[0]
        
        if start_id and end_id:
            router = OptimizedHierarchicalRouter(conn)
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            import time
            start_time = time.time()
            route = router.find_path(start_id, end_id, status_text, progress_bar)
            end_time = time.time()
            
            status_text.empty()
            progress_bar.empty()
            
            if route:
                st.success(f"✅ Rota encontrada em {end_time - start_time:.3f}s")
                display_optimized_route(route, conn, use_cesium)
                
                if show_analysis:
                    show_pygwalker_analysis(conn)
            else:
                st.error("❌ Rota não encontrada")

def display_optimized_route(route: List, conn, use_cesium: bool = True):
    """Exibe rota com visualização otimizada"""
    if not route:
        return
        
    placeholders = ','.join(['?'] * len(route))
    query = f"""
    SELECT id, name, country, lat, lng 
    FROM cities 
    WHERE id IN ({placeholders}) 
    ORDER BY CASE id {' '.join([f"WHEN '{city_id}' THEN {i}" for i, city_id in enumerate(route)])} END
    """
    
    route_df = pd.read_sql_query(query, conn, params=route)
    
    if route_df.empty:
        return
    
    # Calcular distância total
    router = OptimizedHierarchicalRouter(conn)
    total_distance = router._calculate_route_distance(route)
    
    st.metric("📏 Distância Total", f"{total_distance:.2f} km")
    
    # Verificar se é rota global
    is_global_route = route_df['country'].nunique() > 1
    
    if use_cesium and is_global_route:
        st.subheader("🌍 Visualização Cesium 3D")
        cesium_html = create_cesium_3d_map(route_df)
        st.components.v1.html(cesium_html, height=600)
    else:
        # Fallback para Plotly
        if is_global_route:
            fig = px.line_geo(route_df, lat='lat', lon='lng', 
                              title='🌍 Rota Global',
                              projection='orthographic')
            fig.add_trace(px.scatter_geo(route_df, lat='lat', lon='lng', 
                                         hover_name='name').data[0])
        else:
            fig = px.line_mapbox(route_df, lat="lat", lon="lng", 
                                 zoom=4, height=500,
                                 hover_name="name",
                                 title="📍 Rota Local")
            fig.add_scattermapbox(lat=route_df['lat'], lon=route_df['lng'],
                                  mode='markers', 
                                  marker=dict(size=10, color='red'),
                                  text=route_df['name'])
            fig.update_layout(mapbox_style="open-street-map")
        
        st.plotly_chart(fig, use_container_width=True)
        
    # Detalhes da rota
    st.subheader("📋 Detalhes da Rota")
    for i, row in enumerate(route_df.itertuples(), start=1):
        st.write(f"{i}. {row.name} ({row.country})")

def main():
    """Função principal otimizada"""
    
    # Sidebar para navegação
    st.sidebar.title("🌍 Sistema de Roteamento")
    
    if check_db_exists():
        conn = sqlite3.connect(DB_PATH)
        stats = get_database_stats(conn)
        
        if stats['cities'] > 0:
            interface = st.sidebar.selectbox(
                "Escolha a Interface:",
                ["🚀 Roteamento", "📊 Análise PyGWalker", "🛠️ Administração"]
            )
            
            if interface == "🚀 Roteamento":
                show_routing_interface(conn)
            elif interface == "📊 Análise PyGWalker":
                show_pygwalker_analysis(conn)
            elif interface == "🛠️ Administração":
                show_admin_interface()
        else:
            st.warning("⚠️ Banco vazio. Configure na administração.")
            show_admin_interface()
        
        conn.close()
    else:
        show_admin_interface()

if __name__ == "__main__":
    main()

