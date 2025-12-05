# Sistema de Gestão de Confeitaria (Sodiê PUC)

Este projeto é um sistema de gestão de desktop desenvolvido em Python com a biblioteca PyQt6, focado em auxiliar na administração de uma confeitaria ou negócio de alimentos, como a Sodiê PUC. O sistema oferece funcionalidades para gerenciamento de usuários, produtos (incluindo informações nutricionais e geração de código de barras), clientes, lotes de produção e pedidos.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## 🌟 Funcionalidades Principais

*   **Gerenciamento de Usuários:** Controle de acesso com diferentes níveis (Administrador, Gerente, Técnico e Comum).
*   **Cadastro de Produtos:** Registro detalhado de produtos, incluindo porções, códigos de barras (EAN-13) e tabelas nutricionais.
*   **Gestão de Estoque e Lotes:** Acompanhamento de lotes de produção e suas respectivas datas de fabricação e validade.
*   **Controle de Clientes e Pedidos:** Cadastro de clientes e gerenciamento de pedidos.
*   **Interface Gráfica Moderna:** Interface de usuário intuitiva e responsiva desenvolvida com PyQt6.

## 🛠️ Tecnologias Utilizadas

*   Python 3.x
*   PyQt6
*   Biblioteca `barcode`
*   Manipulação de dados em formato JSON

## 🚀 Instalação

Para rodar este projeto localmente, você precisará ter o Python 3 instalado.

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_PROJETO>
    ```
    *(Nota: Substitua `<URL_DO_REPOSITORIO>` e `<NOME_DO_PROJETO>` pelos valores reais do seu projeto.)*

2.  **Instale as dependências:**
    ```bash
    pip install PyQt6 python-barcode
    ```

## 💻 Uso

Para iniciar a aplicação, execute o arquivo principal:

```bash
python app.py
```

As credenciais de usuário padrão para teste são:

| Nível de Acesso | Usuário | Senha |
| :--- | :--- | :--- |
| Administrador | Admin | Admin |
| Técnico | Tecnico | Tecnico |
| Gerente | Gerencia | Gerencia |
| Comum | Funcionário | Funcionario |

---


