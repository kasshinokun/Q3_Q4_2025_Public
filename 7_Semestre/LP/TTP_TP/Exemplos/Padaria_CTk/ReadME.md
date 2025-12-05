## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

# Sistema Padaria - Monolítico

## Visão Geral

O **Sistema Padaria - Monolítico** é uma aplicação de gerenciamento de padaria simples, desenvolvida em Python utilizando a biblioteca **CustomTkinter (ctk)** para a interface gráfica (GUI). O sistema permite o cadastro de produtos, o registro de vendas com controle de estoque e a geração de um relatório básico de análise de vendas.

## Funcionalidades

O sistema é dividido em três abas principais:

1.  **Produtos:**
    *   Cadastro de novos produtos (Nome, Preço e Estoque).
    *   Visualização da lista de produtos cadastrados com seus respectivos IDs, preços e estoque atual.
2.  **Vendas:**
    *   Registro de vendas de produtos.
    *   Seleção do produto através de um *dropdown* (apenas produtos com estoque > 0 são listados).
    *   Validação de estoque: a venda só é registrada se houver quantidade suficiente em estoque.
    *   Atualização automática do estoque após a venda.
3.  **Análise:**
    *   Geração de um relatório detalhado de todas as vendas registradas.
    *   Cálculo e exibição do **Total Geral** de vendas.

## Requisitos

Para executar esta aplicação, você precisa ter o Python instalado em seu sistema.

### Dependências

A única dependência externa é a biblioteca `customtkinter`.

Você pode instalá-la usando o `pip`:

```bash
pip install customtkinter
```

## Como Executar

1.  **Salve o código:** Certifique-se de que o arquivo `padaria_ctk.py` esteja salvo em seu computador.
2.  **Instale as dependências** (se ainda não o fez):
    ```bash
    pip install customtkinter
    ```
3.  **Execute o script Python:**
    ```bash
    python padaria_ctk.py
    ```

A janela principal da aplicação será aberta, e você poderá começar a utilizar o sistema.

## Estrutura do Código

O código é implementado em uma única classe, `PadariaApp`, que gerencia o estado da aplicação (produtos e vendas) e a interface gráfica.

| Atributo | Descrição |
| :--- | :--- |
| `self.produtos` | Dicionário para armazenar os produtos cadastrados. |
| `self.vendas` | Lista para armazenar os registros de vendas. |
| `self.current_id` | Contador para gerar IDs únicos para os produtos. |
| `self.root` | Janela principal do CustomTkinter. |

### Métodos Principais

| Método | Descrição |
| :--- | :--- |
| `cadastrar_produto()` | Adiciona um novo produto ao `self.produtos` e atualiza a lista de produtos e o *dropdown* de vendas. |
| `registrar_venda()` | Processa uma venda, verifica o estoque, atualiza o `self.vendas` e o estoque do produto. |
| `gerar_relatorio()` | Calcula e exibe o relatório de vendas na aba "Análise". |
| `atualizar_lista_produtos()` | Atualiza o `CTkTextbox` na aba "Produtos" com a lista atualizada de produtos. |
| `atualizar_combo_produtos()` | Atualiza o `CTkComboBox` na aba "Vendas" com os produtos disponíveis para venda. |
| `mostrar_erro(mensagem)` | Exibe uma janela de erro (`CTkToplevel`) com a mensagem fornecida. |



