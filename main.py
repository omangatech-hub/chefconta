"""
ChefConta - Sistema de Gestão Financeira
Aplicação Principal
"""
import customtkinter as ctk
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.models.database import create_tables
from src.utils.window_utils import maximize_window
import sys

# Configurar aparência do CustomTkinter - Tema Claro Moderno
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ChefContaApp(ctk.CTk):
    """Aplicação principal do ChefConta"""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("ChefConta - Sistema de Gestão Financeira")
        
        # Inicializar banco de dados
        create_tables()
        
        # Variável para armazenar usuário atual
        self.current_user = None
        
        # Mostrar tela de login
        self.show_login()
        
        # Maximizar janela após criar widgets
        self.after(100, lambda: maximize_window(self))
    
    def show_login(self):
        """Exibe a tela de login"""
        # Limpar widgets existentes
        for widget in self.winfo_children():
            widget.destroy()
        
        # Criar e exibir tela de login
        login_view = LoginView(self, self.on_login_success)
        login_view.pack(fill="both", expand=True)
    
    def on_login_success(self, user_data):
        """Callback executado quando o login é bem-sucedido"""
        self.current_user = user_data
        self.show_main_view()
    
    def show_main_view(self):
        """Exibe a tela principal do sistema"""
        # Limpar widgets existentes
        for widget in self.winfo_children():
            widget.destroy()
        
        # Criar e exibir tela principal
        main_view = MainView(self, self.current_user, self.on_logout)
        main_view.pack(fill="both", expand=True)
    
    def on_logout(self):
        """Callback executado quando o usuário faz logout"""
        self.current_user = None
        self.show_login()

def main():
    """Função principal"""
    try:
        app = ChefContaApp()
        app.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
