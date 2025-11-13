"""
View de Produtos
Tela de gerenciamento de produtos
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from src.controllers.product_controller import ProductController
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class ProductsView(ctk.CTkFrame):
    """Tela de produtos e estoque"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="📦 Produtos e Estoque",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame de ações
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Novo Produto
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Novo Produto",
            font=("Arial", 14),
            width=150,
            height=40,
            command=self.show_new_product_dialog
        )
        new_btn.pack(side="left", padx=5)
        
        # Botão Atualizar
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Atualizar",
            font=("Arial", 14),
            width=120,
            height=40,
            command=self.load_products
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Campo de busca
        search_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=5)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar produto...",
            width=250,
            height=40
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_products())
        
        # Frame da tabela
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=("Arial", 10))
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", "#1f538d")])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Código", "Nome", "Categoria", "Preço Venda", "Estoque", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Preço Venda", text="Preço Venda")
        self.tree.heading("Estoque", text="Estoque")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Código", width=100, anchor="center")
        self.tree.column("Nome", width=250)
        self.tree.column("Categoria", width=120)
        self.tree.column("Preço Venda", width=100, anchor="center")
        self.tree.column("Estoque", width=80, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind duplo clique
        self.tree.bind("<Double-1>", lambda e: self.edit_product())
        
        # Frame de botões de ação
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            width=120,
            command=self.edit_product
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Inativar",
            width=120,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_product
        )
        delete_btn.pack(side="left", padx=5)
        
        stock_btn = ctk.CTkButton(
            btn_frame,
            text="📊 Ajustar Estoque",
            width=150,
            command=self.adjust_stock
        )
        stock_btn.pack(side="left", padx=5)
    
    def load_products(self):
        """Carrega produtos no Treeview"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar produtos
        products = self.product_controller.list_products(self.db, active_only=False)
        
        for product in products:
            category_name = product.category.name if product.category else "N/A"
            status = "Ativo" if product.is_active else "Inativo"
            
            # Colorir linha se estoque baixo
            tag = "low_stock" if product.stock_quantity <= product.min_stock else ""
            
            self.tree.insert("", "end", values=(
                product.id,
                product.code,
                product.name,
                category_name,
                f"R$ {product.sale_price:.2f}",
                f"{product.stock_quantity:.0f}",
                status
            ), tags=(tag,))
        
        # Configurar cor para estoque baixo
        self.tree.tag_configure("low_stock", background="#8B0000")
    
    def search_products(self):
        """Busca produtos"""
        search_term = self.search_entry.get().strip()
        
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_term:
            self.load_products()
            return
        
        # Buscar produtos
        products = self.product_controller.search_products(self.db, search_term)
        
        for product in products:
            category_name = product.category.name if product.category else "N/A"
            status = "Ativo" if product.is_active else "Inativo"
            
            self.tree.insert("", "end", values=(
                product.id,
                product.code,
                product.name,
                category_name,
                f"R$ {product.sale_price:.2f}",
                f"{product.stock_quantity:.0f}",
                status
            ))
    
    def show_new_product_dialog(self):
        """Mostra diálogo de novo produto"""
        dialog = ProductDialog(self, "Novo Produto", None)
        self.wait_window(dialog)
        self.load_products()
    
    def edit_product(self):
        """Edita produto selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        
        product = self.product_controller.get_product(self.db, product_id)
        if product:
            dialog = ProductDialog(self, "Editar Produto", product)
            self.wait_window(dialog)
            self.load_products()
    
    def delete_product(self):
        """Inativa produto selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para inativar.")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][2]
        
        if messagebox.askyesno("Confirmar", f"Deseja inativar o produto '{product_name}'?"):
            if self.product_controller.delete_product(self.db, product_id):
                messagebox.showinfo("Sucesso", "Produto inativado com sucesso!")
                self.load_products()
            else:
                messagebox.showerror("Erro", "Erro ao inativar produto.")
    
    def adjust_stock(self):
        """Ajusta estoque do produto"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para ajustar o estoque.")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        
        product = self.product_controller.get_product(self.db, product_id)
        if product:
            dialog = StockAdjustDialog(self, product)
            self.wait_window(dialog)
            self.load_products()


class ProductDialog(ctk.CTkToplevel):
    """Diálogo de cadastro/edição de produto"""
    
    def __init__(self, parent, title, product=None):
        super().__init__(parent)
        
        self.parent = parent
        self.product = product
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.title(title)
        
        # Tamanho responsivo
        set_dialog_size(self, 'medium')
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        if product:
            self.fill_data()
    
    def create_widgets(self):
        """Cria widgets do diálogo"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Código
        ctk.CTkLabel(main_frame, text="Código:*", font=("Arial", 12)).pack(pady=(10, 5), anchor="w")
        self.code_entry = ctk.CTkEntry(main_frame, width=450, height=35)
        self.code_entry.pack(pady=(0, 10))
        
        # Nome
        ctk.CTkLabel(main_frame, text="Nome:*", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.name_entry = ctk.CTkEntry(main_frame, width=450, height=35)
        self.name_entry.pack(pady=(0, 10))
        
        # Descrição
        ctk.CTkLabel(main_frame, text="Descrição:", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.desc_entry = ctk.CTkEntry(main_frame, width=450, height=35)
        self.desc_entry.pack(pady=(0, 10))
        
        # Unidade
        ctk.CTkLabel(main_frame, text="Unidade:*", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.unit_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="UN, KG, L, etc")
        self.unit_entry.insert(0, "UN")
        self.unit_entry.pack(pady=(0, 10))
        
        # Frame de preços
        price_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=10)
        
        # Preço de custo
        cost_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        cost_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkLabel(cost_frame, text="Preço de Custo:", font=("Arial", 12)).pack(anchor="w")
        self.cost_entry = ctk.CTkEntry(cost_frame, width=210, height=35, placeholder_text="0.00")
        self.cost_entry.pack()
        
        # Preço de venda
        sale_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        sale_frame.pack(side="left", expand=True, fill="x", padx=(5, 0))
        ctk.CTkLabel(sale_frame, text="Preço de Venda:*", font=("Arial", 12)).pack(anchor="w")
        self.sale_entry = ctk.CTkEntry(sale_frame, width=210, height=35, placeholder_text="0.00")
        self.sale_entry.pack()
        
        # Frame de estoque
        stock_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stock_frame.pack(fill="x", pady=10)
        
        # Estoque inicial
        initial_frame = ctk.CTkFrame(stock_frame, fg_color="transparent")
        initial_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkLabel(initial_frame, text="Estoque Inicial:", font=("Arial", 12)).pack(anchor="w")
        self.stock_entry = ctk.CTkEntry(initial_frame, width=210, height=35, placeholder_text="0")
        self.stock_entry.pack()
        
        # Estoque mínimo
        min_frame = ctk.CTkFrame(stock_frame, fg_color="transparent")
        min_frame.pack(side="left", expand=True, fill="x", padx=(5, 0))
        ctk.CTkLabel(min_frame, text="Estoque Mínimo:", font=("Arial", 12)).pack(anchor="w")
        self.min_stock_entry = ctk.CTkEntry(min_frame, width=210, height=35, placeholder_text="0")
        self.min_stock_entry.pack()
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=150,
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Salvar",
            width=150,
            fg_color="green",
            hover_color="darkgreen",
            command=self.save_product
        )
        save_btn.pack(side="right", padx=5)
    
    def fill_data(self):
        """Preenche dados do produto"""
        self.code_entry.insert(0, self.product.code)
        self.code_entry.configure(state="disabled")
        self.name_entry.insert(0, self.product.name)
        if self.product.description:
            self.desc_entry.insert(0, self.product.description)
        self.unit_entry.delete(0, "end")
        self.unit_entry.insert(0, self.product.unit)
        self.cost_entry.insert(0, f"{self.product.cost_price:.2f}")
        self.sale_entry.insert(0, f"{self.product.sale_price:.2f}")
        self.stock_entry.insert(0, f"{self.product.stock_quantity:.0f}")
        self.stock_entry.configure(state="disabled")
        self.min_stock_entry.insert(0, f"{self.product.min_stock:.0f}")
    
    def save_product(self):
        """Salva produto"""
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        unit = self.unit_entry.get().strip()
        
        try:
            cost_price = float(self.cost_entry.get().replace(",", ".")) if self.cost_entry.get() else 0.0
            sale_price = float(self.sale_entry.get().replace(",", "."))
            stock = float(self.stock_entry.get()) if self.stock_entry.get() else 0.0
            min_stock = float(self.min_stock_entry.get()) if self.min_stock_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
            return
        
        if not code or not name or not unit:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios (*).")
            return
        
        if sale_price <= 0:
            messagebox.showwarning("Aviso", "Preço de venda deve ser maior que zero.")
            return
        
        if self.product:
            # Atualizar
            success = self.product_controller.update_product(
                self.db,
                self.product.id,
                name=name,
                description=description,
                unit=unit,
                cost_price=cost_price,
                sale_price=sale_price,
                min_stock=min_stock
            )
            
            if success:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                self.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar produto.")
        else:
            # Criar novo
            product = self.product_controller.create_product(
                self.db,
                code=code,
                name=name,
                description=description,
                unit=unit,
                cost_price=cost_price,
                sale_price=sale_price,
                stock_quantity=stock,
                min_stock=min_stock
            )
            
            if product:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar produto. Código já existe?")


class StockAdjustDialog(ctk.CTkToplevel):
    """Diálogo de ajuste de estoque"""
    
    def __init__(self, parent, product):
        super().__init__(parent)
        
        self.parent = parent
        self.product = product
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.title("Ajustar Estoque")
        
        # Tamanho responsivo
        set_dialog_size(self, 'small')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info do produto
        ctk.CTkLabel(
            main_frame,
            text=f"Produto: {self.product.name}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text=f"Estoque Atual: {self.product.stock_quantity:.0f} {self.product.unit}",
            font=("Arial", 12)
        ).pack(pady=5)
        
        # Tipo de ajuste
        ctk.CTkLabel(main_frame, text="Tipo de Movimentação:", font=("Arial", 12)).pack(pady=(15, 5))
        self.type_var = ctk.StringVar(value="entrada")
        
        type_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        type_frame.pack(pady=5)
        
        ctk.CTkRadioButton(
            type_frame,
            text="Entrada",
            variable=self.type_var,
            value="entrada"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            type_frame,
            text="Saída",
            variable=self.type_var,
            value="saida"
        ).pack(side="left", padx=10)
        
        # Quantidade
        ctk.CTkLabel(main_frame, text="Quantidade:", font=("Arial", 12)).pack(pady=(15, 5))
        self.qty_entry = ctk.CTkEntry(main_frame, width=300, height=35, placeholder_text="0")
        self.qty_entry.pack(pady=5)
        
        # Motivo
        ctk.CTkLabel(main_frame, text="Motivo:", font=("Arial", 12)).pack(pady=(15, 5))
        self.reason_entry = ctk.CTkEntry(main_frame, width=300, height=35, placeholder_text="Motivo do ajuste")
        self.reason_entry.pack(pady=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Confirmar",
            width=120,
            fg_color="green",
            hover_color="darkgreen",
            command=self.adjust_stock
        )
        save_btn.pack(side="right", padx=5)
    
    def adjust_stock(self):
        """Ajusta estoque"""
        try:
            quantity = float(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            return
        
        if quantity <= 0:
            messagebox.showwarning("Aviso", "Quantidade deve ser maior que zero.")
            return
        
        movement_type = self.type_var.get()
        reason = self.reason_entry.get().strip() or "Ajuste manual"
        
        success = self.product_controller.update_stock(
            self.db,
            self.product.id,
            quantity,
            movement_type,
            reason
        )
        
        if success:
            messagebox.showinfo("Sucesso", "Estoque ajustado com sucesso!")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao ajustar estoque.")
