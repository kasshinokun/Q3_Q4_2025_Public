from flask import Blueprint, request, jsonify
import sqlite3
import os
from routing_algorithms import RoutingAlgorithms
from quadtree_logic import Quadtree

routing_bp = Blueprint('routing', __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'routing_system.db')

@routing_bp.route('/cities', methods=['GET'])
def get_cities():
    """Retorna todas as cidades disponíveis no banco de dados."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude FROM cities")
        cities = cursor.fetchall()
        conn.close()
        
        cities_list = [
            {'id': city[0], 'name': city[1], 'latitude': city[2], 'longitude': city[3]}
            for city in cities
        ]
        
        return jsonify({'cities': cities_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routing_bp.route('/cities/search', methods=['POST'])
def search_cities():
    """Busca cidades numa região específica usando a Quadtree."""
    try:
        data = request.get_json()
        min_lat = data.get('min_lat')
        max_lat = data.get('max_lat')
        min_lon = data.get('min_lon')
        max_lon = data.get('max_lon')
        
        if None in [min_lat, max_lat, min_lon, max_lon]:
            return jsonify({'error': 'Parâmetros de caixa delimitadora faltando'}), 400
        
        qt = Quadtree(db_name=DB_PATH)
        cities = qt.find_cities_in_region(min_lat, max_lat, min_lon, max_lon)
        
        return jsonify({'cities': cities}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routing_bp.route('/route/dijkstra', methods=['POST'])
def calculate_dijkstra_route():
    """Calcula a rota mais curta entre duas cidades usando Dijkstra."""
    try:
        data = request.get_json()
        start_city_id = data.get('start_city_id')
        end_city_id = data.get('end_city_id')
        
        if not start_city_id or not end_city_id:
            return jsonify({'error': 'IDs de cidade de início e fim são obrigatórios'}), 400
        
        router = RoutingAlgorithms(db_name=DB_PATH)
        
        # Obter todas as cidades para construir o grafo
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cities")
        all_city_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        path, distance = router.dijkstra(start_city_id, end_city_id, all_city_ids)
        
        if not path:
            return jsonify({'error': 'Caminho não encontrado'}), 404
        
        # Obter coordenadas para cada cidade no caminho
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        path_with_coords = []
        for city_id in path:
            cursor.execute("SELECT id, name, latitude, longitude FROM cities WHERE id = ?", (city_id,))
            city_data = cursor.fetchone()
            if city_data:
                path_with_coords.append({
                    'id': city_data[0],
                    'name': city_data[1],
                    'latitude': city_data[2],
                    'longitude': city_data[3]
                })
        conn.close()
        
        return jsonify({
            'path': path_with_coords,
            'total_distance': distance
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routing_bp.route('/route/kmeans', methods=['POST'])
def calculate_kmeans_clusters():
    """Agrupa cidades em clusters usando K-means."""
    try:
        data = request.get_json()
        city_ids = data.get('city_ids')
        num_clusters = data.get('num_clusters', 3)
        
        if not city_ids:
            return jsonify({'error': 'IDs de cidades são obrigatórios'}), 400
        
        router = RoutingAlgorithms(db_name=DB_PATH)
        clusters = router.kmeans(city_ids, num_clusters)
        
        # Obter informações das cidades para cada cluster
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        clusters_with_info = {}
        for cluster_idx, c_ids in clusters.items():
            cluster_cities = []
            for city_id in c_ids:
                cursor.execute("SELECT id, name, latitude, longitude FROM cities WHERE id = ?", (city_id,))
                city_data = cursor.fetchone()
                if city_data:
                    cluster_cities.append({
                        'id': city_data[0],
                        'name': city_data[1],
                        'latitude': city_data[2],
                        'longitude': city_data[3]
                    })
            clusters_with_info[str(cluster_idx)] = cluster_cities
        conn.close()
        
        return jsonify({'clusters': clusters_with_info}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routing_bp.route('/route/tsp', methods=['POST'])
def calculate_tsp_route():
    """Calcula a rota do Caixeiro Viajante usando o algoritmo do vizinho mais próximo."""
    try:
        data = request.get_json()
        city_ids = data.get('city_ids')
        start_city_id = data.get('start_city_id')
        
        if not city_ids:
            return jsonify({'error': 'IDs de cidades são obrigatórios'}), 400
        
        router = RoutingAlgorithms(db_name=DB_PATH)
        tour, total_distance = router.tsp_nearest_neighbor(city_ids, start_city_id)
        
        if not tour:
            return jsonify({'error': 'Caminho TSP não encontrado'}), 404
        
        # Obter coordenadas para cada cidade no tour
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        tour_with_coords = []
        for city_id in tour:
            cursor.execute("SELECT id, name, latitude, longitude FROM cities WHERE id = ?", (city_id,))
            city_data = cursor.fetchone()
            if city_data:
                tour_with_coords.append({
                    'id': city_data[0],
                    'name': city_data[1],
                    'latitude': city_data[2],
                    'longitude': city_data[3]
                })
        conn.close()
        
        return jsonify({
            'tour': tour_with_coords,
            'total_distance': total_distance
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

