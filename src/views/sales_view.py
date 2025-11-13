"""
View de Vendas
Tela de registro e gerenciamento de vendas
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from src.controllers.sales_controller import SalesController
from src.controllers.product_controller import ProductController
from src.controllers.cash_register_controller import CashRegisterController
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class SalesView(ctk.CTkFrame):
    """Tela de vendas"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.sales_controller = SalesController()
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.create_widgets()
        self.load_sales()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="🛒 Vendas",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame de ações
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Nova Venda
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Nova Venda",
            font=("Arial", 14),
            width=150,
            height=40,
            fg_color="green",
            hover_color="darkgreen",
            command=self.show_new_sale_dialog
        )
        new_btn.pack(side="left", padx=5)
        
        # Botão Atualizar
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Atualizar",
            font=("Arial", 14),
            width=120,
            height=40,
            command=self.load_sales
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
            columns=("ID", "Nº Venda", "Data", "Cliente", "Total", "Desconto", "Final", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nº Venda", text="Nº Venda")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Desconto", text="Desconto")
        self.tree.heading("Final", text="Valor Final")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nº Venda", width=120, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Cliente", width=200)
        self.tree.column("Total", width=100, anchor="center")
        self.tree.column("Desconto", width=100, anchor="center")
        self.tree.column("Final", width=100, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind duplo clique
        self.tree.bind("<Double-1>", lambda e: self.view_sale_details())
        
        # Frame de botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        view_btn = ctk.CTkButton(
            btn_frame,
            text="👁️ Ver Detalhes",
            width=140,
            command=self.view_sale_details
        )
        view_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar Venda",
            width=140,
            fg_color="red",
            hover_color="darkred",
            command=self.cancel_sale
        )
        cancel_btn.pack(side="left", padx=5)
    
    def load_sales(self):
        """Carrega vendas no Treeview"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar vendas (últimos 30 dias)
        sales = self.sales_controller.list_sales(self.db, include_cancelled=True)
        
        for sale in sales[:100]:  # Limitar a 100 registros
            customer_name = sale.customer.name if sale.customer else "Cliente Avulso"
            status = "Cancelada" if sale.is_cancelled else "OK"
            
            tag = "cancelled" if sale.is_cancelled else ""
            
            self.tree.insert("", "end", values=(
                sale.id,
                sale.sale_number,
                sale.sale_date.strftime('%d/%m/%Y %H:%M'),
                customer_name,
                f"R$ {sale.total_amount:.2f}",
                f"R$ {sale.discount:.2f}",
                f"R$ {sale.final_amount:.2f}",
                status
            ), tags=(tag,))
        
        self.tree.tag_configure("cancelled", foreground="gray")
    
    def show_new_sale_dialog(self):
        """Mostra diálogo de nova venda"""
        dialog = NewSaleDialog(self, self.user_data)
        self.wait_window(dialog)
        self.load_sales()
    
    def view_sale_details(self):
        """Visualiza detalhes da venda"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma venda para ver os detalhes.")
            return
        
        item = self.tree.item(selection[0])
        sale_id = item['values'][0]
        
        sale = self.sales_controller.get_sale(self.db, sale_id)
        if sale:
            dialog = SaleDetailsDialog(self, sale)
            self.wait_window(dialog)
    
    def cancel_sale(self):
        """Cancela venda selecionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma venda para cancelar.")
            return
        
        item = self.tree.item(selection[0])
        sale_id = item['values'][0]
        sale_number = item['values'][1]
        
        sale = self.sales_controller.get_sale(self.db, sale_id)
        if sale and sale.is_cancelled:
            messagebox.showinfo("Informação", "Esta venda já está cancelada.")
            return
        
        if messagebox.askyesno("Confirmar", f"Deseja cancelar a venda {sale_number}?\n\nOs produtos serão devolvidos ao estoque."):
            if self.sales_controller.cancel_sale(self.db, sale_id):
                messagebox.showinfo("Sucesso", "Venda cancelada com sucesso!")
                self.load_sales()
            else:
                messagebox.showerror("Erro", "Erro ao cancelar venda.")


class NewSaleDialog(ctk.CTkToplevel):
    """Diálogo de nova venda"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.sales_controller = SalesController()
        self.product_controller = ProductController()
        self.db = SessionLocal()
        
        self.title("Nova Venda")
        
        # Tamanho responsivo
        set_dialog_size(self, 'large')
        
        self.transient(parent)
        self.grab_set()
        
        self.items = []  # Lista de itens da venda
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Cria widgets do diálogo"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Nova Venda",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 20))
        
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
            state="readonly",
            command=self.on_product_selected
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
        
        # Frame de tipo de venda e pagamento
        payment_frame = ctk.CTkFrame(main_frame)
        payment_frame.pack(fill="x", pady=15)
        
        # Tipo de Venda
        type_container = ctk.CTkFrame(payment_frame, fg_color="transparent")
        type_container.pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(type_container, text="🛎️ Tipo de Venda:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 5))
        self.sale_type_var = ctk.StringVar(value="balcao")
        ctk.CTkRadioButton(type_container, text="Balcão", variable=self.sale_type_var, value="balcao", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(type_container, text="Comanda", variable=self.sale_type_var, value="comanda", font=("Arial", 12)).pack(anchor="w", pady=2)
        
        # Forma de Pagamento
        payment_container = ctk.CTkFrame(payment_frame, fg_color="transparent")
        payment_container.pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(payment_container, text="💳 Forma de Pagamento:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 5))
        self.payment_method_var = ctk.StringVar(value="dinheiro")
        ctk.CTkRadioButton(payment_container, text="💵 Dinheiro", variable=self.payment_method_var, value="dinheiro", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(payment_container, text="💳 Cartão", variable=self.payment_method_var, value="cartao", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(payment_container, text="📱 PIX", variable=self.payment_method_var, value="pix", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(payment_container, text="🔄 Outros", variable=self.payment_method_var, value="outros", font=("Arial", 12)).pack(anchor="w", pady=2)
        
        # Frame de totais
        totals_frame = ctk.CTkFrame(main_frame)
        totals_frame.pack(fill="x", pady=10)
        
        # Total
        ctk.CTkLabel(totals_frame, text="Total:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.total_label = ctk.CTkLabel(totals_frame, text="R$ 0,00", font=("Arial", 14))
        self.total_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Desconto
        ctk.CTkLabel(totals_frame, text="Desconto:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.discount_entry = ctk.CTkEntry(totals_frame, width=150, placeholder_text="0.00")
        self.discount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.discount_entry.bind("<KeyRelease>", lambda e: self.calculate_totals())
        
        # Valor Final
        ctk.CTkLabel(totals_frame, text="Valor Final:", font=("Arial", 16, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.final_label = ctk.CTkLabel(totals_frame, text="R$ 0,00", font=("Arial", 16, "bold"), text_color="green")
        self.final_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
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
            text="✅ Finalizar Venda",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="green",
            hover_color="darkgreen",
            command=self.finalize_sale
        )
        save_btn.pack(side="right", padx=5)
    
    def load_products(self):
        """Carrega produtos no combobox"""
        products = self.product_controller.list_products(self.db, active_only=True)
        self.products_dict = {f"{p.code} - {p.name}": p for p in products}
        self.product_combo.configure(values=list(self.products_dict.keys()))
    
    def on_product_selected(self, selected=None):
        """Quando produto é selecionado"""
        # Se não passou o valor, pega do StringVar
        if selected is None:
            selected = self.product_var.get()
        
        if selected in self.products_dict:
            product = self.products_dict[selected]
            self.price_entry.delete(0, "end")
            self.price_entry.insert(0, f"{product.sale_price:.2f}")
    
    def add_item(self):
        """Adiciona item à venda"""
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
        
        # Verificar estoque
        if product.stock_quantity < qty:
            messagebox.showwarning("Aviso", f"Estoque insuficiente! Disponível: {product.stock_quantity:.0f}")
            return
        
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
        self.product_var.set("")
        self.price_entry.delete(0, "end")
        
        self.calculate_totals()
    
    def remove_item(self):
        """Remove item selecionado"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        
        index = self.items_tree.index(selection[0])
        self.items.pop(index)
        self.items_tree.delete(selection[0])
        
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calcula totais"""
        total = sum(item['subtotal'] for item in self.items)
        
        try:
            discount = float(self.discount_entry.get().replace(",", ".")) if self.discount_entry.get() else 0.0
        except ValueError:
            discount = 0.0
        
        final = max(0, total - discount)
        
        self.total_label.configure(text=f"R$ {total:.2f}")
        self.final_label.configure(text=f"R$ {final:.2f}")
    
    def finalize_sale(self):
        """Finaliza a venda"""
        if not self.items:
            messagebox.showwarning("Aviso", "Adicione pelo menos um item à venda.")
            return
        
        try:
            discount = float(self.discount_entry.get().replace(",", ".")) if self.discount_entry.get() else 0.0
        except ValueError:
            discount = 0.0
        
        # Obter tipo de venda e forma de pagamento
        sale_type = self.sale_type_var.get()
        payment_method = self.payment_method_var.get()
        
        # Criar venda
        sale = self.sales_controller.create_sale(
            self.db,
            user_id=self.user_data['id'],
            items=self.items,
            discount=discount,
            payment_method=payment_method
        )
        
        if sale:
            # Registrar no caixa (se houver caixa aberto)
            cash_controller = CashRegisterController()
            cash_register = cash_controller.get_open_cash_register(self.db)
            
            if cash_register:
                movement, error = cash_controller.register_sale_in_cash(
                    self.db,
                    sale_id=sale.id,
                    sale_type=sale_type,
                    payment_method=payment_method,
                    amount=sale.final_amount
                )
                
                if error:
                    messagebox.showwarning(
                        "Aviso",
                        f"Venda realizada, mas houve erro ao registrar no caixa:\n{error}\n\n"
                        f"Registre manualmente se necessário."
                    )
            else:
                messagebox.showwarning(
                    "Aviso Caixa",
                    "⚠️ Venda realizada com sucesso, mas NÃO FOI REGISTRADA NO CAIXA!\n\n"
                    "Não há caixa aberto. Abra o caixa para registrar vendas automaticamente."
                )
            
            tipo_venda_label = "BALCÃO" if sale_type == "balcao" else "COMANDA"
            messagebox.showinfo(
                "Sucesso",
                f"✅ Venda realizada com sucesso!\n\n"
                f"Número: {sale.sale_number}\n"
                f"Tipo: {tipo_venda_label}\n"
                f"Pagamento: {payment_method.upper()}\n"
                f"Valor: R$ {sale.final_amount:.2f}"
            )
            self.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao realizar venda.")


class SaleDetailsDialog(ctk.CTkToplevel):
    """Diálogo de detalhes da venda"""
    
    def __init__(self, parent, sale):
        super().__init__(parent)
        
        self.sale = sale
        
        self.title(f"Detalhes da Venda - {sale.sale_number}")
        
        # Tamanho responsivo
        set_dialog_size(self, 'medium')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = ctk.CTkFrame(main_frame)
        header.pack(fill="x", pady=10)
        
        ctk.CTkLabel(header, text=f"Venda: {self.sale.sale_number}", font=("Arial", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(header, text=f"Data: {self.sale.sale_date.strftime('%d/%m/%Y %H:%M')}", font=("Arial", 12)).pack()
        ctk.CTkLabel(header, text=f"Cliente: {self.sale.customer.name if self.sale.customer else 'Cliente Avulso'}", font=("Arial", 12)).pack()
        ctk.CTkLabel(header, text=f"Vendedor: {self.sale.user.full_name}", font=("Arial", 12)).pack()
        
        if self.sale.is_cancelled:
            ctk.CTkLabel(header, text="⚠️ VENDA CANCELADA", font=("Arial", 14, "bold"), text_color="red").pack(pady=5)
        
        # Itens
        items_frame = ctk.CTkFrame(main_frame)
        items_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(items_frame, text="Itens da Venda:", font=("Arial", 14, "bold")).pack(pady=10)
        
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
        
        for item in self.sale.items:
            tree.insert("", "end", values=(
                item.product.name,
                f"{item.quantity:.2f}",
                f"R$ {item.unit_price:.2f}",
                f"R$ {item.subtotal:.2f}"
            ))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Totais
        totals_frame = ctk.CTkFrame(main_frame)
        totals_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(totals_frame, text=f"Total: R$ {self.sale.total_amount:.2f}", font=("Arial", 12)).pack()
        ctk.CTkLabel(totals_frame, text=f"Desconto: R$ {self.sale.discount:.2f}", font=("Arial", 12)).pack()
        ctk.CTkLabel(totals_frame, text=f"Valor Final: R$ {self.sale.final_amount:.2f}", font=("Arial", 16, "bold"), text_color="green").pack(pady=5)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            self,
            text="Fechar",
            width=150,
            command=self.destroy
        )
        close_btn.pack(pady=20)
