"""
View de Compras
Tela de registro e gerenciamento de compras
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from src.controllers.purchase_controller import PurchaseController
from src.controllers.product_controller import ProductController
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class PurchasesView(ctk.CTkFrame):
    """Tela de compras"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.purchase_controller = PurchaseController()
        self.db = SessionLocal()
        
        self.create_widgets()
        self.load_purchases()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="🛍️ Compras",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame de ações
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Nova Compra
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Nova Compra",
            font=("Arial", 14),
            width=150,
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            command=self.show_new_purchase_dialog
        )
        new_btn.pack(side="left", padx=5)
        
        # Botão Atualizar
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Atualizar",
            font=("Arial", 14),
            width=120,
            height=40,
            command=self.load_purchases
        )
        refresh_btn.pack(side="left", padx=5)
        
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
            columns=("ID", "Nº Compra", "Data", "Fornecedor", "Total", "Itens"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nº Compra", text="Nº Compra")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Fornecedor", text="Fornecedor")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Itens", text="Qtd Itens")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nº Compra", width=150, anchor="center")
        self.tree.column("Data", width=150, anchor="center")
        self.tree.column("Fornecedor", width=300)
        self.tree.column("Total", width=150, anchor="center")
        self.tree.column("Itens", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind duplo clique
        self.tree.bind("<Double-1>", lambda e: self.view_purchase_details())
        
        # Frame de botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        view_btn = ctk.CTkButton(
            btn_frame,
            text="👁️ Ver Detalhes",
            width=140,
            command=self.view_purchase_details
        )
        view_btn.pack(side="left", padx=5)
    
    def load_purchases(self):
        """Carrega compras no Treeview"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar compras
        purchases = self.purchase_controller.list_purchases(self.db)
        
        for purchase in purchases[:100]:  # Limitar a 100
            self.tree.insert("", "end", values=(
                purchase.id,
                purchase.purchase_number,
                purchase.purchase_date.strftime('%d/%m/%Y %H:%M'),
                purchase.supplier.name,
                f"R$ {purchase.total_amount:.2f}",
                len(purchase.items)
            ))
    
    def show_new_purchase_dialog(self):
        """Mostra diálogo de nova compra"""
        dialog = NewPurchaseDialog(self, self.user_data)
        self.wait_window(dialog)
        self.load_purchases()
    
    def view_purchase_details(self):
        """Visualiza detalhes da compra"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma compra para ver os detalhes.")
            return
        
        item = self.tree.item(selection[0])
        purchase_id = item['values'][0]
        
        purchase = self.purchase_controller.get_purchase(self.db, purchase_id)
        if purchase:
            dialog = PurchaseDetailsDialog(self, purchase)
            self.wait_window(dialog)


class NewPurchaseDialog(ctk.CTkToplevel):
    """Diálogo de nova compra"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.purchase_controller = PurchaseController()
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.title("Nova Compra")
        
        self.transient(parent)
        self.grab_set()
        
        self.items = []
        
        # Maximizar janela
        set_dialog_size(self, 'large', maximized=True)
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Cria widgets do diálogo"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Nova Compra",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 20))
        
        # Fornecedor (simulado - em produção viria de uma tabela)
        supplier_frame = ctk.CTkFrame(main_frame)
        supplier_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(supplier_frame, text="Fornecedor:", font=("Arial", 12)).pack(side="left", padx=5)
        self.supplier_entry = ctk.CTkEntry(supplier_frame, width=400, placeholder_text="Nome do fornecedor")
        self.supplier_entry.pack(side="left", padx=5)
        
        # Frame de seleção de produto
        select_frame = ctk.CTkFrame(main_frame)
        select_frame.pack(fill="x", pady=10)
        
        # Produto
        ctk.CTkLabel(select_frame, text="Produto:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.product_var = ctk.StringVar()
        self.product_combo = ctk.CTkComboBox(
            select_frame,
            variable=self.product_var,
            width=300,
            state="readonly"
        )
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Quantidade
        ctk.CTkLabel(select_frame, text="Quantidade:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.qty_entry = ctk.CTkEntry(select_frame, width=100, placeholder_text="0")
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Preço unitário
        ctk.CTkLabel(select_frame, text="Preço Unit:", font=("Arial", 12)).grid(row=0, column=4, padx=5, pady=5)
        self.price_entry = ctk.CTkEntry(select_frame, width=100, placeholder_text="0.00")
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Botão adicionar
        add_btn = ctk.CTkButton(
            select_frame,
            text="➕ Adicionar",
            width=100,
            command=self.add_item
        )
        add_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # Frame da tabela de itens
        items_frame = ctk.CTkFrame(main_frame)
        items_frame.pack(fill="both", expand=True, pady=10)
        
        # Treeview de itens
        style = ttk.Style()
        style.configure("Items.Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       font=("Arial", 10))
        
        scrollbar = ttk.Scrollbar(items_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.items_tree = ttk.Treeview(
            items_frame,
            columns=("Produto", "Quantidade", "Preço Unit.", "Subtotal"),
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Items.Treeview",
            height=10
        )
        scrollbar.config(command=self.items_tree.yview)
        
        self.items_tree.heading("Produto", text="Produto")
        self.items_tree.heading("Quantidade", text="Quantidade")
        self.items_tree.heading("Preço Unit.", text="Preço Unit.")
        self.items_tree.heading("Subtotal", text="Subtotal")
        
        self.items_tree.column("Produto", width=400)
        self.items_tree.column("Quantidade", width=100, anchor="center")
        self.items_tree.column("Preço Unit.", width=100, anchor="center")
        self.items_tree.column("Subtotal", width=120, anchor="center")
        
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão remover item
        remove_btn = ctk.CTkButton(
            main_frame,
            text="🗑️ Remover Item",
            width=150,
            fg_color="red",
            hover_color="darkred",
            command=self.remove_item
        )
        remove_btn.pack(pady=5)
        
        # Frame de totais
        totals_frame = ctk.CTkFrame(main_frame)
        totals_frame.pack(fill="x", pady=10)
        
        # Total
        ctk.CTkLabel(totals_frame, text="Valor Total:", font=("Arial", 16, "bold")).pack(side="left", padx=20)
        self.total_label = ctk.CTkLabel(totals_frame, text="R$ 0,00", font=("Arial", 16, "bold"), text_color="blue")
        self.total_label.pack(side="left", padx=10)
        
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
            text="✅ Finalizar Compra",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="blue",
            hover_color="darkblue",
            command=self.finalize_purchase
        )
        save_btn.pack(side="right", padx=5)
    
    def load_products(self):
        """Carrega produtos no combobox"""
        products = self.product_controller.list_products(self.db, active_only=True)
        self.products_dict = {f"{p.code} - {p.name}": p for p in products}
        self.product_combo.configure(values=list(self.products_dict.keys()))
    
    def add_item(self):
        """Adiciona item à compra"""
        selected = self.product_var.get()
        if not selected or selected not in self.products_dict:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        
        try:
            qty = float(self.qty_entry.get())
            price = float(self.price_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e preço devem ser numéricos!")
            return
        
        if qty <= 0 or price <= 0:
            messagebox.showwarning("Aviso", "Quantidade e preço devem ser maiores que zero.")
            return
        
        product = self.products_dict[selected]
        subtotal = qty * price
        
        # Adicionar à lista
        self.items.append({
            'product_id': product.id,
            'product_name': product.name,
            'quantity': qty,
            'unit_price': price,
            'subtotal': subtotal
        })
        
        # Adicionar ao treeview
        self.items_tree.insert("", "end", values=(
            product.name,
            f"{qty:.2f}",
            f"R$ {price:.2f}",
            f"R$ {subtotal:.2f}"
        ))
        
        # Limpar campos
        self.qty_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.product_var.set("")
        
        self.calculate_total()
    
    def remove_item(self):
        """Remove item selecionado"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        
        index = self.items_tree.index(selection[0])
        self.items.pop(index)
        self.items_tree.delete(selection[0])
        
        self.calculate_total()
    
    def calculate_total(self):
        """Calcula total"""
        total = sum(item['subtotal'] for item in self.items)
        self.total_label.configure(text=f"R$ {total:.2f}")
    
    def finalize_purchase(self):
        """Finaliza a compra"""
        supplier_name = self.supplier_entry.get().strip()
        
        if not supplier_name:
            messagebox.showwarning("Aviso", "Informe o nome do fornecedor.")
            return
        
        if not self.items:
            messagebox.showwarning("Aviso", "Adicione pelo menos um item à compra.")
            return
        
        # Por enquanto, criar um fornecedor temporário
        # Em produção, buscar da tabela de fornecedores
        from src.models import Supplier
        supplier = self.db.query(Supplier).filter(Supplier.name == supplier_name).first()
        if not supplier:
            supplier = Supplier(name=supplier_name)
            self.db.add(supplier)
            self.db.commit()
            self.db.refresh(supplier)
        
        # Criar compra
        purchase = self.purchase_controller.create_purchase(
            self.db,
            user_id=self.user_data['id'],
            supplier_id=supplier.id,
            items=self.items
        )
        
        if purchase:
            messagebox.showinfo(
                "Sucesso",
                f"Compra realizada com sucesso!\n\n"
                f"Número: {purchase.purchase_number}\n"
                f"Valor: R$ {purchase.total_amount:.2f}\n"
                f"Fornecedor: {supplier_name}\n\n"
                f"✅ Estoque atualizado automaticamente!"
            )
            self.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao realizar compra.")


class PurchaseDetailsDialog(ctk.CTkToplevel):
    """Diálogo de detalhes da compra"""
    
    def __init__(self, parent, purchase):
        super().__init__(parent)
        
        self.purchase = purchase
        
        self.title(f"Detalhes da Compra - {purchase.purchase_number}")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'large', maximized=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = ctk.CTkFrame(main_frame)
        header.pack(fill="x", pady=10)
        
        ctk.CTkLabel(header, text=f"Compra: {self.purchase.purchase_number}", font=("Arial", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(header, text=f"Data: {self.purchase.purchase_date.strftime('%d/%m/%Y %H:%M')}", font=("Arial", 12)).pack()
        ctk.CTkLabel(header, text=f"Fornecedor: {self.purchase.supplier.name}", font=("Arial", 12)).pack()
        ctk.CTkLabel(header, text=f"Comprador: {self.purchase.user.full_name}", font=("Arial", 12)).pack()
        
        # Itens
        items_frame = ctk.CTkFrame(main_frame)
        items_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(items_frame, text="Itens da Compra:", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Treeview
        style = ttk.Style()
        scrollbar = ttk.Scrollbar(items_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            items_frame,
            columns=("Produto", "Quantidade", "Preço Unit.", "Subtotal"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=10
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading("Produto", text="Produto")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Preço Unit.", text="Preço Unit.")
        tree.heading("Subtotal", text="Subtotal")
        
        tree.column("Produto", width=350)
        tree.column("Quantidade", width=100, anchor="center")
        tree.column("Preço Unit.", width=100, anchor="center")
        tree.column("Subtotal", width=120, anchor="center")
        
        for item in self.purchase.items:
            tree.insert("", "end", values=(
                item.product.name,
                f"{item.quantity:.2f}",
                f"R$ {item.unit_price:.2f}",
                f"R$ {item.subtotal:.2f}"
            ))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Total
        totals_frame = ctk.CTkFrame(main_frame)
        totals_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            totals_frame,
            text=f"Valor Total: R$ {self.purchase.total_amount:.2f}",
            font=("Arial", 16, "bold"),
            text_color="blue"
        ).pack(pady=10)
        
        # Observações
        if self.purchase.notes:
            ctk.CTkLabel(totals_frame, text=f"Obs: {self.purchase.notes}", font=("Arial", 11)).pack()
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            self,
            text="Fechar",
            width=150,
            command=self.destroy
        )
        close_btn.pack(pady=20)
