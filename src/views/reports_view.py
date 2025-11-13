"""
View de Relatórios
Tela de geração e visualização de relatórios
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
from src.utils.report_generator import ReportGenerator
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size

class ReportsView(ctk.CTkFrame):
    """Tela de relatórios"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.report_generator = ReportGenerator()
        self.db = SessionLocal()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="📈 Relatórios",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cards de relatórios
        cards = [
            {
                'title': '📊 Relatório de Vendas',
                'description': 'Análise completa das vendas por período, produtos mais vendidos, ticket médio',
                'type': 'sales',
                'icon': '📊',
                'color': 'green'
            },
            {
                'title': '💸 Relatório de Despesas',
                'description': 'Controle de despesas por categoria, status de pagamento, vencimentos',
                'type': 'expenses',
                'icon': '💸',
                'color': 'red'
            },
            {
                'title': '💰 Relatório Financeiro',
                'description': 'Resumo financeiro: receitas, despesas, lucro, fluxo de caixa',
                'type': 'financial',
                'icon': '💰',
                'color': 'blue'
            },
            {
                'title': '📦 Relatório de Estoque',
                'description': 'Análise de estoque: produtos em baixa, movimentações, valor total',
                'type': 'stock',
                'icon': '📦',
                'color': 'orange'
            },
            {
                'title': '🛍️ Relatório de Compras',
                'description': 'Histórico de compras, fornecedores, análise de custos',
                'type': 'purchases',
                'icon': '🛍️',
                'color': 'purple'
            },
            {
                'title': '👥 Relatório de Clientes',
                'description': 'Análise de clientes: vendas por cliente, frequência, ticket médio',
                'type': 'customers',
                'icon': '👥',
                'color': 'teal'
            }
        ]
        
        # Grid de cards (2 colunas)
        for idx, card_info in enumerate(cards):
            row = idx // 2
            col = idx % 2
            
            card = self.create_report_card(main_frame, card_info)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            main_frame.grid_columnconfigure(col, weight=1)
            main_frame.grid_rowconfigure(row, weight=1)
    
    def create_report_card(self, parent, card_info):
        """Cria um card de relatório"""
        
        card_frame = ctk.CTkFrame(parent)
        
        # Header
        header = ctk.CTkFrame(card_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header,
            text=card_info['icon'],
            font=("Arial", 32)
        ).pack(side="left", padx=(0, 10))
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text=card_info['title'],
            font=("Arial", 16, "bold"),
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text=card_info['description'],
            font=("Arial", 11),
            text_color="gray",
            anchor="w",
            wraplength=300
        ).pack(anchor="w", pady=(5, 0))
        
        # Botão gerar
        btn = ctk.CTkButton(
            card_frame,
            text="📄 Gerar Relatório",
            font=("Arial", 13, "bold"),
            height=40,
            fg_color=card_info['color'],
            hover_color=self.darken_color(card_info['color']),
            command=lambda t=card_info['type']: self.open_report_dialog(t)
        )
        btn.pack(fill="x", padx=20, pady=(10, 20))
        
        return card_frame
    
    def darken_color(self, color):
        """Escurece uma cor para efeito hover"""
        color_map = {
            'green': 'darkgreen',
            'red': 'darkred',
            'blue': 'darkblue',
            'orange': 'darkorange',
            'purple': 'darkviolet',
            'teal': 'darkcyan'
        }
        return color_map.get(color, 'gray')
    
    def open_report_dialog(self, report_type):
        """Abre diálogo de configuração do relatório"""
        dialog = ReportConfigDialog(self, report_type)
        self.wait_window(dialog)


class ReportConfigDialog(ctk.CTkToplevel):
    """Diálogo de configuração de relatório"""
    
    def __init__(self, parent, report_type):
        super().__init__(parent)
        
        self.parent = parent
        self.report_type = report_type
        self.report_generator = ReportGenerator()
        self.db = SessionLocal()
        
        # Configurar janela
        self.title(f"Configurar Relatório - {self.get_report_name()}")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'medium', maximized=True)
        
        self.create_widgets()
    
    def get_report_name(self):
        """Retorna o nome do relatório"""
        names = {
            'sales': 'Vendas',
            'expenses': 'Despesas',
            'financial': 'Financeiro',
            'stock': 'Estoque',
            'purchases': 'Compras',
            'customers': 'Clientes'
        }
        return names.get(self.report_type, 'Relatório')
    
    def create_widgets(self):
        """Cria widgets do diálogo"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"📈 Relatório de {self.get_report_name()}",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 20))
        
        # Período
        period_frame = ctk.CTkFrame(main_frame)
        period_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            period_frame,
            text="📅 Período:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        # Opções de período
        self.period_var = ctk.StringVar(value="month")
        
        periods = [
            ("Hoje", "today"),
            ("Esta Semana", "week"),
            ("Este Mês", "month"),
            ("Últimos 30 dias", "30days"),
            ("Últimos 90 dias", "90days"),
            ("Este Ano", "year"),
            ("Personalizado", "custom")
        ]
        
        for text, value in periods:
            ctk.CTkRadioButton(
                period_frame,
                text=text,
                variable=self.period_var,
                value=value,
                font=("Arial", 12),
                command=self.on_period_change
            ).pack(anchor="w", padx=20, pady=2)
        
        # Frame de datas personalizadas (inicialmente oculto)
        self.custom_frame = ctk.CTkFrame(main_frame)
        
        dates_row = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
        dates_row.pack(fill="x", pady=10)
        
        # Data inicial
        ctk.CTkLabel(dates_row, text="De:", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="w")
        self.start_date_entry = ctk.CTkEntry(dates_row, width=150, placeholder_text="DD/MM/AAAA")
        self.start_date_entry.grid(row=0, column=1, padx=5)
        self.start_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y"))
        
        # Data final
        ctk.CTkLabel(dates_row, text="Até:", font=("Arial", 12)).grid(row=0, column=2, padx=5, sticky="w")
        self.end_date_entry = ctk.CTkEntry(dates_row, width=150, placeholder_text="DD/MM/AAAA")
        self.end_date_entry.grid(row=0, column=3, padx=5)
        self.end_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Opções adicionais (conforme tipo de relatório)
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=15)
        
        ctk.CTkLabel(
            options_frame,
            text="⚙️ Opções:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        # Opções específicas por tipo
        self.create_specific_options(options_frame)
        
        # Formato
        format_frame = ctk.CTkFrame(main_frame)
        format_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(format_frame, text="📄 Formato:", font=("Arial", 12)).pack(side="left", padx=10)
        
        self.format_var = ctk.StringVar(value="pdf")
        ctk.CTkRadioButton(format_frame, text="PDF", variable=self.format_var, value="pdf").pack(side="left", padx=5)
        ctk.CTkRadioButton(format_frame, text="Excel", variable=self.format_var, value="excel").pack(side="left", padx=5)
        
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
        
        generate_btn = ctk.CTkButton(
            btn_frame,
            text="✅ Gerar Relatório",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="blue",
            hover_color="darkblue",
            command=self.generate_report
        )
        generate_btn.pack(side="right", padx=5)
    
    def create_specific_options(self, parent):
        """Cria opções específicas por tipo de relatório"""
        
        if self.report_type == 'sales':
            self.group_by_var = ctk.StringVar(value="day")
            ctk.CTkRadioButton(parent, text="Agrupar por Dia", variable=self.group_by_var, value="day").pack(anchor="w", padx=20, pady=2)
            ctk.CTkRadioButton(parent, text="Agrupar por Produto", variable=self.group_by_var, value="product").pack(anchor="w", padx=20, pady=2)
            ctk.CTkRadioButton(parent, text="Agrupar por Cliente", variable=self.group_by_var, value="customer").pack(anchor="w", padx=20, pady=2)
        
        elif self.report_type == 'expenses':
            self.filter_status_var = ctk.StringVar(value="all")
            ctk.CTkRadioButton(parent, text="Todas as Despesas", variable=self.filter_status_var, value="all").pack(anchor="w", padx=20, pady=2)
            ctk.CTkRadioButton(parent, text="Apenas Pagas", variable=self.filter_status_var, value="paid").pack(anchor="w", padx=20, pady=2)
            ctk.CTkRadioButton(parent, text="Apenas Pendentes", variable=self.filter_status_var, value="pending").pack(anchor="w", padx=20, pady=2)
        
        elif self.report_type == 'stock':
            self.include_movements_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(parent, text="Incluir movimentações de estoque", variable=self.include_movements_var).pack(anchor="w", padx=20, pady=2)
            
            self.low_stock_only_var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(parent, text="Apenas produtos em baixa", variable=self.low_stock_only_var).pack(anchor="w", padx=20, pady=2)
    
    def on_period_change(self):
        """Mostra/oculta datas personalizadas"""
        if self.period_var.get() == "custom":
            self.custom_frame.pack(fill="x", pady=10)
        else:
            self.custom_frame.pack_forget()
    
    def get_date_range(self):
        """Retorna o intervalo de datas selecionado"""
        period = self.period_var.get()
        today = datetime.now()
        
        if period == "today":
            start_date = today.replace(hour=0, minute=0, second=0)
            end_date = today
        elif period == "week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif period == "month":
            start_date = today.replace(day=1)
            end_date = today
        elif period == "30days":
            start_date = today - timedelta(days=30)
            end_date = today
        elif period == "90days":
            start_date = today - timedelta(days=90)
            end_date = today
        elif period == "year":
            start_date = today.replace(month=1, day=1)
            end_date = today
        elif period == "custom":
            try:
                start_date = datetime.strptime(self.start_date_entry.get(), "%d/%m/%Y")
                end_date = datetime.strptime(self.end_date_entry.get(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
                return None, None
        else:
            start_date = today - timedelta(days=30)
            end_date = today
        
        return start_date, end_date
    
    def generate_report(self):
        """Gera o relatório"""
        
        start_date, end_date = self.get_date_range()
        if not start_date or not end_date:
            return
        
        if start_date > end_date:
            messagebox.showerror("Erro", "A data inicial não pode ser maior que a data final!")
            return
        
        # Escolher local para salvar
        default_filename = f"relatorio_{self.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if self.format_var.get() == "pdf":
            default_filename += ".pdf"
            filetypes = [("PDF files", "*.pdf")]
        else:
            default_filename += ".xlsx"
            filetypes = [("Excel files", "*.xlsx")]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=filetypes[0][1],
            filetypes=filetypes,
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        try:
            # Gerar relatório conforme tipo
            if self.report_type == 'sales':
                self.report_generator.generate_sales_report(
                    self.db,
                    start_date,
                    end_date,
                    filepath
                )
            elif self.report_type == 'expenses':
                # Implementar
                messagebox.showinfo("Info", "Relatório de despesas será implementado em breve")
                return
            elif self.report_type == 'financial':
                self.report_generator.generate_financial_report(
                    self.db,
                    start_date,
                    end_date,
                    filepath
                )
            elif self.report_type == 'stock':
                # Implementar
                messagebox.showinfo("Info", "Relatório de estoque será implementado em breve")
                return
            else:
                messagebox.showinfo("Info", f"Relatório de {self.get_report_name()} será implementado em breve")
                return
            
            messagebox.showinfo(
                "Sucesso",
                f"Relatório gerado com sucesso!\n\nArquivo: {filepath}"
            )
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
