"""
View de Caixa
Tela de controle de caixa com abertura, fechamento e movimentações
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from src.controllers.cash_register_controller import CashRegisterController
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class CashRegisterView(ctk.CTkFrame):
    """Tela de controle de caixa"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        self.current_cash = None
        
        self.create_widgets()
        self.check_cash_status()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="💰 Controle de Caixa",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame principal (será atualizado conforme status do caixa)
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def check_cash_status(self):
        """Verifica status do caixa e exibe tela apropriada"""
        self.current_cash = self.cash_controller.get_open_cash_register(self.db)
        
        # Limpar container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        if self.current_cash:
            self.show_open_cash_view()
        else:
            self.show_closed_cash_view()
    
    def show_closed_cash_view(self):
        """Exibe view quando caixa está fechado"""
        
        # Card de aviso
        warning_frame = ctk.CTkFrame(self.main_container)
        warning_frame.pack(pady=40)
        
        ctk.CTkLabel(
            warning_frame,
            text="⚠️ Caixa Fechado",
            font=("Arial", 24, "bold"),
            text_color="orange"
        ).pack(pady=(30, 10))
        
        ctk.CTkLabel(
            warning_frame,
            text="Não há caixa aberto no momento.\nAbra o caixa para começar a registrar vendas.",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=10)
        
        # Botão abrir caixa
        open_btn = ctk.CTkButton(
            warning_frame,
            text="🔓 Abrir Caixa",
            font=("Arial", 16, "bold"),
            height=50,
            width=200,
            fg_color="green",
            hover_color="darkgreen",
            command=self.show_open_cash_dialog
        )
        open_btn.pack(pady=(20, 30))
        
        # Histórico
        history_btn = ctk.CTkButton(
            self.main_container,
            text="📋 Ver Histórico de Caixas",
            width=200,
            command=self.show_cash_history
        )
        history_btn.pack(pady=10)
    
    def show_open_cash_view(self):
        """Exibe view quando caixa está aberto"""
        
        # Obter resumo
        summary = self.cash_controller.get_cash_register_summary(self.db, self.current_cash.id)
        
        # Header com status
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", pady=(0, 20))
        
        status_frame = ctk.CTkFrame(header, fg_color="green")
        status_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="🟢 CAIXA ABERTO",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(padx=20, pady=10)
        
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Abertura: {self.current_cash.opening_date.strftime('%d/%m/%Y %H:%M')}",
            font=("Arial", 12)
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Operador: {self.user_data['full_name']}",
            font=("Arial", 12)
        ).pack(anchor="w")
        
        # Botões de ação no header
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Atualizar",
            width=120,
            command=self.check_cash_status
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔒 Fechar Caixa",
            width=140,
            fg_color="red",
            hover_color="darkred",
            command=self.show_close_cash_dialog
        ).pack(side="left", padx=5)
        
        # Cards de resumo
        cards_frame = ctk.CTkFrame(self.main_container)
        cards_frame.pack(fill="x", pady=10)
        
        cards = [
            ("💵 Saldo Inicial", f"R$ {self.current_cash.opening_balance:.2f}", "blue"),
            ("💰 Total Vendas", f"R$ {summary['total_vendas']:.2f}", "green"),
            ("📋 Comandas", f"R$ {summary['total_comanda']:.2f}", "purple"),
            ("🛎️ Balcão", f"R$ {summary['total_balcao']:.2f}", "teal"),
            ("💸 Saldo Atual", f"R$ {summary['saldo_atual']:.2f}", "orange"),
            ("🧾 Qtd Vendas", f"{summary['quantidade_vendas']}", "gray")
        ]
        
        for idx, (title, value, color) in enumerate(cards):
            card = ctk.CTkFrame(cards_frame)
            card.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")
            cards_frame.grid_columnconfigure(idx % 3, weight=1)
            
            ctk.CTkLabel(card, text=title, font=("Arial", 12)).pack(pady=(15, 5))
            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 20, "bold"),
                text_color=color
            ).pack(pady=(5, 15))
        
        # Detalhamento por forma de pagamento
        payment_frame = ctk.CTkFrame(self.main_container)
        payment_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            payment_frame,
            text="Formas de Pagamento:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        payment_grid = ctk.CTkFrame(payment_frame, fg_color="transparent")
        payment_grid.pack(fill="x", padx=10, pady=10)
        
        payments = [
            ("💵 Dinheiro", summary['total_dinheiro']),
            ("💳 Cartão", summary['total_cartao']),
            ("📱 PIX", summary['total_pix'])
        ]
        
        for idx, (name, value) in enumerate(payments):
            ctk.CTkLabel(
                payment_grid,
                text=f"{name}: R$ {value:.2f}",
                font=("Arial", 12, "bold")
            ).grid(row=0, column=idx, padx=20, pady=5)
        
        # Botões de operações
        operations_frame = ctk.CTkFrame(self.main_container)
        operations_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            operations_frame,
            text="Operações:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        btn_container = ctk.CTkFrame(operations_frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            btn_container,
            text="💸 Sangria",
            width=150,
            command=self.show_sangria_dialog
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_container,
            text="💰 Reforço",
            width=150,
            command=self.show_reforco_dialog
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_container,
            text="📜 Ver Movimentações",
            width=180,
            command=self.show_movements_dialog
        ).pack(side="left", padx=5)
    
    def show_open_cash_dialog(self):
        """Mostra diálogo de abertura de caixa"""
        dialog = OpenCashDialog(self, self.user_data)
        self.wait_window(dialog)
        self.check_cash_status()
    
    def show_close_cash_dialog(self):
        """Mostra diálogo de fechamento de caixa"""
        summary = self.cash_controller.get_cash_register_summary(self.db, self.current_cash.id)
        dialog = CloseCashDialog(self, self.current_cash, summary)
        self.wait_window(dialog)
        self.check_cash_status()
    
    def show_sangria_dialog(self):
        """Mostra diálogo de sangria"""
        dialog = SangriaDialog(self)
        self.wait_window(dialog)
        self.check_cash_status()
    
    def show_reforco_dialog(self):
        """Mostra diálogo de reforço"""
        dialog = ReforcoDialog(self)
        self.wait_window(dialog)
        self.check_cash_status()
    
    def show_movements_dialog(self):
        """Mostra diálogo de movimentações"""
        summary = self.cash_controller.get_cash_register_summary(self.db, self.current_cash.id)
        dialog = MovementsDialog(self, summary)
        self.wait_window(dialog)
    
    def show_cash_history(self):
        """Mostra histórico de caixas"""
        dialog = CashHistoryDialog(self)
        self.wait_window(dialog)


class OpenCashDialog(ctk.CTkToplevel):
    """Diálogo de abertura de caixa"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        
        self.title("Abrir Caixa")
        
        # Tamanho responsivo
        set_dialog_size(self, 'small')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="🔓 Abertura de Caixa",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame,
            text=f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=("Arial", 13)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            main_frame,
            text=f"Operador: {self.user_data['full_name']}",
            font=("Arial", 13)
        ).pack(pady=5)
        
        # Saldo inicial
        ctk.CTkLabel(
            main_frame,
            text="💵 Valor Inicial do Caixa:",
            font=("Arial", 14, "bold")
        ).pack(pady=(30, 5))
        
        self.balance_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=45,
            font=("Arial", 16),
            placeholder_text="0.00"
        )
        self.balance_entry.pack(pady=10)
        self.balance_entry.focus()
        
        # Observações
        ctk.CTkLabel(
            main_frame,
            text="📝 Observações (opcional):",
            font=("Arial", 12)
        ).pack(pady=(20, 5))
        
        self.notes_entry = ctk.CTkEntry(
            main_frame,
            width=400,
            placeholder_text="Ex: Troco de R$ 100,00"
        )
        self.notes_entry.pack(pady=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=150,
            command=self.destroy
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="✅ Abrir Caixa",
            width=180,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="green",
            hover_color="darkgreen",
            command=self.open_cash
        ).pack(side="right", padx=5)
    
    def open_cash(self):
        """Abre o caixa"""
        try:
            balance = float(self.balance_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inicial inválido!")
            return
        
        if balance < 0:
            messagebox.showerror("Erro", "O valor inicial não pode ser negativo!")
            return
        
        notes = self.notes_entry.get().strip()
        
        cash, error = self.cash_controller.open_cash_register(
            self.db,
            user_id=self.user_data['id'],
            opening_balance=balance,
            notes=notes if notes else None
        )
        
        if error:
            messagebox.showerror("Erro", error)
        else:
            messagebox.showinfo(
                "Sucesso",
                f"✅ Caixa aberto com sucesso!\n\n"
                f"Valor inicial: R$ {balance:.2f}\n"
                f"Horário: {cash.opening_date.strftime('%H:%M')}"
            )
            self.destroy()


class CloseCashDialog(ctk.CTkToplevel):
    """Diálogo de fechamento de caixa"""
    
    def __init__(self, parent, cash_register, summary):
        super().__init__(parent)
        
        self.parent = parent
        self.cash_register = cash_register
        self.summary = summary
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        
        self.title("Fechar Caixa")
        
        # Tamanho responsivo
        set_dialog_size(self, 'medium')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scroll
        scroll = ctk.CTkScrollableFrame(main_frame)
        scroll.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            scroll,
            text="🔒 Fechamento de Caixa",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 10))
        
        # Resumo do dia
        summary_frame = ctk.CTkFrame(scroll)
        summary_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            summary_frame,
            text="📊 Resumo do Dia",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        resume_data = [
            ("Abertura", f"R$ {self.cash_register.opening_balance:.2f}"),
            ("Total Vendas", f"R$ {self.summary['total_vendas']:.2f}"),
            ("Comandas", f"R$ {self.summary['total_comanda']:.2f}"),
            ("Balcão", f"R$ {self.summary['total_balcao']:.2f}"),
            ("Quantidade Vendas", f"{self.summary['quantidade_vendas']}"),
            ("Saídas/Sangrias", f"R$ {self.summary['total_saidas']:.2f}"),
            ("Saldo Esperado", f"R$ {self.summary['saldo_atual']:.2f}")
        ]
        
        for label, value in resume_data:
            row = ctk.CTkFrame(summary_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=3)
            
            ctk.CTkLabel(row, text=f"{label}:", font=("Arial", 12), anchor="w", width=150).pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Arial", 12, "bold"), anchor="e").pack(side="right")
        
        # Contagem de valores
        count_frame = ctk.CTkFrame(scroll)
        count_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            count_frame,
            text="💰 Informe os Valores no Caixa",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Campos de entrada
        self.entries = {}
        fields = [
            ("💵 Dinheiro", "cash"),
            ("💳 Cartão", "card"),
            ("📱 PIX", "pix"),
            ("🔄 Outros", "other")
        ]
        
        for label, key in fields:
            row = ctk.CTkFrame(count_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)
            
            ctk.CTkLabel(row, text=label, font=("Arial", 13), width=120, anchor="w").pack(side="left", padx=5)
            entry = ctk.CTkEntry(row, width=200, placeholder_text="0.00")
            entry.pack(side="left", padx=5)
            self.entries[key] = entry
            
            # Pré-preencher com valores esperados
            if key == "cash":
                entry.insert(0, f"{self.summary['total_dinheiro']:.2f}")
            elif key == "card":
                entry.insert(0, f"{self.summary['total_cartao']:.2f}")
            elif key == "pix":
                entry.insert(0, f"{self.summary['total_pix']:.2f}")
        
        # Total informado
        self.total_label = ctk.CTkLabel(
            count_frame,
            text="Total Informado: R$ 0,00",
            font=("Arial", 14, "bold"),
            text_color="blue"
        )
        self.total_label.pack(pady=15)
        
        # Botão calcular
        ctk.CTkButton(
            count_frame,
            text="🔢 Calcular Total",
            width=150,
            command=self.calculate_total
        ).pack(pady=5)
        
        # Observações
        ctk.CTkLabel(
            scroll,
            text="📝 Observações:",
            font=("Arial", 12)
        ).pack(pady=(10, 5))
        
        self.notes_entry = ctk.CTkEntry(scroll, width=600, placeholder_text="Observações do fechamento")
        self.notes_entry.pack(pady=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=150,
            command=self.destroy
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔒 Fechar Caixa",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="red",
            hover_color="darkred",
            command=self.close_cash
        ).pack(side="right", padx=5)
    
    def calculate_total(self):
        """Calcula total informado"""
        try:
            total = 0.0
            for entry in self.entries.values():
                value = entry.get().strip()
                if value:
                    total += float(value.replace(",", "."))
            
            self.total_label.configure(text=f"Total Informado: R$ {total:.2f}")
            
            # Mostrar diferença
            diff = total - self.summary['saldo_atual']
            if abs(diff) > 0.01:
                color = "red" if diff < 0 else "green"
                self.total_label.configure(
                    text=f"Total Informado: R$ {total:.2f} (Diferença: R$ {diff:+.2f})",
                    text_color=color
                )
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
    
    def close_cash(self):
        """Fecha o caixa"""
        try:
            total_cash = float(self.entries['cash'].get().replace(",", ".") or "0")
            total_card = float(self.entries['card'].get().replace(",", ".") or "0")
            total_pix = float(self.entries['pix'].get().replace(",", ".") or "0")
            total_other = float(self.entries['other'].get().replace(",", ".") or "0")
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
            return
        
        if not messagebox.askyesno(
            "Confirmar Fechamento",
            "⚠️ Tem certeza que deseja fechar o caixa?\n\n"
            "Esta operação não pode ser desfeita!"
        ):
            return
        
        notes = self.notes_entry.get().strip()
        
        cash, error = self.cash_controller.close_cash_register(
            self.db,
            cash_register_id=self.cash_register.id,
            total_cash=total_cash,
            total_card=total_card,
            total_pix=total_pix,
            total_other=total_other,
            notes=notes if notes else None
        )
        
        if error:
            messagebox.showerror("Erro", error)
        else:
            diff_msg = ""
            if abs(cash.difference) > 0.01:
                diff_msg = f"\n\n⚠️ Diferença: R$ {cash.difference:+.2f}"
                if cash.difference < 0:
                    diff_msg += "\n(Falta no caixa)"
                else:
                    diff_msg += "\n(Sobra no caixa)"
            
            messagebox.showinfo(
                "Sucesso",
                f"✅ Caixa fechado com sucesso!\n\n"
                f"Saldo Esperado: R$ {cash.expected_balance:.2f}\n"
                f"Saldo Informado: R$ {cash.closing_balance:.2f}"
                f"{diff_msg}"
            )
            self.destroy()


class SangriaDialog(ctk.CTkToplevel):
    """Diálogo de sangria"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        
        self.title("Sangria")
        
        # Tamanho responsivo
        set_dialog_size(self, 'small')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="💸 Sangria",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame,
            text="Valor:",
            font=("Arial", 13)
        ).pack(pady=5)
        
        self.amount_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=40,
            placeholder_text="0.00"
        )
        self.amount_entry.pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="Motivo:",
            font=("Arial", 13)
        ).pack(pady=5)
        
        self.desc_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            placeholder_text="Ex: Pagamento fornecedor"
        )
        self.desc_entry.pack(pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=130,
            command=self.destroy
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💸 Confirmar Sangria",
            width=180,
            fg_color="red",
            hover_color="darkred",
            command=self.confirm_sangria
        ).pack(side="right", padx=5)
    
    def confirm_sangria(self):
        """Confirma sangria"""
        try:
            amount = float(self.amount_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
            return
        
        if amount <= 0:
            messagebox.showerror("Erro", "O valor deve ser maior que zero!")
            return
        
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showerror("Erro", "Informe o motivo da sangria!")
            return
        
        movement, error = self.cash_controller.add_sangria(self.db, amount, description)
        
        if error:
            messagebox.showerror("Erro", error)
        else:
            messagebox.showinfo("Sucesso", f"Sangria de R$ {amount:.2f} registrada!")
            self.destroy()


class ReforcoDialog(ctk.CTkToplevel):
    """Diálogo de reforço"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        
        self.title("Reforço de Caixa")
        
        # Tamanho responsivo
        set_dialog_size(self, 'small')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="💰 Reforço de Caixa",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame,
            text="Valor:",
            font=("Arial", 13)
        ).pack(pady=5)
        
        self.amount_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=40,
            placeholder_text="0.00"
        )
        self.amount_entry.pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="Motivo:",
            font=("Arial", 13)
        ).pack(pady=5)
        
        self.desc_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            placeholder_text="Ex: Troco adicional"
        )
        self.desc_entry.pack(pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=130,
            command=self.destroy
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💰 Confirmar Reforço",
            width=180,
            fg_color="green",
            hover_color="darkgreen",
            command=self.confirm_reforco
        ).pack(side="right", padx=5)
    
    def confirm_reforco(self):
        """Confirma reforço"""
        try:
            amount = float(self.amount_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
            return
        
        if amount <= 0:
            messagebox.showerror("Erro", "O valor deve ser maior que zero!")
            return
        
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showerror("Erro", "Informe o motivo do reforço!")
            return
        
        movement, error = self.cash_controller.add_reforco(self.db, amount, description)
        
        if error:
            messagebox.showerror("Erro", error)
        else:
            messagebox.showinfo("Sucesso", f"Reforço de R$ {amount:.2f} registrado!")
            self.destroy()


class MovementsDialog(ctk.CTkToplevel):
    """Diálogo de movimentações"""
    
    def __init__(self, parent, summary):
        super().__init__(parent)
        
        self.summary = summary
        
        self.title("Movimentações do Caixa")
        
        # Tamanho responsivo
        set_dialog_size(self, 'large')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📜 Movimentações do Caixa",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))
        
        # Tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure("Cash.Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       font=("Arial", 10))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            table_frame,
            columns=("Hora", "Tipo", "Descrição", "Valor"),
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Cash.Treeview"
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading("Hora", text="Hora")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Valor", text="Valor")
        
        tree.column("Hora", width=150, anchor="center")
        tree.column("Tipo", width=150, anchor="center")
        tree.column("Descrição", width=400)
        tree.column("Valor", width=150, anchor="center")
        
        for mov in self.summary['movements']:
            color = "green" if mov.movement_type in ["entrada", "reforco"] else "red"
            valor = f"R$ {mov.amount:.2f}"
            if mov.movement_type in ["saida", "sangria"]:
                valor = f"-{valor}"
            
            tree.insert("", "end", values=(
                mov.created_at.strftime("%H:%M:%S"),
                mov.movement_type.upper(),
                mov.description,
                valor
            ))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão fechar
        ctk.CTkButton(
            self,
            text="Fechar",
            width=150,
            command=self.destroy
        ).pack(pady=20)


class CashHistoryDialog(ctk.CTkToplevel):
    """Diálogo de histórico de caixas"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.cash_controller = CashRegisterController()
        self.db = SessionLocal()
        
        self.title("Histórico de Caixas")
        
        # Tamanho responsivo
        set_dialog_size(self, 'extra-large')
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.load_history()
    
    def create_widgets(self):
        """Cria widgets"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📋 Histórico de Caixas",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))
        
        # Tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Data", "Abertura", "Fechamento", "Vendas", "Diferença", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("Data", text="Data")
        self.tree.heading("Abertura", text="Abertura")
        self.tree.heading("Fechamento", text="Fechamento")
        self.tree.heading("Vendas", text="Total Vendas")
        self.tree.heading("Diferença", text="Diferença")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Data", width=150, anchor="center")
        self.tree.column("Abertura", width=120, anchor="center")
        self.tree.column("Fechamento", width=120, anchor="center")
        self.tree.column("Vendas", width=120, anchor="center")
        self.tree.column("Diferença", width=120, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão fechar
        ctk.CTkButton(
            self,
            text="Fechar",
            width=150,
            command=self.destroy
        ).pack(pady=20)
    
    def load_history(self):
        """Carrega histórico"""
        registers = self.cash_controller.list_cash_registers(self.db, limit=100)
        
        for reg in registers:
            self.tree.insert("", "end", values=(
                reg.opening_date.strftime("%d/%m/%Y"),
                f"R$ {reg.opening_balance:.2f}",
                f"R$ {reg.closing_balance:.2f}" if reg.closing_balance else "-",
                f"R$ {reg.total_sales:.2f}" if reg.total_sales else "R$ 0,00",
                f"R$ {reg.difference:+.2f}" if reg.difference else "-",
                "ABERTO" if reg.is_open else "FECHADO"
            ))
