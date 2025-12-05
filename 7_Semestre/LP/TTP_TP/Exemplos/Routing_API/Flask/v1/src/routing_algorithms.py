import sqlite3
import math
import heapq
from collections import defaultdict
import random

class RoutingAlgorithms:
    def __init__(self, db_name='routing_system.db'):
        self.db_name = db_name

    def _get_city_coordinates(self, city_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM cities WHERE id = ?", (city_id,))
        coords = cursor.fetchone()
        conn.close()
        return coords

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Raio da Terra em quilómetros

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def dijkstra(self, start_city_id, end_city_id, all_city_ids):
        graph = defaultdict(list)
        city_coords = {}

        for city_id in all_city_ids:
            coords = self._get_city_coordinates(city_id)
            if coords: 
                city_coords[city_id] = coords
            else:
                print(f"Coordenadas não encontradas para a cidade ID: {city_id}")
                return [], float('inf')

        for i, city1_id in enumerate(all_city_ids):
            for j, city2_id in enumerate(all_city_ids):
                if city1_id != city2_id:
                    lat1, lon1 = city_coords[city1_id]
                    lat2, lon2 = city_coords[city2_id]
                    distance = self.haversine_distance(lat1, lon1, lat2, lon2)
                    graph[city1_id].append((city2_id, distance))

        distances = {city_id: float('inf') for city_id in all_city_ids}
        distances[start_city_id] = 0
        previous_cities = {city_id: None for city_id in all_city_ids}
        priority_queue = [(0, start_city_id)]

        while priority_queue:
            current_distance, current_city_id = heapq.heappop(priority_queue)

            if current_distance > distances[current_city_id]:
                continue

            for neighbor_city_id, weight in graph[current_city_id]:
                distance = current_distance + weight
                if distance < distances[neighbor_city_id]:
                    distances[neighbor_city_id] = distance
                    previous_cities[neighbor_city_id] = current_city_id
                    heapq.heappush(priority_queue, (distance, neighbor_city_id))

        path = []
        current = end_city_id
        while current is not None:
            path.insert(0, current)
            current = previous_cities[current]

        if not path or path[0] != start_city_id:
            return [], float('inf')

        return path, distances[end_city_id]

    def kmeans(self, city_ids, num_clusters, max_iterations=100):
        if len(city_ids) < num_clusters:
            return {i: [city_id] for i, city_id in enumerate(city_ids)}

        city_data = {}
        for city_id in city_ids:
            coords = self._get_city_coordinates(city_id)
            if coords: 
                city_data[city_id] = list(coords)
            else:
                print(f"Coordenadas não encontradas para a cidade ID: {city_id}")
                return {}

        centroids = random.sample(list(city_data.values()), num_clusters)

        for _ in range(max_iterations):
            clusters = defaultdict(list)
            for city_id, (lat, lon) in city_data.items():
                min_distance = float('inf')
                closest_centroid_idx = -1
                for i, (c_lat, c_lon) in enumerate(centroids):
                    dist = self.haversine_distance(lat, lon, c_lat, c_lon)
                    if dist < min_distance:
                        min_distance = dist
                        closest_centroid_idx = i
                clusters[closest_centroid_idx].append(city_id)

            new_centroids = []
            for i in range(num_clusters):
                if clusters[i]:
                    cluster_lats = [city_data[city_id][0] for city_id in clusters[i]]
                    cluster_lons = [city_data[city_id][1] for city_id in clusters[i]]
                    new_centroids.append([
                        sum(cluster_lats) / len(cluster_lats),
                        sum(cluster_lons) / len(cluster_lons)
                    ])
                else:
                    new_centroids.append(random.choice(list(city_data.values())))
            
            if new_centroids == centroids:
                break
            centroids = new_centroids
        
        return clusters

    def tsp_nearest_neighbor(self, city_ids, start_city_id=None):
        if not city_ids:
            return [], 0

        if start_city_id is None:
            start_city_id = city_ids[0]

        unvisited_cities = set(city_ids)
        current_city = start_city_id
        tour = [current_city]
        unvisited_cities.remove(current_city)
        total_distance = 0

        while unvisited_cities:
            min_distance = float('inf')
            nearest_city = None
            
            current_coords = self._get_city_coordinates(current_city)
            if not current_coords:
                print(f"Coordenadas não encontradas para a cidade ID: {current_city}")
                return [], float('inf')
            current_lat, current_lon = current_coords

            for city_id in unvisited_cities:
                city_coords = self._get_city_coordinates(city_id)
                if not city_coords:
                    print(f"Coordenadas não encontradas para a cidade ID: {city_id}")
                    return [], float('inf')
                lat, lon = city_coords
                
                distance = self.haversine_distance(current_lat, current_lon, lat, lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_city = city_id
            
            if nearest_city is None:
                break

            tour.append(nearest_city)
            unvisited_cities.remove(nearest_city)
            total_distance += min_distance
            current_city = nearest_city

        if len(tour) > 1:
            start_coords = self._get_city_coordinates(tour[0])
            end_coords = self._get_city_coordinates(tour[-1])
            if start_coords and end_coords:
                total_distance += self.haversine_distance(end_coords[0], end_coords[1], start_coords[0], start_coords[1])
                tour.append(tour[0])

        return tour, total_distance


if __name__ == '__main__':
    router = RoutingAlgorithms()

    conn = sqlite3.connect(router.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM cities")
    cities_data = cursor.fetchall()
    conn.close()

    city_name_to_id = {name: id for id, name in cities_data}
    city_id_to_name = {id: name for id, name in cities_data}

    print("Cidades disponíveis:")
    for id, name in cities_data:
        print(f"  ID: {id}, Nome: {name}")

    all_city_ids = [id for id, _ in cities_data]

    if 'Lisboa' in city_name_to_id and 'Paris' in city_name_to_id:
        lisboa_id = city_name_to_id['Lisboa']
        paris_id = city_name_to_id['Paris']

        print(f"\nCalculando rota de {city_id_to_name[lisboa_id]} para {city_id_to_name[paris_id]} usando Dijkstra...")
        path, distance = router.dijkstra(lisboa_id, paris_id, all_city_ids)

        if path:
            path_names = [city_id_to_name[city_id] for city_id in path]
            print(f"Caminho: {' -> '.join(path_names)}")
            print(f"Distância total: {distance:.2f} km")
        else:
            print("Caminho não encontrado.")

    if 'Nova Iorque' in city_name_to_id and 'Tóquio' in city_name_to_id:
        ny_id = city_name_to_id['Nova Iorque']
        tokyo_id = city_name_to_id['Tóquio']

        print(f"\nCalculando rota de {city_id_to_name[ny_id]} para {city_id_to_name[tokyo_id]} usando Dijkstra...")
        path, distance = router.dijkstra(ny_id, tokyo_id, all_city_ids)

        if path:
            path_names = [city_id_to_name[city_id] for city_id in path]
            print(f"Caminho: {' -> '.join(path_names)}")
            print(f"Distância total: {distance:.2f} km")
        else:
            print("Caminho não encontrado.")

    print("\nTestando K-means com 3 clusters...")
    if 'Nova Iorque' in city_name_to_id and 'Tóquio' in city_name_to_id:
        city_ids_for_kmeans = [id for id, _ in cities_data if id not in [city_name_to_id['Nova Iorque'], city_name_to_id['Tóquio']]]
        if len(city_ids_for_kmeans) > 0:
            clusters = router.kmeans(city_ids_for_kmeans, num_clusters=3)
            for cluster_idx, c_ids in clusters.items():
                print(f"Cluster {cluster_idx}: {[city_id_to_name[cid] for cid in c_ids]}")

    print("\nTestando TSP (Vizinho Mais Próximo) com cidades europeias...")
    if 'Lisboa' in city_name_to_id:
        european_city_names = ['Lisboa', 'Porto', 'Faro', 'Madrid', 'Barcelona', 'Paris', 'Londres']
        european_city_ids = [city_name_to_id[name] for name in european_city_names if name in city_name_to_id]
        if european_city_ids:
            tsp_path, tsp_distance = router.tsp_nearest_neighbor(european_city_ids, start_city_id=city_name_to_id['Lisboa'])
            if tsp_path:
                tsp_path_names = [city_id_to_name[city_id] for city_id in tsp_path]
                print(f"Caminho TSP: {' -> '.join(tsp_path_names)}")
                print(f"Distância total TSP: {tsp_distance:.2f} km")

