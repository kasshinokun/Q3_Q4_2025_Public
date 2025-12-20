# Script de Correção para Problemas no startx/XFCE no Alpine Linux
#
# Este script deve ser executado como root.

USER_NAME="<Nome_do_Usuario>"
HOME_DIR="/home/$USER_NAME"

echo "Iniciando script de correção para o usuário: $USER_NAME"

# 1. Adicionar o usuário aos grupos necessários
echo "1. Adicionando o usuário '$USER_NAME' aos grupos: wheel, audio, video, input..."
# Verifica se o grupo 'wheel' existe e adiciona o usuário. Instala o sudo se não estiver presente.
if ! grep -q "^wheel:" /etc/group; then
    echo "Grupo 'wheel' não encontrado. Instalando 'sudo' e criando o grupo."
    apk add sudo
fi
adduser "$USER_NAME" wheel
adduser "$USER_NAME" audio
adduser "$USER_NAME" video
adduser "$USER_NAME" input

# 2. Configurar e iniciar os serviços dbus e elogind
echo "2. Configurando e iniciando os serviços dbus e elogind..."

# Instalação dos pacotes (caso não estejam instalados, embora o usuário tenha confirmado a instalação)
apk update
apk add dbus elogind

# Ativar serviços para iniciar no boot (se já estiverem ativados, o comando apenas confirma)
rc-update add dbus default
rc-update add elogind default

# Iniciar serviços imediatamente (se já estiverem rodando, o comando apenas confirma)
rc-service dbus start
rc-service elogind start

# 3. Criar ou sobrescrever o arquivo .xinitrc para o usuário
echo "3. Criando/sobrescrevendo o arquivo .xinitrc em $HOME_DIR/..."

# Verifica se o diretório home existe
if [ ! -d "$HOME_DIR" ]; then
    echo "ERRO: O diretório home '$HOME_DIR' não existe. Abortando."
    exit 1
fi

# Cria o arquivo .xinitrc com o comando correto para iniciar o XFCE
echo "#!/bin/sh" > "$HOME_DIR/.xinitrc"
echo "" >> "$HOME_DIR/.xinitrc"
echo "# Inicia o XFCE" >> "$HOME_DIR/.xinitrc"
echo "exec startxfce4" >> "$HOME_DIR/.xinitrc"

# Garante que o usuário seja o dono do arquivo
chown "$USER_NAME":"$USER_NAME" "$HOME_DIR/.xinitrc"
chmod +x "$HOME_DIR/.xinitrc"

echo "Configuração concluída."
echo "Próxima etapa: Mude para o usuário '$USER_NAME' e tente iniciar o XFCE:"
echo "  su - $USER_NAME"
echo "  startx"
