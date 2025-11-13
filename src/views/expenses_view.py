"""
View de Despesas
Tela de registro e gerenciamento de despesas
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from src.controllers.expense_controller import ExpenseController
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class ExpensesView(ctk.CTkFrame):
    """Tela de despesas"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.expense_controller = ExpenseController()
        self.db = SessionLocal()
        
        self.create_widgets()
        self.load_expenses()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="💸 Despesas",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame de resumo
        summary_frame = ctk.CTkFrame(self)
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        # Cards de resumo
        self.total_card = ctk.CTkLabel(summary_frame, text="Total: R$ 0,00", font=("Arial", 12))
        self.total_card.pack(side="left", padx=20, pady=10)
        
        self.paid_card = ctk.CTkLabel(summary_frame, text="Pagas: R$ 0,00", font=("Arial", 12), text_color="green")
        self.paid_card.pack(side="left", padx=20, pady=10)
        
        self.pending_card = ctk.CTkLabel(summary_frame, text="Pendentes: R$ 0,00", font=("Arial", 12), text_color="red")
        self.pending_card.pack(side="left", padx=20, pady=10)
        
        # Frame de ações
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão Nova Despesa
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Nova Despesa",
            font=("Arial", 14),
            width=150,
            height=40,
            fg_color="red",
            hover_color="darkred",
            command=self.show_new_expense_dialog
        )
        new_btn.pack(side="left", padx=5)
        
        # Botão Atualizar
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Atualizar",
            font=("Arial", 14),
            width=120,
            height=40,
            command=self.load_expenses
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Filtro de status
        filter_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        filter_frame.pack(side="right", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Filtrar:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.filter_var = ctk.StringVar(value="Todas")
        filter_combo = ctk.CTkComboBox(
            filter_frame,
            variable=self.filter_var,
            values=["Todas", "Pagas", "Pendentes"],
            width=150,
            state="readonly",
            command=lambda x: self.load_expenses()
        )
        filter_combo.pack(side="left", padx=5)
        
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
            columns=("ID", "Nº", "Data", "Tipo", "Descrição", "Valor", "Vencimento", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nº", text="Nº Despesa")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Vencimento", text="Vencimento")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nº", width=120, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Tipo", width=100)
        self.tree.column("Descrição", width=250)
        self.tree.column("Valor", width=100, anchor="center")
        self.tree.column("Vencimento", width=100, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame de botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        pay_btn = ctk.CTkButton(
            btn_frame,
            text="✅ Marcar como Paga",
            width=160,
            fg_color="green",
            hover_color="darkgreen",
            command=self.mark_as_paid
        )
        pay_btn.pack(side="left", padx=5)
        
        view_btn = ctk.CTkButton(
            btn_frame,
            text="👁️ Ver Detalhes",
            width=140,
            command=self.view_expense_details
        )
        view_btn.pack(side="left", padx=5)
    
    def load_expenses(self):
        """Carrega despesas no Treeview"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Determinar filtro
        filter_status = self.filter_var.get()
        paid_filter = None
        if filter_status == "Pagas":
            paid_filter = True
        elif filter_status == "Pendentes":
            paid_filter = False
        
        # Buscar despesas
        expenses = self.expense_controller.list_expenses(self.db, paid=paid_filter)
        
        for expense in expenses[:100]:  # Limitar a 100
            status = "Paga" if expense.paid else "Pendente"
            vencimento = expense.due_date.strftime('%d/%m/%Y') if expense.due_date else "N/A"
            
            # Verificar se está vencida
            tag = ""
            if not expense.paid and expense.due_date and expense.due_date < datetime.now():
                tag = "overdue"
            elif expense.paid:
                tag = "paid"
            
            self.tree.insert("", "end", values=(
                expense.id,
                expense.expense_number,
                expense.expense_date.strftime('%d/%m/%Y'),
                expense.expense_type,
                expense.description[:40] + "..." if len(expense.description) > 40 else expense.description,
                f"R$ {expense.amount:.2f}",
                vencimento,
                status
            ), tags=(tag,))
        
        self.tree.tag_configure("overdue", background="#8B0000")
        self.tree.tag_configure("paid", foreground="gray")
        
        # Atualizar resumo
        self.update_summary()
    
    def update_summary(self):
        """Atualiza cards de resumo"""
        summary = self.expense_controller.get_expenses_summary(self.db)
        
        self.total_card.configure(text=f"Total: R$ {summary['total_amount']:.2f}")
        self.paid_card.configure(text=f"Pagas: R$ {summary['paid_amount']:.2f}")
        self.pending_card.configure(text=f"Pendentes: R$ {summary['pending_amount']:.2f}")
    
    def show_new_expense_dialog(self):
        """Mostra diálogo de nova despesa"""
        dialog = ExpenseDialog(self, self.user_data)
        self.wait_window(dialog)
        self.load_expenses()
    
    def mark_as_paid(self):
        """Marca despesa como paga"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma despesa para marcar como paga.")
            return
        
        item = self.tree.item(selection[0])
        expense_id = item['values'][0]
        
        expense = self.expense_controller.get_expense(self.db, expense_id)
        if expense and expense.paid:
            messagebox.showinfo("Informação", "Esta despesa já está marcada como paga.")
            return
        
        if messagebox.askyesno("Confirmar", "Marcar esta despesa como paga?"):
            if self.expense_controller.mark_as_paid(self.db, expense_id):
                messagebox.showinfo("Sucesso", "Despesa marcada como paga!")
                self.load_expenses()
            else:
                messagebox.showerror("Erro", "Erro ao marcar despesa como paga.")
    
    def view_expense_details(self):
        """Visualiza detalhes da despesa"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma despesa para ver os detalhes.")
            return
        
        item = self.tree.item(selection[0])
        expense_id = item['values'][0]
        
        expense = self.expense_controller.get_expense(self.db, expense_id)
        if expense:
            dialog = ExpenseDetailsDialog(self, expense)
            self.wait_window(dialog)


class ExpenseDialog(ctk.CTkToplevel):
    """Diálogo de cadastro de despesa"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.expense_controller = ExpenseController()
        self.db = SessionLocal()
        
        self.title("Nova Despesa")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'medium', maximized=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets do diálogo"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tipo de despesa
        ctk.CTkLabel(main_frame, text="Tipo de Despesa:*", font=("Arial", 12)).pack(pady=(10, 5), anchor="w")
        self.type_var = ctk.StringVar(value="outros")
        type_combo = ctk.CTkComboBox(
            main_frame,
            variable=self.type_var,
            values=["fornecedor", "aluguel", "salario", "imposto", "energia", "agua", "telefone", "internet", "outros"],
            width=450,
            height=35,
            state="readonly"
        )
        type_combo.pack(pady=(0, 10))
        
        # Descrição
        ctk.CTkLabel(main_frame, text="Descrição:*", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.desc_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="Descrição da despesa")
        self.desc_entry.pack(pady=(0, 10))
        
        # Valor
        ctk.CTkLabel(main_frame, text="Valor:*", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.amount_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="0.00")
        self.amount_entry.pack(pady=(0, 10))
        
        # Data da despesa
        ctk.CTkLabel(main_frame, text="Data da Despesa:", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.date_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="DD/MM/AAAA (deixe vazio para hoje)")
        self.date_entry.pack(pady=(0, 10))
        
        # Data de vencimento
        ctk.CTkLabel(main_frame, text="Data de Vencimento:", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.due_date_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="DD/MM/AAAA (opcional)")
        self.due_date_entry.pack(pady=(0, 10))
        
        # Método de pagamento
        ctk.CTkLabel(main_frame, text="Método de Pagamento:", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.payment_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="Dinheiro, Cartão, PIX, etc")
        self.payment_entry.pack(pady=(0, 10))
        
        # Checkbox pago
        self.paid_var = ctk.BooleanVar(value=False)
        paid_check = ctk.CTkCheckBox(
            main_frame,
            text="Marcar como paga",
            variable=self.paid_var,
            font=("Arial", 12)
        )
        paid_check.pack(pady=10)
        
        # Observações
        ctk.CTkLabel(main_frame, text="Observações:", font=("Arial", 12)).pack(pady=(5, 5), anchor="w")
        self.notes_entry = ctk.CTkEntry(main_frame, width=450, height=35, placeholder_text="Observações adicionais")
        self.notes_entry.pack(pady=(0, 10))
        
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
            command=self.save_expense
        )
        save_btn.pack(side="right", padx=5)
    
    def save_expense(self):
        """Salva despesa"""
        expense_type = self.type_var.get()
        description = self.desc_entry.get().strip()
        
        try:
            amount = float(self.amount_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
            return
        
        if not description or amount <= 0:
            messagebox.showwarning("Aviso", "Preencha descrição e valor válido.")
            return
        
        # Processar data
        expense_date = None
        if self.date_entry.get():
            try:
                expense_date = datetime.strptime(self.date_entry.get(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA")
                return
        
        # Processar vencimento
        due_date = None
        if self.due_date_entry.get():
            try:
                due_date = datetime.strptime(self.due_date_entry.get(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data de vencimento inválida! Use DD/MM/AAAA")
                return
        
        payment_method = self.payment_entry.get().strip() or None
        paid = self.paid_var.get()
        notes = self.notes_entry.get().strip() or None
        
        # Criar despesa
        expense = self.expense_controller.create_expense(
            self.db,
            user_id=self.user_data['id'],
            expense_type=expense_type,
            description=description,
            amount=amount,
            expense_date=expense_date,
            due_date=due_date,
            paid=paid,
            payment_method=payment_method,
            notes=notes
        )
        
        if expense:
            messagebox.showinfo("Sucesso", f"Despesa registrada!\n\nNúmero: {expense.expense_number}\nValor: R$ {expense.amount:.2f}")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao registrar despesa.")


class ExpenseDetailsDialog(ctk.CTkToplevel):
    """Diálogo de detalhes da despesa"""
    
    def __init__(self, parent, expense):
        super().__init__(parent)
        
        self.expense = expense
        
        self.title(f"Detalhes da Despesa - {expense.expense_number}")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'medium', maximized=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        ctk.CTkLabel(
            main_frame,
            text=f"Despesa: {self.expense.expense_number}",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        # Informações
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="both", expand=True, pady=10)
        
        details = [
            ("Tipo:", self.expense.expense_type.upper()),
            ("Descrição:", self.expense.description),
            ("Valor:", f"R$ {self.expense.amount:.2f}"),
            ("Data:", self.expense.expense_date.strftime('%d/%m/%Y')),
            ("Vencimento:", self.expense.due_date.strftime('%d/%m/%Y') if self.expense.due_date else "N/A"),
            ("Status:", "PAGA ✅" if self.expense.paid else "PENDENTE ⏳"),
            ("Paga em:", self.expense.paid_date.strftime('%d/%m/%Y') if self.expense.paid_date else "N/A"),
            ("Método:", self.expense.payment_method or "N/A"),
            ("Fornecedor:", self.expense.supplier.name if self.expense.supplier else "N/A"),
            ("Usuário:", self.expense.user.full_name),
            ("Observações:", self.expense.notes or "Nenhuma"),
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            detail_frame.pack(fill="x", pady=5, padx=10)
            
            ctk.CTkLabel(
                detail_frame,
                text=label,
                font=("Arial", 12, "bold"),
                width=120,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                detail_frame,
                text=str(value),
                font=("Arial", 12),
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            self,
            text="Fechar",
            width=150,
            command=self.destroy
        )
        close_btn.pack(pady=20)
