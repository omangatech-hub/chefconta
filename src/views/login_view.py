"""
View de Login
Tela de autenticação do sistema
"""
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.auth_controller import AuthController
from src.models.database import SessionLocal

class LoginView(ctk.CTkFrame):
    """Tela de login"""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        
        self.parent = parent
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela de login"""
        
        # Container central
        login_container = ctk.CTkFrame(self, fg_color="transparent")
        login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            login_container,
            text="🍳 ChefConta",
            font=("Arial", 42, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            login_container,
            text="Sistema de Gestão Financeira",
            font=("Arial", 16)
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(login_container)
        form_frame.pack(padx=40, pady=20)
        
        # Campo de usuário
        ctk.CTkLabel(
            form_frame,
            text="Usuário:",
            font=("Arial", 14)
        ).pack(pady=(20, 5), padx=40, anchor="w")
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Digite seu usuário"
        )
        self.username_entry.pack(padx=40, pady=(0, 15))
        
        # Campo de senha
        ctk.CTkLabel(
            form_frame,
            text="Senha:",
            font=("Arial", 14)
        ).pack(pady=(5, 5), padx=40, anchor="w")
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Digite sua senha",
            show="●"
        )
        self.password_entry.pack(padx=40, pady=(0, 25))
        
        # Botão de login
        login_button = ctk.CTkButton(
            form_frame,
            text="Entrar",
            width=300,
            height=45,
            font=("Arial", 16, "bold"),
            command=self.perform_login
        )
        login_button.pack(padx=40, pady=(10, 30))
        
        # Bind Enter para fazer login
        self.password_entry.bind("<Return>", lambda e: self.perform_login())
        
        # Informação de primeiro acesso
        info_label = ctk.CTkLabel(
            login_container,
            text="Primeiro acesso? Usuário: admin | Senha: admin123",
            font=("Arial", 11),
            text_color="gray"
        )
        info_label.pack(pady=(20, 0))
    
    def perform_login(self):
        """Realiza o login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Por favor, preencha usuário e senha."
            )
            return
        
        # Tentar fazer login
        db = SessionLocal()
        try:
            user_data = self.auth_controller.login(db, username, password)
            
            if user_data:
                messagebox.showinfo(
                    "Login bem-sucedido",
                    f"Bem-vindo(a), {user_data['full_name']}!"
                )
                self.on_login_success(user_data)
            else:
                messagebox.showerror(
                    "Erro de login",
                    "Usuário ou senha incorretos."
                )
                self.password_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao realizar login: {str(e)}"
            )
        finally:
            db.close()
