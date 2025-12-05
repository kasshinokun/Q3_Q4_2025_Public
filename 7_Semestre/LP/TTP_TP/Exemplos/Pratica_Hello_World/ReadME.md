<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
# <i class="fa-brands fa-python" style="height:1.3em; width:1.3em;color:white; background-image: linear-gradient(to top right, blue, yellow);"></i> Pratica_Hello_World.py

Este projeto contém um exemplo prático de funções e procedimentos em Python, demonstrando diferentes formas de implementar uma saudação personalizada ao usuário.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## 📁 Estrutura do Código

O arquivo `Pratica_Hello_World.py` contém:

- Uma variável global `aluno`
- Funções e procedimentos para exibir mensagens de boas-vindas
- Um bloco principal (`if __name__ == '__main__'`) que orquestra a execução

## 🧠 Funções Implementadas

### 1. `Hello_World(nome: str) -> str`
- **Tipo:** Função (com tipagem explícita)
- **Descrição:** Recebe um nome e retorna uma string formatada.
- **Uso global:** Atualiza a variável `aluno` antes de retornar.

### 2. `pratica()`
- **Tipo:** Procedimento
- **Descrição:** Contém três subfunções internas que demonstram diferentes estilos de implementação:
  - `Hello_World()`: Versão local com tipagem.
  - `Hello_World2()`: Versão local sem tipagem.
  - `Hello_World3()`: Versão que usa `print()` em vez de retornar (procedimento interno).

## ▶️ Como Executar

Execute o arquivo diretamente no terminal:

## ▶️ Saída Execução

```bash
python Pratica_Hello_World.py
```

```bash
Procedimento pratica
Função 1 pratica
Por favor digite o seu nome:------:> Maria
Olá Maria, Bem-vindo ao Python
Função 2 pratica
Por favor digite o seu nome:------:> João
Olá João, Bem-vindo ao Python
Procedimento pratica
Por favor digite o seu nome:------:> Ana
Olá Ana, Bem-vindo ao Python
Fora do Procedimento pratica
Função
Por favor digite o seu nome:------:> Pedro
Olá Pedro, Bem-vindo ao Python
Muito, Obrigado, 
```