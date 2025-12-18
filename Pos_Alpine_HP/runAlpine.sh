#!/bin/sh
# install-alpine-kde-hp6005.sh
# Script de pós-instalação para Alpine Linux com KDE no HP Compaq 6005 Pro SFF
# Execute como root após a instalação básica do Alpine

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Função para confirmar ações
confirm() {
    while true; do
        read -p "$1 (S/n): " resposta
        case "$resposta" in
            [Ss]*|[Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            *) echo "Por favor, responda S/s ou N/n" ;;
        esac
    done
}

# Verificar se é root
if [ "$(id -u)" -ne 0 ]; then
    log_error "Este script precisa ser executado como root!"
    exit 1
fi

# Verificar se está no Alpine
if [ ! -f /etc/alpine-release ]; then
    log_error "Este script é específico para Alpine Linux!"
    exit 1
fi

# Banner informativo
echo "========================================="
echo "  Instalação Alpine Linux + KDE Plasma"
echo "  HP Compaq 6005 Pro SFF"
echo "========================================="

# Atualizar repositórios
log_info "Atualizando repositórios..."
apk update

# Adicionar repositório community se não existir
if ! grep -q "^http.*/community$" /etc/apk/repositories; then
    log_info "Adicionando repositório community..."
    echo "http://dl-cdn.alpinelinux.org/alpine/v$(cut -d'.' -f1,2 /etc/alpine-release)/community" >> /etc/apk/repositories
    apk update
fi

# CORREÇÃO: Linha 73 - faltou 'add' antes de firefox
log_info "Instalando aplicativos essenciais..."
apk add dolphin konsole kate kcalc ksystemlog partitionmanager
apk add firefox libreoffice libreoffice-l10n-pt-br  # CORRIGIDO

# Instalar kernel e firmwares (corrigir ordem - antes de X11)
log_info "Instalando kernel Linux e firmwares..."
apk add linux-firmware linux-firmware-other linux-firmware-radeon

# Instalar X11 e utilitários básicos primeiro
log_info "Instalando X11 e utilitários básicos..."
apk add xorg-server xrandr xset xinit xauth
apk add sudo bash bash-completion nano htop curl wget git

# Instalar drivers e bibliotecas gráficas (otimizado para Radeon)
log_info "Instalando drivers gráficos Radeon..."
apk add mesa-dri-gallium mesa-va-gallium mesa-vdpau-gallium mesa-egl
apk add mesa-va-radeon mesa-vdpau-radeon  # Específico para Radeon
apk add xf86-video-ati xf86-video-vesa xf86-video-fbdev
apk add libdrm

# Instalar áudio - Realtek ALC261/Similar
log_info "Instalando drivers de áudio..."
apk add alsa-utils alsa-ucm-conf alsa-tools alsa-tools-doc
apk add pulseaudio pulseaudio-alsa pulseaudio-bluetooth
apk add pavucontrol

# Instalar rede - Broadcom BCM5761
log_info "Instalando drivers de rede..."
apk add bcom-firmware broadcom-net
apk add networkmanager networkmanager-wifi networkmanager-tui
apk add wireless-tools wpa_supplicant  # Para Wi-Fi se necessário

# Instalar KDE Plasma (otimizado - menos pacotes desnecessários)
log_info "Instalando KDE Plasma..."
apk add plasma-desktop plasma-desktop-doc
apk add plasma-nm plasma-pa  # Integração NetworkManager e PulseAudio
apk add sddm sddm-breeze
apk add kdegraphics-thumbnailers kde-cli-tools
apk add breeze-icons oxygen-icons

# Pacotes KDE opcionais (reduzir tempo de instalação)
if confirm "Instalar pacotes KDE completos (recomendado para desktop completo)?"; then
    log_info "Instalando pacotes KDE completos..."
    apk add kde-applications
else
    log_info "Instalando apenas aplicativos essenciais KDE..."
    apk add dolphin konsole kate kcalc ksystemlog partitionmanager
    apk add ark filelight kate kgpg knotes konqueror
fi

# Instalar codecs de mídia
log_info "Instalando codecs de mídia..."
apk add vlc vlc-lang
apk add gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly
apk add ffmpeg ffmpeg-libs

# Configurar serviços
log_info "Configurando serviços..."
rc-update add dbus default
rc-update add udev sysinit
rc-update add udev-trigger sysinit
rc-update add NetworkManager default
rc-update add sddm default
rc-update add acpid default
rc-update add alsa default
rc-update add cupsd default  # Só se tiver impressora

# Configurar áudio - MELHORIA: detectar usuário atual
log_info "Configurando áudio..."
CURRENT_USER=$(who am i | awk '{print $1}')
if [ -z "$CURRENT_USER" ] || [ "$CURRENT_USER" = "root" ]; then
    log_warn "Usuário não detectado. Configure manualmente depois."
else
    addgroup "$CURRENT_USER" audio
    addgroup "$CURRENT_USER" pulse
    addgroup "$CURRENT_USER" pulse-access
    addgroup "$CURRENT_USER" video
fi

# Configuração de áudio para Realtek
cat > /etc/asound.conf << 'EOF'
defaults.pcm.card 0
defaults.ctl.card 0

pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "hw:0,0"
    }
    capture.pcm {
        type plug
        slave.pcm "hw:0,0"
    }
}
EOF

# Configuração específica para Radeon HD 4200/7660D (melhorada)
log_info "Criando configuração X11 para Radeon..."
mkdir -p /etc/X11/xorg.conf.d

cat > /etc/X11/xorg.conf.d/10-radeon.conf << 'EOF'
Section "Device"
    Identifier  "Radeon"
    Driver      "radeon"
    Option      "AccelMethod" "glamor"
    Option      "DRI" "3"
    Option      "TearFree" "on"
    Option      "ColorTiling" "on"
    Option      "ColorTiling2D" "on"
    Option      "EnablePageFlip" "on"
EndSection

Section "Module"
    Load "dri3"
    Load "glamoregl"
EndSection

Section "Extensions"
    Option "Composite" "Enable"
EndSection
EOF

# Configuração para evitar tela preta no KDE com Radeon antigo
cat > /etc/X11/xorg.conf.d/15-kde-compat.conf << 'EOF'
Section "Screen"
    Identifier "Screen0"
    SubSection "Display"
        Depth 24
        Modes "1024x768" "800x600" "640x480"
    EndSubSection
EndSection
EOF

# Configurações de desempenho
log_info "Otimizando configurações do sistema..."
echo "vm.swappiness=10" >> /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf

# Configurar sudo
log_info "Configurando sudo..."
echo "%wheel ALL=(ALL) ALL" > /etc/sudoers.d/wheel
echo "Defaults timestamp_timeout=30" >> /etc/sudoers.d/wheel
chmod 440 /etc/sudoers.d/wheel

# Configurações regionais
if confirm "Configurar locale para pt_BR?"; then
    log_info "Configurando locale para pt_BR..."
    apk add locale lang
    echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen
    locale-gen
    setup-locale LANG=pt_BR.UTF-8
fi

log_info "Configurando teclado..."
setup-keymap us us

log_info "Configurando fuso horário..."
setup-timezone America/Sao_Paulo

log_info "Configurando hostname..."
setup-hostname alpine-hp6005

# Criar usuário
if confirm "Criar um novo usuário agora?"; then
    log_warn "Digite o nome do usuário: "
    read -r username
    
    if [ -n "$username" ] && [ "$username" != "root" ]; then
        log_info "Criando usuário $username..."
        adduser -g "$username" "$username"
        
        # Adicionar aos grupos
        for grupo in wheel audio video pulse pulse-access netdev input; do
            addgroup "$username" "$grupo" 2>/dev/null || true
        done
        
        # Configurar senha
        passwd "$username"
        
        log_info "Usuário $username criado com sucesso!"
    else
        log_error "Nome de usuário inválido!"
    fi
fi

# Limpar cache
log_info "Limpando cache..."
apk cache clean

# Resumo final
log_info "========================================="
log_info "INSTALAÇÃO CONCLUÍDA!"
log_info "========================================="
log_info "Configurações aplicadas:"
log_info "  - KDE Plasma Desktop"
log_info "  - Drivers Radeon HD 4200/7660D"
log_info "  - Áudio Realtek ALC261"
log_info "  - Rede Broadcom BCM5761"
log_info "  - NetworkManager com interface gráfica"
log_info ""
log_info "Próximos passos após reiniciar:"
log_info "1. Login no SDDM (gerenciador de display)"
log_info "2. Configurar rede: nmtui ou ícone do sistema"
log_info "3. Testar áudio: pavucontrol"
log_info "4. Atualizar sistema: sudo apk update && sudo apk upgrade"
log_info ""

if confirm "Reiniciar o sistema agora?"; then
    log_info "Reiniciando em 10 segundos..."
    sleep 10
    reboot
else
    log_warn "Reinicie manualmente quando pronto:"
    log_warn "  reboot"
    log_warn ""
    log_warn "Para iniciar o KDE manualmente:"
    log_warn "  rc-service sddm start"
fi