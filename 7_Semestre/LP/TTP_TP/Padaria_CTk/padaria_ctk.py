import customtkinter as ctk
from datetime import datetime

class PadariaApp:
    def __init__(self):
        self.produtos = {}
        self.vendas = []
        self.current_id = 1
        
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Sistema Padaria - Monolítico")
        self.root.geometry("800x600")
        
        # Criar abas para diferentes funcionalidades
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Abas do sistema
        self.tab_produtos = self.tabview.add("Produtos")
        self.tab_vendas = self.tabview.add("Vendas")
        self.tab_analise = self.tabview.add("Análise")
        
        self.criar_aba_produtos()
        self.criar_aba_vendas()
        self.criar_aba_analise()
        
    def criar_aba_produtos(self):
        # Frame de cadastro
        frame_cadastro = ctk.CTkFrame(self.tab_produtos)
        frame_cadastro.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(frame_cadastro, text="Cadastro de Produtos", font=("Arial", 16)).pack(pady=10)
        
        # Formulário de cadastro
        form_frame = ctk.CTkFrame(frame_cadastro)
        form_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = ctk.CTkEntry(form_frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_preco = ctk.CTkEntry(form_frame)
        self.entry_preco.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Estoque:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_estoque = ctk.CTkEntry(form_frame)
        self.entry_estoque.grid(row=2, column=1, padx=5, pady=5)
        
        btn_cadastrar = ctk.CTkButton(form_frame, text="Cadastrar Produto", command=self.cadastrar_produto)
        btn_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Lista de produtos
        self.lista_produtos = ctk.CTkTextbox(self.tab_produtos, height=300)
        self.lista_produtos.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.atualizar_lista_produtos()
        
    def criar_aba_vendas(self):
        # Frame de venda
        frame_venda = ctk.CTkFrame(self.tab_vendas)
        frame_venda.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(frame_venda, text="Registro de Vendas", font=("Arial", 16)).pack(pady=10)
        
        # Seleção de produto
        selecao_frame = ctk.CTkFrame(frame_venda)
        selecao_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(selecao_frame, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_produtos = ctk.CTkComboBox(selecao_frame, values=[])
        self.combo_produtos.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(selecao_frame, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantidade = ctk.CTkEntry(selecao_frame)
        self.entry_quantidade.grid(row=1, column=1, padx=5, pady=5)
        
        btn_vender = ctk.CTkButton(selecao_frame, text="Registrar Venda", command=self.registrar_venda)
        btn_vender.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Lista de vendas
        self.lista_vendas = ctk.CTkTextbox(self.tab_vendas, height=300)
        self.lista_vendas.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.atualizar_combo_produtos()
        
    def criar_aba_analise(self):
        # Frame de análise
        frame_analise = ctk.CTkFrame(self.tab_analise)
        frame_analise.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(frame_analise, text="Análise de Vendas", font=("Arial", 16)).pack(pady=10)
        
        # Botão para gerar relatório
        btn_relatorio = ctk.CTkButton(frame_analise, text="Gerar Relatório", command=self.gerar_relatorio)
        btn_relatorio.pack(pady=10)
        
        # Área de relatório
        self.relatorio = ctk.CTkTextbox(frame_analise)
        self.relatorio.pack(padx=10, pady=10, fill="both", expand=True)
        
    def cadastrar_produto(self):
        nome = self.entry_nome.get()
        try:
            preco = float(self.entry_preco.get())
            estoque = int(self.entry_estoque.get())
        except ValueError:
            self.mostrar_erro("Valores inválidos para preço ou estoque!")
            return
            
        produto_id = self.current_id
        self.produtos[produto_id] = {
            'nome': nome,
            'preco': preco,
            'estoque': estoque
        }
        self.current_id += 1
        
        self.entry_nome.delete(0, 'end')
        self.entry_preco.delete(0, 'end')
        self.entry_estoque.delete(0, 'end')
        
        self.atualizar_lista_produtos()
        self.atualizar_combo_produtos()
        
    def registrar_venda(self):
        produto_id = int(self.combo_produtos.get().split(":")[0])
        quantidade = int(self.entry_quantidade.get())
        
        if produto_id in self.produtos:
            produto = self.produtos[produto_id]
            if produto['estoque'] >= quantidade:
                # Atualizar estoque
                produto['estoque'] -= quantidade
                
                # Registrar venda
                venda = {
                    'produto_id': produto_id,
                    'produto_nome': produto['nome'],
                    'quantidade': quantidade,
                    'preco_unitario': produto['preco'],
                    'total': produto['preco'] * quantidade,
                    'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                self.vendas.append(venda)
                
                self.entry_quantidade.delete(0, 'end')
                self.atualizar_lista_produtos()
                self.atualizar_combo_produtos()
            else:
                self.mostrar_erro("Estoque insuficiente!")
        else:
            self.mostrar_erro("Produto não encontrado!")
            
    def gerar_relatorio(self):
        self.relatorio.delete("1.0", "end")
        
        if not self.vendas:
            self.relatorio.insert("end", "Nenhuma venda registrada.\n")
            return
            
        total_geral = 0
        relatorio_texto = "=== RELATÓRIO DE VENDAS ===\n\n"
        
        for venda in self.vendas:
            relatorio_texto += f"Data: {venda['data']}\n"
            relatorio_texto += f"Produto: {venda['produto_nome']}\n"
            relatorio_texto += f"Quantidade: {venda['quantidade']}\n"
            relatorio_texto += f"Total: R$ {venda['total']:.2f}\n"
            relatorio_texto += "-" * 30 + "\n"
            total_geral += venda['total']
            
        relatorio_texto += f"\nTOTAL GERAL: R$ {total_geral:.2f}"
        
        self.relatorio.insert("end", relatorio_texto)
        
    def atualizar_lista_produtos(self):
        self.lista_produtos.delete("1.0", "end")
        if not self.produtos:
            self.lista_produtos.insert("end", "Nenhum produto cadastrado.\n")
            return
            
        for pid, produto in self.produtos.items():
            self.lista_produtos.insert("end", 
                f"ID: {pid} | Nome: {produto['nome']} | "
                f"Preço: R$ {produto['preco']:.2f} | "
                f"Estoque: {produto['estoque']}\n"
            )
            
    def atualizar_combo_produtos(self):
        valores = []
        for pid, produto in self.produtos.items():
            if produto['estoque'] > 0:
                valores.append(f"{pid}: {produto['nome']} (R$ {produto['preco']:.2f})")
        self.combo_produtos.configure(values=valores)
        if valores:
            self.combo_produtos.set(valores[0])
            
    def mostrar_erro(self, mensagem):
        # Janela simples de erro
        erro = ctk.CTkToplevel(self.root)
        erro.title("Erro")
        erro.geometry("300x100")
        ctk.CTkLabel(erro, text=mensagem).pack(pady=20)
        ctk.CTkButton(erro, text="OK", command=erro.destroy).pack()
        
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PadariaApp()
    app.executar()