// Variáveis globais
let scene, camera, renderer, globe, controls;
let cities = [];
let currentAlgorithm = 'dijkstra';
let routeLines = [];


// Função para criar textura da Terra proceduralmente(Prototipo Inicial)
function createEarthTexture(size = 512) {
    const canvas = document.createElement('canvas');
    canvas.width = size * 2; // Largura é 2x altura para mapeamento esférico correto
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    
    // Gradiente de fundo azul (oceanos)
    const oceanGradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    oceanGradient.addColorStop(0, '#1a2980');
    oceanGradient.addColorStop(1, '#26d0ce');
    
    ctx.fillStyle = oceanGradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Desenhar continentes (formas simplificadas)
    
    // América do Norte
    ctx.fillStyle = '#4CAF50';
    ctx.beginPath();
    ctx.ellipse(canvas.width * 0.25, canvas.height * 0.4, 120, 80, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // América do Sul
    ctx.beginPath();
    ctx.ellipse(canvas.width * 0.3, canvas.height * 0.7, 100, 120, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // África
    ctx.beginPath();
    ctx.ellipse(canvas.width * 0.5, canvas.height * 0.5, 100, 100, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Europa/Ásia
    ctx.fillStyle = '#8BC34A';
    ctx.beginPath();
    ctx.ellipse(canvas.width * 0.6, canvas.height * 0.4, 200, 100, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Austrália
    ctx.fillStyle = '#CDDC39';
    ctx.beginPath();
    ctx.ellipse(canvas.width * 0.8, canvas.height * 0.7, 60, 50, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Antártica (na parte inferior)
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, canvas.height - 30, canvas.width, 30);
    
    // Adicionar alguns detalhes (ilhas, etc.)
    ctx.fillStyle = '#388E3C';
    
    // Ilhas no Pacífico
    for (let i = 0; i < 15; i++) {
        const x = canvas.width * 0.1 + Math.random() * 0.8 * canvas.width;
        const y = Math.random() * canvas.height;
        const size = 5 + Math.random() * 8;
        
        if (x > canvas.width * 0.7 && x < canvas.width * 0.9 && y > canvas.height * 0.5) {
            continue; // Pular área oceânica específica
        }
        
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Adicionar nuvens (opcional)
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    for (let i = 0; i < 20; i++) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        const width = 30 + Math.random() * 40;
        const height = 15 + Math.random() * 20;
        
        ctx.beginPath();
        ctx.ellipse(x, y, width, height, 0, 0, Math.PI * 2);
        ctx.fill();
    }
    
    return canvas;
}

// Inicializar a cena 3D
function init() {
    // Configurar a cena
    scene = new THREE.Scene();
    
    // Configurar a câmera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 3;
    
    // Configurar o renderer
    const canvas = document.getElementById('globe-canvas');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Criar o globo
    const geometry = new THREE.SphereGeometry(1, 64, 64);


    // Criar textura da Terra proceduralmente
    //const earthCanvas = createEarthTexture(512);
    //const earthTexture = new THREE.CanvasTexture(earthCanvas);

    //Usando URL para gerar mapa de textura
    const textureLoader = new THREE.TextureLoader();
    const earthTexture = textureLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg');

    const material = new THREE.MeshPhongMaterial({
        map: earthTexture, // Aplicar a textura
        //color: 0x2194ce,
        emissive: 0x000000, // NOVO: Emissive preto para usar a cor da textura
        specular: 0x111111, // NOVO: Especular sutil
        shininess: 10, // NOVO: Brilho ajustado
        wireframe: false
    });
    globe = new THREE.Mesh(geometry, material);
    scene.add(globe);
    
    // Adicionar luzes
    const ambientLight = new THREE.AmbientLight(0x404040, 2);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);
    
    // Adicionar estrelas ao fundo
    addStars();
    
    // Controles de rotação do globo com o mouse
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const deltaX = e.clientX - previousMousePosition.x;
            const deltaY = e.clientY - previousMousePosition.y;
            
            globe.rotation.y += deltaX * 0.005;
            globe.rotation.x += deltaY * 0.005;
            
            previousMousePosition = { x: e.clientX, y: e.clientY };
        }
    });
    
    canvas.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
    });
    
    // Zoom com a roda do mouse
    canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        camera.position.z += e.deltaY * 0.001;
        camera.position.z = Math.max(1.5, Math.min(5, camera.position.z));
    });
    
    // Redimensionar ao alterar o tamanho da janela
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    // Carregar cidades
    loadCities();
    
    // Carregar países
    loadCountries();

    // Iniciar a animação
    animate();
}

// Adicionar estrelas ao fundo
function addStars() {
    const starGeometry = new THREE.BufferGeometry();
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.02 });
    
    const starVertices = [];
    for (let i = 0; i < 1000; i++) {
        const x = (Math.random() - 0.5) * 20;
        const y = (Math.random() - 0.5) * 20;
        const z = (Math.random() - 0.5) * 20;
        starVertices.push(x, y, z);
    }
    
    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);
}

// Função de animação
function animate() {
    requestAnimationFrame(animate);
    
    // Rotação automática suave do globo
    globe.rotation.y += 0.001;
    
    renderer.render(scene, camera);
}

// Converter coordenadas lat/lon para posição 3D no globo
function latLonToVector3(lat, lon, radius = 1) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    
    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const z = (radius * Math.sin(phi) * Math.sin(theta));
    const y = (radius * Math.cos(phi));
    
    return new THREE.Vector3(x, y, z);
}

// Carregar cidades da API
async function loadCities() {
    showLoading(true);
    try {
        const response = await fetch('/api/routing/cities');
        const data = await response.json();
        cities = data.cities;
        
        populateCitySelects();
        populateCityCheckboxes();
        addCityMarkers();
        
        showLoading(false);
    } catch (error) {
        console.error('Erro ao carregar cidades:', error);
        showLoading(false);
        showResult('Erro ao carregar cidades: ' + error.message);
    }
}

// Popular os selects de cidades
function populateCitySelects() {
    const startSelect = document.getElementById('start-city');
    const endSelect = document.getElementById('end-city');
    
    startSelect.innerHTML = '';
    endSelect.innerHTML = '';
    
    cities.forEach(city => {
        const option1 = document.createElement('option');
        option1.value = city.id;
        option1.textContent = city.name;
        startSelect.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = city.id;
        option2.textContent = city.name;
        endSelect.appendChild(option2);
    });
}

// Popular os checkboxes de cidades
function populateCityCheckboxes() {
    const tspContainer = document.getElementById('city-checkboxes');
    const kmeansContainer = document.getElementById('kmeans-city-checkboxes');
    
    tspContainer.innerHTML = '';
    kmeansContainer.innerHTML = '';
    
    cities.forEach(city => {
        const div1 = document.createElement('div');
        div1.className = 'city-checkbox';
        div1.innerHTML = `
            <input type="checkbox" id="tsp-city-${city.id}" value="${city.id}">
            <label for="tsp-city-${city.id}">${city.name}</label>
        `;
        tspContainer.appendChild(div1);
        
        const div2 = document.createElement('div');
        div2.className = 'city-checkbox';
        div2.innerHTML = `
            <input type="checkbox" id="kmeans-city-${city.id}" value="${city.id}">
            <label for="kmeans-city-${city.id}">${city.name}</label>
        `;
        kmeansContainer.appendChild(div2);
    });
}

// Adicionar marcadores de cidades no globo
function addCityMarkers() {
    cities.forEach(city => {
        const position = latLonToVector3(city.latitude, city.longitude, 1.01);
        
        const markerGeometry = new THREE.SphereGeometry(0.01, 16, 16);
        const markerMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        
        marker.position.copy(position);
        globe.add(marker);
    });
}

// NOVO: Função auxiliar para desenhar um polígono (fronteira)
function drawPolygon(coords, material) {
    const points = [];
    coords.forEach(coord => {
        // Coordenadas são [longitude, latitude]
        const vector = latLonToVector3(coord[1], coord[0], 1.001); // Raio ligeiramente maior que o globo
        points.push(vector);
    });
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);
    globe.add(line);
}

// NOVO: Carregar e desenhar fronteiras dos países
async function loadCountries() {
    try {
        // URL para o TopoJSON de países (1:110m)
        const worldData = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json");
        
        // Converter TopoJSON para GeoJSON (fronteiras dos países)
        const countries = topojson.feature(worldData, worldData.objects.countries);
        
        // Material para as linhas das fronteiras
        const lineMaterial = new THREE.LineBasicMaterial({ color: 0x00ff00, linewidth: 1 }); // Verde para as fronteiras
        
        countries.features.forEach(feature => {
            // A geometria pode ser MultiPolygon ou Polygon
            const geometryType = feature.geometry.type;
            const coordinates = feature.geometry.coordinates;
            
            if (geometryType === 'Polygon') {
                drawPolygon(coordinates[0], lineMaterial);
            } else if (geometryType === 'MultiPolygon') {
                coordinates.forEach(polygon => {
                    drawPolygon(polygon[0], lineMaterial);
                });
            }
        });
        
    } catch (error) {
        console.error('Erro ao carregar fronteiras dos países:', error);
    }
}

// Alternar entre algoritmos
function switchAlgorithm(algorithm) {
    currentAlgorithm = algorithm;
    
    // Atualizar tabs
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Mostrar/ocultar controles
    document.querySelectorAll('.algorithm-controls').forEach(control => {
        control.style.display = 'none';
    });
    document.getElementById(`${algorithm}-controls`).style.display = 'block';
    
    // Limpar resultado
    document.getElementById('result').innerHTML = '';
    
    // Limpar rotas anteriores
    clearRoutes();
}

// Calcular rota com Dijkstra
async function calculateDijkstra() {
    const startCityId = parseInt(document.getElementById('start-city').value);
    const endCityId = parseInt(document.getElementById('end-city').value);
    
    showLoading(true);
    clearRoutes();
    
    try {
        const response = await fetch('/api/routing/route/dijkstra', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start_city_id: startCityId, end_city_id: endCityId })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            drawRoute(data.path, 0x00ff00);
            showResult(`Rota calculada com sucesso!<br>Distância total: ${data.total_distance.toFixed(2)} km<br>Caminho: ${data.path.map(c => c.name).join(' → ')}`);
        } else {
            showResult('Erro: ' + data.error);
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Erro ao calcular rota:', error);
        showLoading(false);
        showResult('Erro ao calcular rota: ' + error.message);
    }
}

// Calcular rota com TSP
async function calculateTSP() {
    const checkboxes = document.querySelectorAll('#city-checkboxes input[type="checkbox"]:checked');
    const cityIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
    
    if (cityIds.length < 2) {
        showResult('Por favor, selecione pelo menos 2 cidades.');
        return;
    }
    
    showLoading(true);
    clearRoutes();
    
    try {
        const response = await fetch('/api/routing/route/tsp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city_ids: cityIds, start_city_id: cityIds[0] })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            drawRoute(data.tour, 0xff00ff);
            showResult(`Rota TSP calculada com sucesso!<br>Distância total: ${data.total_distance.toFixed(2)} km<br>Caminho: ${data.tour.map(c => c.name).join(' → ')}`);
        } else {
            showResult('Erro: ' + data.error);
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Erro ao calcular TSP:', error);
        showLoading(false);
        showResult('Erro ao calcular TSP: ' + error.message);
    }
}

// Calcular clusters com K-means
async function calculateKMeans() {
    const checkboxes = document.querySelectorAll('#kmeans-city-checkboxes input[type="checkbox"]:checked');
    const cityIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
    const numClusters = parseInt(document.getElementById('num-clusters').value);
    
    if (cityIds.length < numClusters) {
        showResult(`Por favor, selecione pelo menos ${numClusters} cidades.`);
        return;
    }
    
    showLoading(true);
    clearRoutes();
    
    try {
        const response = await fetch('/api/routing/route/kmeans', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city_ids: cityIds, num_clusters: numClusters })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffa500, 0x800080, 0x008000, 0x000080];
            let resultText = 'Clusters calculados com sucesso!<br><br>';
            
            Object.keys(data.clusters).forEach((clusterIdx, i) => {
                const cluster = data.clusters[clusterIdx];
                const color = colors[i % colors.length];
                
                // Destacar cidades do cluster
                cluster.forEach(city => {
                    const position = latLonToVector3(city.latitude, city.longitude, 1.02);
                    const markerGeometry = new THREE.SphereGeometry(0.02, 16, 16);
                    const markerMaterial = new THREE.MeshBasicMaterial({ color });
                    const marker = new THREE.Mesh(markerGeometry, markerMaterial);
                    marker.position.copy(position);
                    globe.add(marker);
                    routeLines.push(marker);
                });
                
                resultText += `<strong>Cluster ${parseInt(clusterIdx) + 1}:</strong> ${cluster.map(c => c.name).join(', ')}<br>`;
            });
            
            showResult(resultText);
        } else {
            showResult('Erro: ' + data.error);
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Erro ao calcular K-means:', error);
        showLoading(false);
        showResult('Erro ao calcular K-means: ' + error.message);
    }
}

// Desenhar rota no globo
function drawRoute(path, color) {
    if (path.length < 2) return;
    
    for (let i = 0; i < path.length - 1; i++) {
        const start = latLonToVector3(path[i].latitude, path[i].longitude, 1.01);
        const end = latLonToVector3(path[i + 1].latitude, path[i + 1].longitude, 1.01);
        
        const curve = new THREE.QuadraticBezierCurve3(
            start,
            start.clone().lerp(end, 0.5).multiplyScalar(1.2),
            end
        );
        
        const points = curve.getPoints(50);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ color, linewidth: 2 });
        const line = new THREE.Line(geometry, material);
        
        globe.add(line);
        routeLines.push(line);
    }
}

// Limpar rotas anteriores
function clearRoutes() {
    routeLines.forEach(line => {
        globe.remove(line);
    });
    routeLines = [];
}

// Mostrar/ocultar loading
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// Mostrar resultado
function showResult(message) {
    document.getElementById('result').innerHTML = message;
}

// Inicializar quando a página carregar
window.addEventListener('DOMContentLoaded', init);

