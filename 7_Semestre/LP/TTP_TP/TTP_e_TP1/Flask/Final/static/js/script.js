/**
 * SISTEMA DE APRESENTAÇÕES FLASK - JAVASCRIPT
 * Gerencia interações da sidebar, dropdown e sincronização com Reveal.js
 */

// ============================================================================
// INICIALIZAÇÃO DO REVEAL.JS
// ============================================================================
Reveal.initialize({
    // Configurações de navegação
    hash: true,
    hashOneBasedIndex: false,
    respondToHashChanges: true,
    
    // Configurações de transição
    transition: 'slide',
    transitionSpeed: 'default',
    backgroundTransition: 'fade',
    
    // Configurações de UI
    slideNumber: 'c/t',
    controls: true,
    progress: true,
    center: true,
    touch: true,
    loop: false,
    
    // Configurações de navegação
    navigationMode: 'default',
    shuffle: false,
    
    // Configurações de fragmentos
    fragments: true,
    fragmentInURL: true,
    
    // Outras configurações
    embedded: false,
    help: true,
    showNotes: false,
    autoPlayMedia: null,
    preloadIframes: null,
    autoSlide: 0,
    autoSlideStoppable: true,
    mouseWheel: false,
    hideInactiveCursor: true,
    hideCursorTime: 5000,
    previewLinks: false,
    
    // Dimensões
    width: 1366,
    height: 768,
    margin: 0.02,
    minScale: 0.2,
    maxScale: 2.0,
    
    // Plugins
    plugins: [RevealMarkdown, RevealHighlight, RevealNotes]
});

console.log('✓ Reveal.js inicializado');

// ============================================================================
// DROPDOWN DE SELEÇÃO DE APRESENTAÇÃO
// ============================================================================
const dropdownToggle = document.getElementById('dropdown-toggle');
const dropdownMenu = document.getElementById('dropdown-menu');

if (dropdownToggle && dropdownMenu) {
    // Toggle dropdown ao clicar no botão
    dropdownToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
        console.log('Dropdown toggled:', dropdownMenu.classList.contains('show'));
    });

    // Fechar dropdown ao clicar fora
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            dropdownMenu.classList.remove('show');
        }
    });

    // Fechar dropdown ao pressionar ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && dropdownMenu.classList.contains('show')) {
            dropdownMenu.classList.remove('show');
        }
    });

    console.log('✓ Dropdown de apresentações configurado');
}

// ============================================================================
// SIDEBAR TOGGLE
// ============================================================================
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggle-sidebar');
const closeBtn = document.getElementById('close-sidebar');
const revealContainer = document.querySelector('.reveal');

/**
 * Função para alternar a visibilidade da sidebar
 */
function toggleSidebar() {
    const isHidden = sidebar.classList.contains('hidden');
    
    sidebar.classList.toggle('hidden');
    revealContainer.classList.toggle('full-width');
    
    // Atualizar layout do Reveal.js
    setTimeout(() => {
        Reveal.layout();
        Reveal.sync();
    }, 300);
    
    // Atualizar estado do botão na top bar
    updateToggleButtonState(!isHidden);
    
    console.log('Sidebar toggled:', !isHidden);
}

/**
 * Atualiza o estado visual do botão de toggle
 * @param {boolean} isSidebarVisible - Se a sidebar está visível
 */
function updateToggleButtonState(isSidebarVisible) {
    if (toggleBtn) {
        const icon = toggleBtn.querySelector('.hamburger-icon');
        const text = toggleBtn.querySelector('.toggle-text');
        
        if (isSidebarVisible) {
            // Sidebar está aberta
            if (icon) icon.textContent = '☰';
            if (text) text.textContent = 'Sumário';
        } else {
            // Sidebar está fechada
            if (icon) icon.textContent = '📑';
            if (text) text.textContent = 'Fechar Sumário';
        }
    }
}

// Configurar eventos de toggle
if (toggleBtn && sidebar && revealContainer) {
    toggleBtn.addEventListener('click', toggleSidebar);
    console.log('✓ Toggle da sidebar configurado');
}

if (closeBtn && sidebar && revealContainer) {
    closeBtn.addEventListener('click', toggleSidebar);
    console.log('✓ Botão fechar da sidebar configurado');
}

// ============================================================================
// SUBMENU DROPDOWN NA SIDEBAR
// ============================================================================
const navItemsWithSubmenu = document.querySelectorAll('.nav-item-with-submenu');

navItemsWithSubmenu.forEach(item => {
    const navLink = item.querySelector('.nav-link');
    const submenu = item.querySelector('.submenu');
    
    if (navLink && submenu) {
        navLink.addEventListener('click', (e) => {
            // Prevenir navegação se clicar no link principal
            if (e.target.closest('.nav-link') && !e.target.closest('.submenu-link')) {
                e.preventDefault();
            }
            
            // Toggle do submenu
            const wasOpen = item.classList.contains('open');
            
            // Fechar todos os outros submenus
            navItemsWithSubmenu.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('open');
                }
            });
            
            // Toggle do submenu atual
            item.classList.toggle('open', !wasOpen);
            
            console.log('Submenu toggled:', item.classList.contains('open'));
        });
    }
});

console.log('✓ Submenus da sidebar configurados');

// ============================================================================
// SINCRONIZAÇÃO DE NAVEGAÇÃO COM SLIDES
// ============================================================================
const allNavLinks = document.querySelectorAll('.nav-link, .submenu-link');

/**
 * Função para atualizar link ativo na sidebar
 * @param {string} slideId - ID do slide atual
 */
function updateActiveNavLink(slideId) {
    if (!slideId) return;
    
    // Remover classe active de todos os links
    allNavLinks.forEach(link => link.classList.remove('active'));
    
    // Encontrar e ativar o link correspondente
    const activeLink = document.querySelector(`a[href="#/${slideId}"]`);
    
    if (activeLink) {
        activeLink.classList.add('active');
        
        // Se for um submenu-link, abrir o submenu pai
        const parentSubmenu = activeLink.closest('.nav-item-with-submenu');
        if (parentSubmenu) {
            parentSubmenu.classList.add('open');
        }
        
        // Scroll suave até o link ativo na sidebar (apenas se sidebar estiver visível)
        if (!sidebar.classList.contains('hidden')) {
            setTimeout(() => {
                activeLink.scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest',
                    inline: 'nearest'
                });
            }, 100);
        }
        
        console.log('Link ativo atualizado:', slideId);
    }
}

/**
 * Obtém o ID do slide atual
 * @param {HTMLElement} slide - Elemento do slide
 * @returns {string} ID do slide
 */
function getSlideId(slide) {
    return slide.id || 
           slide.getAttribute('data-id') || 
           slide.getAttribute('data-slide-id') ||
           `slide-${Array.from(slide.parentNode.children).indexOf(slide)}`;
}

// Sincronizar ao mudar de slide
Reveal.on('slidechanged', event => {
    const currentSlide = event.currentSlide;
    const slideId = getSlideId(currentSlide);
    
    updateActiveNavLink(slideId);
    
    // Fechar dropdown de apresentações se estiver aberto
    if (dropdownMenu && dropdownMenu.classList.contains('show')) {
        dropdownMenu.classList.remove('show');
    }
});

// Sincronizar ao carregar a página
Reveal.on('ready', event => {
    const currentSlide = event.currentSlide;
    const slideId = getSlideId(currentSlide);
    
    updateActiveNavLink(slideId);
    
    // Inicializar estado do botão de toggle
    updateToggleButtonState(!sidebar.classList.contains('hidden'));
});

console.log('✓ Sincronização de navegação configurada');

// ============================================================================
// ATALHOS DE TECLADO PERSONALIZADOS
// ============================================================================
document.addEventListener('keydown', (e) => {
    // Toggle sidebar com 'S' ou 's'
    if ((e.key === 's' || e.key === 'S') && !e.ctrlKey && !e.metaKey && !e.altKey) {
        // Verificar se não está em um input ou textarea
        if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
            e.preventDefault();
            toggleSidebar();
        }
    }
    
    // Fechar dropdown com ESC
    if (e.key === 'Escape') {
        if (dropdownMenu && dropdownMenu.classList.contains('show')) {
            e.preventDefault();
            dropdownMenu.classList.remove('show');
        }
    }
    
    // Navegação rápida entre slides com números (1-9)
    if (e.key >= '1' && e.key <= '9' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const slideNumber = parseInt(e.key) - 1;
        const totalSlides = Reveal.getTotalSlides();
        
        if (slideNumber < totalSlides) {
            e.preventDefault();
            Reveal.slide(slideNumber);
        }
    }
});

console.log('✓ Atalhos de teclado configurados');

// ============================================================================
// RESPONSIVE: AUTO-HIDE SIDEBAR EM MOBILE
// ============================================================================
/**
 * Gerencia o comportamento responsivo da sidebar
 */
function handleResponsiveSidebar() {
    if (window.innerWidth <= 768) {
        // Em mobile, garantir que sidebar esteja fechada por padrão
        if (sidebar && revealContainer) {
            sidebar.classList.add('hidden');
            revealContainer.classList.add('full-width');
        }
    } else {
        // Em desktop, garantir que sidebar esteja visível por padrão
        if (sidebar && revealContainer) {
            sidebar.classList.remove('hidden');
            revealContainer.classList.remove('full-width');
        }
    }
    
    // Atualizar layout do Reveal.js
    setTimeout(() => {
        Reveal.layout();
    }, 100);
}

// Executar ao carregar
document.addEventListener('DOMContentLoaded', () => {
    handleResponsiveSidebar();
});

// Executar ao redimensionar com debounce
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        handleResponsiveSidebar();
    }, 250);
});

console.log('✓ Responsividade configurada');

// ============================================================================
// CLICK EM LINKS DE NAVEGAÇÃO
// ============================================================================
allNavLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        // Se for um link com submenu, já foi tratado acima
        if (this.classList.contains('nav-link') && this.closest('.nav-item-with-submenu')) {
            // Não fazer nada, o evento de submenu já trata
            return;
        }
        
        // Para links de submenu ou links simples, marcar como ativo
        allNavLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        // Em mobile, fechar sidebar após clicar
        if (window.innerWidth <= 768) {
            setTimeout(() => {
                if (sidebar && revealContainer) {
                    sidebar.classList.add('hidden');
                    revealContainer.classList.add('full-width');
                    updateToggleButtonState(false);
                }
            }, 300);
        }
    });
});

// ============================================================================
// GESTÃO DE ESTADO DA APLICAÇÃO
// ============================================================================
const AppState = {
    // Estado atual da aplicação
    currentState: {
        sidebarVisible: true,
        currentPresentation: null,
        currentSlide: 0
    },
    
    // Salvar estado no localStorage
    saveState() {
        try {
            localStorage.setItem('presentationAppState', JSON.stringify(this.currentState));
        } catch (e) {
            console.warn('Não foi possível salvar o estado:', e);
        }
    },
    
    // Carregar estado do localStorage
    loadState() {
        try {
            const saved = localStorage.getItem('presentationAppState');
            if (saved) {
                this.currentState = { ...this.currentState, ...JSON.parse(saved) };
                return true;
            }
        } catch (e) {
            console.warn('Não foi possível carregar o estado:', e);
        }
        return false;
    },
    
    // Atualizar estado da sidebar
    updateSidebarState(isVisible) {
        this.currentState.sidebarVisible = isVisible;
        this.saveState();
    }
};

// Carregar estado salvo ao inicializar
document.addEventListener('DOMContentLoaded', () => {
    if (AppState.loadState()) {
        // Aplicar estado salvo da sidebar
        if (sidebar && revealContainer) {
            if (!AppState.currentState.sidebarVisible) {
                sidebar.classList.add('hidden');
                revealContainer.classList.add('full-width');
            }
            updateToggleButtonState(AppState.currentState.sidebarVisible);
        }
    }
});

// Atualizar estado quando a sidebar for alternada
if (sidebar) {
    sidebar.addEventListener('transitionend', () => {
        const isVisible = !sidebar.classList.contains('hidden');
        AppState.updateSidebarState(isVisible);
    });
}

// ============================================================================
// OTIMIZAÇÕES DE PERFORMANCE
// ============================================================================
/**
 * Debounce function para otimizar eventos frequentes
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Aplicar debounce em eventos de resize
window.addEventListener('resize', debounce(() => {
    Reveal.layout();
}, 100));

// ============================================================================
// TRATAMENTO DE ERROS
// ============================================================================
window.addEventListener('error', (e) => {
    console.error('Erro na aplicação:', e.error);
});

// Capturar erros não tratados em Promises
window.addEventListener('unhandledrejection', (e) => {
    console.error('Promise rejeitada não tratada:', e.reason);
});

// ============================================================================
// CONSOLE LOG FINAL
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        console.log('\n' + '='.repeat(60));
        console.log('🎉 SISTEMA DE APRESENTAÇÕES CARREGADO COM SUCESSO');
        console.log('='.repeat(60));
        console.log('📌 Atalhos Disponíveis:');
        console.log('   • Pressione "S" para toggle da sidebar');
        console.log('   • Use setas ← → para navegar entre slides');
        console.log('   • Pressione "ESC" para visão geral/fechar dropdowns');
        console.log('   • Pressione "F" para fullscreen');
        console.log('   • Teclas 1-9 para navegação rápida entre slides');
        console.log('='.repeat(60));
        console.log('📊 Estado Inicial:');
        console.log('   • Sidebar:', !sidebar.classList.contains('hidden') ? 'VISÍVEL' : 'OCULTA');
        console.log('   • Slides totais:', Reveal.getTotalSlides());
        console.log('   • Slide atual:', Reveal.getIndices().h + 1);
        console.log('='.repeat(60) + '\n');
    }, 1000);
});

// ============================================================================
// EXPORTAÇÕES PARA DEBUG (apenas em desenvolvimento)
// ============================================================================
if (typeof window !== 'undefined') {
    window.PresentationApp = {
        toggleSidebar,
        updateActiveNavLink,
        getSlideId,
        handleResponsiveSidebar,
        AppState
    };
    
    console.log('🔧 Funções de debug disponíveis em window.PresentationApp');
}
