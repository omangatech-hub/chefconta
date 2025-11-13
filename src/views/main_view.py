"""
View Principal
Tela principal do sistema com menu e conteúdo
"""
import customtkinter as ctk
from tkinter import messagebox
from src.views.products_view import ProductsView
from src.views.sales_view import SalesView
from src.views.expenses_view import ExpensesView
from src.views.purchases_view import PurchasesView
from src.views.reports_view import ReportsView
from src.views.settings_view import SettingsView
from src.views.cash_register_view import CashRegisterView
from src.utils.modern_theme import COLORS, create_colored_card, create_info_card

class MainView(ctk.CTkFrame):
    """Tela principal do sistema"""
    
    def __init__(self, parent, user_data, on_logout):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela principal"""
        
        # Layout: Sidebar + Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Criar sidebar
        self.create_sidebar()
        
        # Criar área de conteúdo
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Mostrar dashboard por padrão
        self.show_dashboard()
    
    def create_sidebar(self):
        """Cria o menu lateral"""
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=COLORS['sidebar_bg'])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo/Título
        logo_label = ctk.CTkLabel(
            sidebar,
            text="🍳 ChefConta",
            font=("Arial", 26, "bold"),
            text_color=COLORS['sidebar_text']
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            sidebar,
            text="Gestão Financeira",
            font=("Arial", 11),
            text_color=COLORS['sidebar_text_secondary']
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Info do usuário
        user_frame = ctk.CTkFrame(sidebar, fg_color=COLORS['sidebar_hover'], corner_radius=8)
        user_frame.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")
        
        ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.user_data['full_name']}",
            font=("Arial", 12, "bold"),
            text_color=COLORS['sidebar_text']
        ).pack(pady=(12, 2))
        
        ctk.CTkLabel(
            user_frame,
            text=f"{self.user_data['role'].upper()}",
            font=("Arial", 10),
            text_color=COLORS['sidebar_text_secondary']
        ).pack(pady=(0, 12))
        
        # Botões do menu
        menu_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("💰 Caixa", self.show_cash_register),
            ("🛒 Vendas", self.show_sales),
            ("📦 Produtos", self.show_products),
            ("💸 Despesas", self.show_expenses),
            ("🛍️ Compras", self.show_purchases),
            ("📈 Relatórios", self.show_reports),
        ]
        
        # Adicionar configurações apenas para admin
        if self.user_data['role'] == 'admin':
            menu_buttons.append(("⚙️ Configurações", self.show_settings))
        
        for idx, (text, command) in enumerate(menu_buttons, start=3):
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 13),
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS['sidebar_hover'],
                text_color=COLORS['sidebar_text'],
                corner_radius=8,
                command=command
            )
            btn.grid(row=idx, column=0, padx=15, pady=3, sticky="ew")
        
        # Botão de logout (sempre no final)
        logout_btn = ctk.CTkButton(
            sidebar,
            text="🚪 Sair",
            font=("Arial", 13),
            height=45,
            fg_color=COLORS['danger'],
            hover_color=COLORS['danger_hover'],
            text_color=COLORS['text_white'],
            corner_radius=8,
            command=self.perform_logout
        )
        logout_btn.grid(row=11, column=0, padx=15, pady=(10, 20), sticky="ew")
    
    def clear_content(self):
        """Limpa a área de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Exibe o dashboard"""
        self.clear_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=("Arial", 32, "bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Visão geral do mês atual",
            font=("Arial", 14),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(side="left", padx=(15, 0), pady=(8, 0))
        
        # Cards coloridos em grid
        cards_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 30))
        
        # Configurar grid
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card 1 - Vendas (Verde)
        card1 = create_colored_card(
            cards_frame,
            "Vendas do Mês",
            "R$ 0,00",
            "Total de vendas",
            COLORS['success'],
            "📈"
        )
        card1.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        
        # Card 2 - Despesas (Laranja)
        card2 = create_colored_card(
            cards_frame,
            "Despesas do Mês",
            "R$ 0,00",
            "Total de despesas",
            COLORS['warning'],
            "💸"
        )
        card2.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        # Card 3 - Saldo (Azul)
        card3 = create_colored_card(
            cards_frame,
            "Saldo do Mês",
            "R$ 0,00",
            "Saldo positivo",
            COLORS['info'],
            "💰"
        )
        card3.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")
        
        # Card 4 - Estoque (Cinza)
        card4 = create_colored_card(
            cards_frame,
            "Estoque Baixo",
            "0",
            "Produtos em alerta",
            COLORS['secondary'],
            "📦"
        )
        card4.grid(row=0, column=3, padx=8, pady=8, sticky="nsew")
        
        # Card de resumo financeiro
        summary_card = create_info_card(self.content_frame, "Resumo Financeiro")
        summary_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Conteúdo do resumo
        summary_content = ctk.CTkFrame(summary_card, fg_color="transparent")
        summary_content.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        # Linha 1
        row1 = ctk.CTkFrame(summary_content, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            row1,
            text="Total de Vendas",
            font=("Arial", 14),
            text_color=COLORS['text_secondary']
        ).pack(side="left")
        
        ctk.CTkLabel(
            row1,
            text="+ R$ 0,00",
            font=("Arial", 14, "bold"),
            text_color=COLORS['success']
        ).pack(side="right")
        
        # Linha 2
        row2 = ctk.CTkFrame(summary_content, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            row2,
            text="Total de Despesas",
            font=("Arial", 14),
            text_color=COLORS['text_secondary']
        ).pack(side="left")
        
        ctk.CTkLabel(
            row2,
            text="- R$ 0,00",
            font=("Arial", 14, "bold"),
            text_color=COLORS['danger']
        ).pack(side="right")
        
        # Separador
        separator = ctk.CTkFrame(summary_content, height=2, fg_color=COLORS['border_light'])
        separator.pack(fill="x", pady=15)
        
        # Linha 3 - Saldo Final
        row3 = ctk.CTkFrame(summary_content, fg_color="transparent")
        row3.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            row3,
            text="Saldo Final",
            font=("Arial", 16, "bold"),
            text_color=COLORS['text_primary']
        ).pack(side="left")
        
        ctk.CTkLabel(
            row3,
            text="R$ 0,00",
            font=("Arial", 16, "bold"),
            text_color=COLORS['success']
        ).pack(side="right")
    
    def show_cash_register(self):
        """Exibe a tela de caixa"""
        self.clear_content()
        cash_view = CashRegisterView(self.content_frame, self.user_data)
        cash_view.pack(fill="both", expand=True)
    
    def show_sales(self):
        """Exibe a tela de vendas"""
        self.clear_content()
        sales_view = SalesView(self.content_frame, self.user_data)
        sales_view.pack(fill="both", expand=True)
    
    def show_products(self):
        """Exibe a tela de produtos"""
        self.clear_content()
        products_view = ProductsView(self.content_frame)
        products_view.pack(fill="both", expand=True)
    
    def show_expenses(self):
        """Exibe a tela de despesas"""
        self.clear_content()
        expenses_view = ExpensesView(self.content_frame, self.user_data)
        expenses_view.pack(fill="both", expand=True)
    
    def show_purchases(self):
        """Exibe a tela de compras"""
        self.clear_content()
        purchases_view = PurchasesView(self.content_frame, self.user_data)
        purchases_view.pack(fill="both", expand=True)
    
    def show_reports(self):
        """Exibe a tela de relatórios"""
        self.clear_content()
        reports_view = ReportsView(self.content_frame, self.user_data)
        reports_view.pack(fill="both", expand=True)
    
    def show_settings(self):
        """Exibe a tela de configurações"""
        self.clear_content()
        settings_view = SettingsView(self.content_frame, self.user_data)
        settings_view.pack(fill="both", expand=True)
    
    def create_placeholder(self, title, message):
        """Cria um placeholder para telas em desenvolvimento"""
        title_label = ctk.CTkLabel(
            self.content_frame,
            text=title,
            font=("Arial", 28, "bold")
        )
        title_label.pack(pady=20, anchor="w")
        
        message_label = ctk.CTkLabel(
            self.content_frame,
            text=message,
            font=("Arial", 16),
            text_color="gray"
        )
        message_label.pack(pady=40)
    
    def perform_logout(self):
        """Realiza o logout"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            from src.controllers.auth_controller import AuthController
            auth = AuthController()
            auth.logout()
            self.on_logout()
