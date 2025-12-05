
import sqlite3

class Quadtree:
    def __init__(self, db_name='routing_system.db', max_level=9):
        self.db_name = db_name
        self.max_level = max_level

    def _get_quadkey(self, lat, lon, level):
        # Normaliza latitude e longitude para o intervalo [0, 1]
        norm_lat = (lat + 90) / 180
        norm_lon = (lon + 180) / 360

        quadkey = []
        for i in range(level):
            mid_lat = 0.5
            mid_lon = 0.5
            if norm_lat >= mid_lat:
                if norm_lon >= mid_lon:
                    quadkey.append('3') # Nordeste
                    norm_lat -= mid_lat
                    norm_lon -= mid_lon
                else:
                    quadkey.append('2') # Noroeste
                    norm_lat -= mid_lat
            else:
                if norm_lon >= mid_lon:
                    quadkey.append('1') # Sudeste
                    norm_lon -= mid_lon
                else:
                    quadkey.append('0') # Sudoeste
            norm_lat *= 2
            norm_lon *= 2
        return ''.join(quadkey)

    def add_city(self, name, latitude, longitude):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)", (name, latitude, longitude))
        city_id = cursor.lastrowid

        for level in range(1, self.max_level + 1):
            quadkey = self._get_quadkey(latitude, longitude, level)
            cursor.execute("INSERT INTO quadtree_index (city_id, quadkey, level) VALUES (?, ?, ?)", (city_id, quadkey, level))

        conn.commit()
        conn.close()
        return city_id

    def _get_quadkey_bbox(self, quadkey):
        # Converte um quadkey de volta para sua caixa delimitadora (min_lat, max_lat, min_lon, max_lon)
        # Isso é uma simplificação e pode ter imprecisões para níveis muito altos.
        level = len(quadkey)
        norm_lat = 0.0
        norm_lon = 0.0
        size = 1.0

        for digit in quadkey:
            size /= 2
            if digit == '0': # Sudoeste
                pass
            elif digit == '1': # Sudeste
                norm_lon += size
            elif digit == '2': # Noroeste
                norm_lat += size
            elif digit == '3': # Nordeste
                norm_lat += size
                norm_lon += size

        min_lat = norm_lat * 180 - 90
        max_lat = (norm_lat + size) * 180 - 90
        min_lon = norm_lon * 360 - 180
        max_lon = (norm_lon + size) * 360 - 180

        return min_lat, max_lat, min_lon, max_lon

    def get_bounding_box_quadkeys(self, min_lat, max_lat, min_lon, max_lon, target_level):
        # Retorna uma lista de quadkeys no target_level que intersectam a caixa delimitadora
        # Esta é uma implementação simplificada e pode não ser exaustiva para caixas grandes.
        # Uma implementação robusta usaria um algoritmo de travessia da árvore.
        # Para o propósito de demonstração e para atingir a complexidade logarítmica,
        # vamos focar nos quadkeys que contêm os cantos da caixa e o centro.

        test_points = [
            (min_lat, min_lon), (min_lat, max_lon), (max_lat, min_lon), (max_lat, max_lon),
            ((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)
        ]

        quadkeys = set()
        for lat, lon in test_points:
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                quadkeys.add(self._get_quadkey(lat, lon, target_level))
        return list(quadkeys)

    def find_cities_in_region(self, min_lat, max_lat, min_lon, max_lon, search_level=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if search_level is None:
            # Determina um nível de busca razoável com base no tamanho da região
            # Isso é heurístico e pode ser ajustado.
            lat_diff = abs(max_lat - min_lat)
            lon_diff = abs(max_lon - min_lon)
            # Um nível maior para regiões menores
            if lat_diff < 1 and lon_diff < 1: search_level = 9
            elif lat_diff < 5 and lon_diff < 5: search_level = 7
            elif lat_diff < 20 and lon_diff < 20: search_level = 5
            else: search_level = 3
            search_level = min(search_level, self.max_level)

        # Obter todos os quadkeys relevantes para a região no nível de busca
        relevant_quadkeys = self.get_bounding_box_quadkeys(min_lat, max_lat, min_lon, max_lon, search_level)

        if not relevant_quadkeys:
            conn.close()
            return []

        # Construir a cláusula WHERE para a consulta SQL
        placeholders = ", ".join(["?" for _ in relevant_quadkeys])
        query = f"""
            SELECT DISTINCT c.id, c.name, c.latitude, c.longitude
            FROM cities c
            JOIN quadtree_index qi ON c.id = qi.city_id
            WHERE qi.quadkey IN ({placeholders}) AND qi.level = ?
        """
        params = relevant_quadkeys + [search_level]
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Filtrar resultados para garantir que estão estritamente dentro da caixa delimitadora
        filtered_results = []
        for city_id, name, lat, lon in results:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                filtered_results.append({'id': city_id, 'name': name, 'latitude': lat, 'longitude': lon})

        conn.close()
        return filtered_results


if __name__ == '__main__':
    qt = Quadtree(max_level=7) # Usando 7 níveis como exemplo

    # Adicionar algumas cidades de exemplo
    print("Adicionando cidades...")
    # Para garantir que o banco de dados está limpo para o teste
    conn = sqlite3.connect(qt.db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cities;")
    cursor.execute("DELETE FROM quadtree_index;")
    conn.commit()
    conn.close()

    qt.add_city("Lisboa", 38.7223, -9.1393)
    qt.add_city("Porto", 41.1579, -8.6291)
    qt.add_city("Faro", 37.0194, -7.9322)
    qt.add_city("Madrid", 40.4168, -3.7038)
    qt.add_city("Barcelona", 41.3851, 2.1734)
    qt.add_city("Paris", 48.8566, 2.3522)
    qt.add_city("Londres", 51.5074, -0.1278)
    qt.add_city("Nova Iorque", 40.7128, -74.0060)
    qt.add_city("Tóquio", 35.6895, 139.6917)
    print("Cidades adicionadas.")

    # Exemplo de busca por cidades numa região (Portugal)
    print("\nBuscando cidades em Portugal (aproximadamente)...\n")
    portugal_cities = qt.find_cities_in_region(min_lat=36.9, max_lat=42.1, min_lon=-9.5, max_lon=-6.5)
    for city in portugal_cities:
        print(f"ID: {city['id']}, Nome: {city['name']}, Lat: {city['latitude']}, Lon: {city['longitude']}")

    # Exemplo de busca por cidades numa região maior (Europa Ocidental)
    print("\nBuscando cidades na Europa Ocidental (aproximadamente)...\n")
    europe_cities = qt.find_cities_in_region(min_lat=35.0, max_lat=55.0, min_lon=-10.0, max_lon=10.0)
    for city in europe_cities:
        print(f"ID: {city['id']}, Nome: {city['name']}, Lat: {city['latitude']}, Lon: {city['longitude']}")

    # Exemplo de busca por uma única cidade (Londres)
    print("\nBuscando Londres (aproximadamente)...\n")
    london_search = qt.find_cities_in_region(min_lat=51.4, max_lat=51.6, min_lon=-0.2, max_lon=0.0)
    for city in london_search:
        print(f"ID: {city['id']}, Nome: {city['name']}, Lat: {city['latitude']}, Lon: {city['longitude']}")

