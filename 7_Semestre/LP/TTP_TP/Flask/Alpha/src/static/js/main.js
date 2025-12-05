/**
 * JavaScript principal da apresentação
 * Demonstra características do JavaScript: programação funcional, orientada a eventos, assíncrona
 */

// Classe para gerenciar a navegação (POO em JavaScript)
class NavigationManager {
    constructor() {
        this.navToggle = document.getElementById('nav-toggle');
        this.sidebar = document.getElementById('sidebar');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSmoothScrolling();
        this.setupCodeHighlighting();
        this.setupAnimations();
        this.highlightCurrentPage();
    }

    // Programação orientada a eventos
    setupEventListeners() {
        // Toggle do menu mobile
        if (this.navToggle && this.sidebar) {
            this.navToggle.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Fechar menu ao clicar em um link
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMobileMenu());
        });

        // Fechar menu ao redimensionar a tela
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.closeMobileMenu();
            }
        });

        // Adicionar efeitos de hover nos cards
        this.setupCardEffects();
    }

    toggleMobileMenu() {
        this.sidebar.classList.toggle('active');
        this.navToggle.classList.toggle('active');
    }

    closeMobileMenu() {
        this.sidebar.classList.remove('active');
        this.navToggle.classList.remove('active');
    }

    // Destacar página atual no menu
    highlightCurrentPage() {
        const currentPath = window.location.pathname;
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        
        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    // Programação funcional - uso de higher-order functions
    setupCardEffects() {
        const cards = document.querySelectorAll('.nav-card, .key-point, .paradigm-card');
        
        // Usando map para aplicar efeitos a todos os cards
        Array.from(cards).map(card => {
            card.addEventListener('mouseenter', this.addHoverEffect);
            card.addEventListener('mouseleave', this.removeHoverEffect);
        });
    }

    // Arrow functions (ES6+)
    addHoverEffect = (event) => {
        event.target.style.transform = 'translateY(-5px) scale(1.02)';
    }

    removeHoverEffect = (event) => {
        event.target.style.transform = '';
    }

    setupSmoothScrolling() {
        // Smooth scrolling para links internos
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        internalLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupCodeHighlighting() {
        // Melhorar a exibição de código
        const codeBlocks = document.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
            // Adicionar números de linha
            this.addLineNumbers(block);
            
            // Adicionar botão de cópia
            this.addCopyButton(block.parentElement);
        });
    }

    addLineNumbers(codeBlock) {
        const lines = codeBlock.textContent.split('\n');
        const numberedLines = lines.map((line, index) => {
            if (index === lines.length - 1 && line.trim() === '') return '';
            return `<span class="line-number">${index + 1}</span>${line}`;
        }).join('\n');
        
        codeBlock.innerHTML = numberedLines;
    }

    addCopyButton(preElement) {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copiar';
        copyButton.addEventListener('click', () => this.copyCode(preElement, copyButton));
        
        preElement.style.position = 'relative';
        preElement.appendChild(copyButton);
    }

    // Programação assíncrona com async/await
    async copyCode(preElement, button) {
        const code = preElement.querySelector('code').textContent;
        
        try {
            await navigator.clipboard.writeText(code);
            button.textContent = 'Copiado!';
            button.style.background = '#28a745';
            
            // Usar setTimeout com Promise para demonstrar programação assíncrona
            await this.delay(2000);
            button.textContent = 'Copiar';
            button.style.background = '';
        } catch (err) {
            console.error('Erro ao copiar código:', err);
            button.textContent = 'Erro';
            await this.delay(2000);
            button.textContent = 'Copiar';
        }
    }

    // Função utilitária que retorna uma Promise (programação assíncrona)
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    setupAnimations() {
        // Intersection Observer para animações ao scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observar elementos para animação
        const animatedElements = document.querySelectorAll('.slide, .key-point, .paradigm-card, .timeline-item');
        animatedElements.forEach(el => observer.observe(el));
    }
}

// Classe para gerenciar temas (demonstra encapsulamento)
class ThemeManager {
    constructor() {
        this.currentTheme = 'python';
        this.init();
    }

    init() {
        this.detectPageTheme();
        this.applyTheme();
    }

    detectPageTheme() {
        const path = window.location.pathname;
        if (path.includes('javascript')) {
            this.currentTheme = 'javascript';
        }
    }

    applyTheme() {
        if (this.currentTheme === 'javascript') {
            document.body.classList.add('js-theme');
        }
    }

    // Método público para trocar tema
    switchTheme(theme) {
        document.body.classList.remove('js-theme');
        if (theme === 'javascript') {
            document.body.classList.add('js-theme');
        }
        this.currentTheme = theme;
    }
}

// Funções utilitárias (programação funcional)
const utils = {
    // Debounce function para otimizar performance
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Função para formatar texto
    formatText: (text) => text.trim().replace(/\s+/g, ' '),

    // Função para validar email (regex)
    isValidEmail: (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),

    // Função para gerar ID único
    generateId: () => Math.random().toString(36).substr(2, 9),

    // Função para animar números (contador)
    animateNumber: (element, start, end, duration) => {
        const startTime = performance.now();
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (end - start) * progress);
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }
};

// Função para adicionar estilos CSS dinamicamente
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }
        
        .copy-button:hover {
            background: #0056b3;
        }
        
        .line-number {
            display: inline-block;
            width: 30px;
            color: #666;
            user-select: none;
            margin-right: 10px;
        }
        
        .animate-in {
            animation: slideInUp 0.6s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
    `;
    document.head.appendChild(style);
}

// Event listener para quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar managers
    const navigationManager = new NavigationManager();
    const themeManager = new ThemeManager();
    
    // Adicionar estilos dinâmicos
    addDynamicStyles();
    
    // Adicionar funcionalidades específicas da página
    initPageSpecificFeatures();
    
    // Log para demonstrar console.log do JavaScript
    console.log('🐍 Apresentação Python & JavaScript carregada!');
    console.log('📊 Demonstrando características do JavaScript:');
    console.log('   ✓ Programação orientada a eventos');
    console.log('   ✓ Programação funcional (map, filter, arrow functions)');
    console.log('   ✓ Programação assíncrona (async/await, Promises)');
    console.log('   ✓ POO com classes ES6+');
    console.log('   ✓ Manipulação do DOM');
});

// Função para inicializar recursos específicos da página
function initPageSpecificFeatures() {
    // Adicionar contador de caracteres em exemplos de código
    const codeExamples = document.querySelectorAll('.code-example code');
    codeExamples.forEach((code, index) => {
        const charCount = code.textContent.length;
        console.log(`Exemplo ${index + 1}: ${charCount} caracteres`);
    });
    
    // Adicionar tooltips informativos
    addTooltips();
    
    // Configurar lazy loading para imagens (se houver)
    setupLazyLoading();
}

// Função para adicionar tooltips
function addTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.getAttribute('data-tooltip');
    tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    
    event.target._tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target._tooltip) {
        document.body.removeChild(event.target._tooltip);
        delete event.target._tooltip;
    }
}

// Função para configurar lazy loading
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Exportar para uso global (se necessário)
window.PresentationApp = {
    NavigationManager,
    ThemeManager,
    utils
};

    // Programação funcional - uso de higher-order functions
    setupCardEffects() {
        const cards = document.querySelectorAll('.nav-card, .key-point, .paradigm-card');
        
        // Usando map para aplicar efeitos a todos os cards
        Array.from(cards).map(card => {
            card.addEventListener('mouseenter', this.addHoverEffect);
            card.addEventListener('mouseleave', this.removeHoverEffect);
        });
    }

    // Arrow functions (ES6+)
    addHoverEffect = (event) => {
        event.target.style.transform = 'translateY(-5px) scale(1.02)';
    }

    removeHoverEffect = (event) => {
        event.target.style.transform = '';
    }

    setupSmoothScrolling() {
        // Smooth scrolling para links internos
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        internalLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupCodeHighlighting() {
        // Melhorar a exibição de código
        const codeBlocks = document.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
            // Adicionar números de linha
            this.addLineNumbers(block);
            
            // Adicionar botão de cópia
            this.addCopyButton(block.parentElement);
        });
    }

    addLineNumbers(codeBlock) {
        const lines = codeBlock.textContent.split('\n');
        const numberedLines = lines.map((line, index) => {
            if (index === lines.length - 1 && line.trim() === '') return '';
            return `<span class="line-number">${index + 1}</span>${line}`;
        }).join('\n');
        
        codeBlock.innerHTML = numberedLines;
    }

    addCopyButton(preElement) {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copiar';
        copyButton.addEventListener('click', () => this.copyCode(preElement, copyButton));
        
        preElement.style.position = 'relative';
        preElement.appendChild(copyButton);
    }

    // Programação assíncrona com async/await
    async copyCode(preElement, button) {
        const code = preElement.querySelector('code').textContent;
        
        try {
            await navigator.clipboard.writeText(code);
            button.textContent = 'Copiado!';
            button.style.background = '#28a745';
            
            // Usar setTimeout com Promise para demonstrar programação assíncrona
            await this.delay(2000);
            button.textContent = 'Copiar';
            button.style.background = '';
        } catch (err) {
            console.error('Erro ao copiar código:', err);
            button.textContent = 'Erro';
            await this.delay(2000);
            button.textContent = 'Copiar';
        }
    }

    // Função utilitária que retorna uma Promise (programação assíncrona)
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    setupAnimations() {
        // Intersection Observer para animações ao scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observar elementos para animação
        const animatedElements = document.querySelectorAll('.slide, .key-point, .paradigm-card, .timeline-item');
        animatedElements.forEach(el => observer.observe(el));
    }
}

// Classe para gerenciar temas (demonstra encapsulamento)
class ThemeManager {
    constructor() {
        this.currentTheme = 'python';
        this.init();
    }

    init() {
        this.detectPageTheme();
        this.applyTheme();
    }

    detectPageTheme() {
        const path = window.location.pathname;
        if (path.includes('javascript')) {
            this.currentTheme = 'javascript';
        }
    }

    applyTheme() {
        if (this.currentTheme === 'javascript') {
            document.body.classList.add('js-theme');
        }
    }

    // Método público para trocar tema
    switchTheme(theme) {
        document.body.classList.remove('js-theme');
        if (theme === 'javascript') {
            document.body.classList.add('js-theme');
        }
        this.currentTheme = theme;
    }
}

// Funções utilitárias (programação funcional)
const utils = {
    // Debounce function para otimizar performance
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Função para formatar texto
    formatText: (text) => text.trim().replace(/\s+/g, ' '),

    // Função para validar email (regex)
    isValidEmail: (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),

    // Função para gerar ID único
    generateId: () => Math.random().toString(36).substr(2, 9),

    // Função para animar números (contador)
    animateNumber: (element, start, end, duration) => {
        const startTime = performance.now();
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (end - start) * progress);
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }
};

// Função para adicionar estilos CSS dinamicamente
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }
        
        .copy-button:hover {
            background: #0056b3;
        }
        
        .line-number {
            display: inline-block;
            width: 30px;
            color: #666;
            user-select: none;
            margin-right: 10px;
        }
        
        .animate-in {
            animation: slideInUp 0.6s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
    `;
    document.head.appendChild(style);
}

// Event listener para quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar managers
    const navigationManager = new NavigationManager();
    const themeManager = new ThemeManager();
    
    // Adicionar estilos dinâmicos
    addDynamicStyles();
    
    // Adicionar funcionalidades específicas da página
    initPageSpecificFeatures();
    
    // Log para demonstrar console.log do JavaScript
    console.log('🐍 Apresentação Python & JavaScript carregada!');
    console.log('📊 Demonstrando características do JavaScript:');
    console.log('   ✓ Programação orientada a eventos');
    console.log('   ✓ Programação funcional (map, filter, arrow functions)');
    console.log('   ✓ Programação assíncrona (async/await, Promises)');
    console.log('   ✓ POO com classes ES6+');
    console.log('   ✓ Manipulação do DOM');
});

// Função para inicializar recursos específicos da página
function initPageSpecificFeatures() {
    // Adicionar contador de caracteres em exemplos de código
    const codeExamples = document.querySelectorAll('.code-example code');
    codeExamples.forEach((code, index) => {
        const charCount = code.textContent.length;
        console.log(`Exemplo ${index + 1}: ${charCount} caracteres`);
    });
    
    // Adicionar tooltips informativos
    addTooltips();
    
    // Configurar lazy loading para imagens (se houver)
    setupLazyLoading();
}

// Função para adicionar tooltips
function addTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.getAttribute('data-tooltip');
    tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    
    event.target._tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target._tooltip) {
        document.body.removeChild(event.target._tooltip);
        delete event.target._tooltip;
    }
}

// Função para configurar lazy loading
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Exportar para uso global (se necessário)
window.PresentationApp = {
    NavigationManager,
    ThemeManager,
    utils
};

