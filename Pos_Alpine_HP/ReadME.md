# Script de Pós-Instalação para Alpine Linux no HP Compaq 6005 Pro SFF

Versão 18-12-2025 Revisão 4 19-12-2025

## Motivo e observação

Necessidade de configurar um desktop com GUI no Alpine Linux, e **ainda está em testes(pode haver erros)**.

### Melhorias
- ```v4-19-12-2025```: Roda até o final, mas leia o próximo tópico por favor
  
### Bugs a serem corrigidos
 - ```v4-19-12-2025```: Carrega interface gráfica, porém não exibe corretamente e não permite manuseio

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## Sobre

Este script automatiza a configuração de um ambiente de desktop completo (KDE Plasma) no **Alpine Linux (ISO: v3.22 Extended)**, especificamente otimizado para o hardware do **HP Compaq 6005 Pro SFF**. Ele instala drivers essenciais, o ambiente gráfico, software básico e aplica otimizações de sistema.

---
## Versão do Alpine Linux

Alpine Linux 3.23 - ISO Extended(release de 19-12-2025 do SO)
<br>[Autores: (Alpine Linux Developers Team)](https://wiki.alpinelinux.org/wiki/Alpine_Linux:Developers)
<br>[About do SO](https://www.alpinelinux.org/about/)
<br>[Link para download](https://www.alpinelinux.org/downloads/)
<br>[Documentação SO](https://wiki.alpinelinux.org/wiki/Main_Page)

## Compatibilidade

| Componente | Especificação | Observações |
| :--- | :--- | :--- |
| **Hardware** | HP Compaq 6005 Pro SFF | Otimizado para este modelo. |
| **Processador** | AMD Athlon II / Phenom II (ou similar) | |
| **Gráficos** | AMD Radeon HD 4200 / 7660D (Integrado) | Instala drivers `radeon` e configurações X11 para melhor desempenho e correção de *tearing*. |
| **Áudio** | Realtek ALC261 (ou similar) | Configura ALSA e PulseAudio. |
| **Rede** | Broadcom BCM5761 (ou similar) | Instala firmware e drivers Broadcom. |
| **Sistema Operacional** | Alpine Linux (Instalação Base) | Deve ser executado após a instalação inicial do Alpine. |

## Pré-requisitos

1.  **Alpine Linux** instalado (instalação base via `setup-alpine`).
2.  Acesso **root** (o script deve ser executado como `root`).
3.  Conexão com a internet ativa.

## Uso

1.  **Baixe o script:**
    ```bash
    wget <URL_DO_SCRIPT>/runAlpine.sh
    ```
    *(Se você já o tem, pule esta etapa)*

2.  **Dê permissão de execução:**
    ```bash
    chmod +x runAlpine.sh
    ```

3.  **Execute o script como root:**
    ```bash
    ./runAlpine.sh
    ```

O script fará perguntas interativas sobre a instalação de pacotes KDE completos, configuração de `locale` e criação de um novo usuário.

## Funcionalidades Principais

O script realiza as seguintes ações:

### 1. Configuração do Sistema
*   Atualiza os repositórios e adiciona o repositório `community`.
*   Instala o kernel Linux e firmwares essenciais.
*   Habilita serviços críticos: `dbus`, `udev`, `NetworkManager`, `sddm`, `alsa`, `acpid` (e opcionalmente `cupsd`).
*   Configura o `sudo` para o grupo `wheel`.
*   Aplica otimizações de desempenho (`vm.swappiness=10`, `vm.vfs_cache_pressure=50`).
*   Configurações regionais opcionais: `pt_BR.UTF-8`, fuso horário `America/Sao_Paulo`.

### 2. Ambiente Gráfico e Drivers
*   Instala o servidor X11 (`xorg-server`) e utilitários básicos.
*   Instala o ambiente de desktop **KDE Plasma** (`plasma-desktop`).
*   Instala o gerenciador de display **SDDM**.
*   Instala drivers gráficos **Radeon** (`xf86-video-ati`, `mesa-dri-gallium`) e cria um arquivo de configuração X11 (`/etc/X11/xorg.conf.d/10-radeon.conf`) com otimizações como `TearFree`.

### 3. Software Essencial
*   **Navegador:** `firefox`
*   **Suíte Office:** `libreoffice` (com localização em português)
*   **Multimídia:** `vlc`, `ffmpeg`, codecs de mídia.
*   **Utilitários:** `sudo`, `bash`, `nano`, `htop`, `curl`, `wget`, `git`.
*   **KDE Apps:** `dolphin`, `konsole`, `kate`, `partitionmanager`, etc.

### 4. Configuração de Usuário
*   Opcionalmente, cria um novo usuário e o adiciona aos grupos necessários (`wheel`, `audio`, `video`, `pulse`, etc.) para garantir o funcionamento correto do áudio e do ambiente gráfico.

## Próximos Passos

Após a conclusão do script, o sistema estará pronto para ser reiniciado.

1.  **Reinicie o sistema** (o script perguntará se deseja reiniciar automaticamente).
    ```bash
    reboot
    ```
2.  Ao iniciar, você será recebido pelo gerenciador de display **SDDM**.
3.  Faça login com o usuário criado.
4.  **Configure a rede** usando o ícone do NetworkManager na bandeja do sistema ou via terminal com `nmtui`.
5.  **Teste o áudio** usando o `pavucontrol` (Controle de Volume do PulseAudio).
6.  Mantenha o sistema atualizado:
    ```bash
    sudo apk update && sudo apk upgrade
    ```



