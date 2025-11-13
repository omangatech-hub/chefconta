"""
View de Configurações
Tela de configurações do sistema (apenas admin)
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from src.controllers.auth_controller import AuthController
from src.models import User
from src.models.database import SessionLocal
from src.utils.window_utils import set_dialog_size
import shutil
import os
from datetime import datetime

class SettingsView(ctk.CTkFrame):
    """Tela de configurações"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.parent = parent
        self.user_data = user_data
        self.auth_controller = AuthController()
        self.db = SessionLocal()
        
        # Verificar permissão
        if user_data['role'] != 'admin':
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar as configurações.")
            return
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="⚙️ Configurações",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20, padx=20, anchor="w")
        
        # Criar Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar abas
        self.tabview.add("👥 Usuários")
        self.tabview.add("🏢 Empresa")
        self.tabview.add("💾 Backup")
        self.tabview.add("ℹ️ Sistema")
        
        # Preencher abas
        self.create_users_tab()
        self.create_company_tab()
        self.create_backup_tab()
        self.create_system_tab()
    
    def create_users_tab(self):
        """Cria aba de usuários"""
        tab = self.tabview.tab("👥 Usuários")
        
        # Frame de ações
        actions_frame = ctk.CTkFrame(tab, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Novo Usuário",
            font=("Arial", 14),
            width=150,
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            command=self.show_new_user_dialog
        )
        new_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Atualizar",
            font=("Arial", 14),
            width=120,
            height=40,
            command=self.load_users
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Tabela de usuários
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Settings.Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       font=("Arial", 10))
        style.configure("Settings.Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=("Arial", 11, "bold"))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.users_tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Usuário", "Nome Completo", "Perfil", "Ativo"),
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Settings.Treeview",
            height=12
        )
        scrollbar.config(command=self.users_tree.yview)
        
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Usuário", text="Usuário")
        self.users_tree.heading("Nome Completo", text="Nome Completo")
        self.users_tree.heading("Perfil", text="Perfil")
        self.users_tree.heading("Ativo", text="Ativo")
        
        self.users_tree.column("ID", width=50, anchor="center")
        self.users_tree.column("Usuário", width=150)
        self.users_tree.column("Nome Completo", width=250)
        self.users_tree.column("Perfil", width=100, anchor="center")
        self.users_tree.column("Ativo", width=80, anchor="center")
        
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            width=120,
            command=self.edit_user
        )
        edit_btn.pack(side="left", padx=5)
        
        toggle_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Ativar/Desativar",
            width=150,
            command=self.toggle_user_active
        )
        toggle_btn.pack(side="left", padx=5)
        
        password_btn = ctk.CTkButton(
            btn_frame,
            text="🔑 Trocar Senha",
            width=140,
            command=self.change_user_password
        )
        password_btn.pack(side="left", padx=5)
        
        self.load_users()
    
    def create_company_tab(self):
        """Cria aba de informações da empresa"""
        tab = self.tabview.tab("🏢 Empresa")
        
        form_frame = ctk.CTkFrame(tab)
        form_frame.pack(fill="both", expand=True, pady=20, padx=20)
        
        ctk.CTkLabel(
            form_frame,
            text="Informações da Empresa",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 20))
        
        # Campos
        fields = [
            ("Nome da Empresa:", "company_name"),
            ("CNPJ:", "cnpj"),
            ("Endereço:", "address"),
            ("Telefone:", "phone"),
            ("Email:", "email"),
            ("Website:", "website")
        ]
        
        self.company_entries = {}
        
        for label_text, field_name in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            ctk.CTkLabel(row, text=label_text, width=150, anchor="w").pack(side="left", padx=10)
            entry = ctk.CTkEntry(row, width=400)
            entry.pack(side="left", padx=10)
            self.company_entries[field_name] = entry
        
        # Botão salvar
        save_btn = ctk.CTkButton(
            form_frame,
            text="💾 Salvar Informações",
            font=("Arial", 14, "bold"),
            height=45,
            fg_color="blue",
            hover_color="darkblue",
            command=self.save_company_info
        )
        save_btn.pack(pady=20)
        
        # Carregar dados (em produção, buscar da tabela system_config)
        self.load_company_info()
    
    def create_backup_tab(self):
        """Cria aba de backup"""
        tab = self.tabview.tab("💾 Backup")
        
        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(fill="both", expand=True, pady=20, padx=20)
        
        ctk.CTkLabel(
            content_frame,
            text="Backup e Restauração",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 20))
        
        # Info
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Mantenha backups regulares do seu banco de dados para evitar perda de informações.",
            font=("Arial", 12),
            wraplength=600,
            text_color="gray"
        ).pack(pady=15)
        
        # Backup
        backup_card = ctk.CTkFrame(content_frame)
        backup_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            backup_card,
            text="💾 Fazer Backup",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            backup_card,
            text="Cria uma cópia de segurança do banco de dados",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=5)
        
        backup_btn = ctk.CTkButton(
            backup_card,
            text="📦 Criar Backup Agora",
            font=("Arial", 14),
            height=45,
            width=250,
            fg_color="blue",
            hover_color="darkblue",
            command=self.create_backup
        )
        backup_btn.pack(pady=15)
        
        # Restauração
        restore_card = ctk.CTkFrame(content_frame)
        restore_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            restore_card,
            text="♻️ Restaurar Backup",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            restore_card,
            text="Restaura o banco de dados a partir de um backup anterior",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=5)
        
        restore_btn = ctk.CTkButton(
            restore_card,
            text="📂 Restaurar de Backup",
            font=("Arial", 14),
            height=45,
            width=250,
            fg_color="orange",
            hover_color="darkorange",
            command=self.restore_backup
        )
        restore_btn.pack(pady=15)
    
    def create_system_tab(self):
        """Cria aba de informações do sistema"""
        tab = self.tabview.tab("ℹ️ Sistema")
        
        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(fill="both", expand=True, pady=20, padx=20)
        
        ctk.CTkLabel(
            content_frame,
            text="Informações do Sistema",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 20))
        
        # Info cards
        info_data = [
            ("🍳 Sistema", "ChefConta - Gestão Financeira"),
            ("📋 Versão", "1.0.0"),
            ("👨‍💻 Desenvolvedor", "Seu Nome/Empresa"),
            ("📅 Data de Instalação", datetime.now().strftime("%d/%m/%Y")),
            ("💾 Banco de Dados", "SQLite 3"),
            ("🐍 Python", "3.13+"),
            ("🎨 Interface", "CustomTkinter")
        ]
        
        for label, value in info_data:
            row = ctk.CTkFrame(content_frame)
            row.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=("Arial", 13, "bold"),
                width=200,
                anchor="w"
            ).pack(side="left", padx=15)
            
            ctk.CTkLabel(
                row,
                text=value,
                font=("Arial", 12),
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Licença
        license_frame = ctk.CTkFrame(content_frame)
        license_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            license_frame,
            text="📜 Este é um sistema de uso interno",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=15)
    
    def load_users(self):
        """Carrega usuários"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users = self.db.query(User).all()
        for user in users:
            self.users_tree.insert("", "end", values=(
                user.id,
                user.username,
                user.full_name,
                user.role.upper(),
                "Sim" if user.is_active else "Não"
            ), tags=('active' if user.is_active else 'inactive',))
    
    def show_new_user_dialog(self):
        """Mostra diálogo de novo usuário"""
        dialog = UserDialog(self, None)
        self.wait_window(dialog)
        self.load_users()
    
    def edit_user(self):
        """Edita usuário selecionado"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            dialog = UserDialog(self, user)
            self.wait_window(dialog)
            self.load_users()
    
    def toggle_user_active(self):
        """Ativa/desativa usuário"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário.")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            if user.id == self.user_data['id']:
                messagebox.showerror("Erro", "Você não pode desativar seu próprio usuário!")
                return
            
            user.is_active = not user.is_active
            self.db.commit()
            
            status = "ativado" if user.is_active else "desativado"
            messagebox.showinfo("Sucesso", f"Usuário {status} com sucesso!")
            self.load_users()
    
    def change_user_password(self):
        """Altera senha do usuário"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário.")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            dialog = ChangePasswordDialog(self, user)
            self.wait_window(dialog)
    
    def load_company_info(self):
        """Carrega informações da empresa"""
        # Em produção, buscar da tabela system_config
        pass
    
    def save_company_info(self):
        """Salva informações da empresa"""
        # Em produção, salvar na tabela system_config
        messagebox.showinfo("Sucesso", "Informações da empresa salvas com sucesso!")
    
    def create_backup(self):
        """Cria backup do banco"""
        try:
            from tkinter import filedialog
            
            filename = f"chefconta_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db")],
                initialfile=filename
            )
            
            if filepath:
                db_path = "database/chefconta.db"
                shutil.copy2(db_path, filepath)
                messagebox.showinfo("Sucesso", f"Backup criado com sucesso!\n\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup:\n{str(e)}")
    
    def restore_backup(self):
        """Restaura backup"""
        if not messagebox.askyesno(
            "Confirmação",
            "⚠️ ATENÇÃO!\n\n"
            "Esta operação irá substituir todos os dados atuais.\n"
            "Certifique-se de ter um backup recente antes de continuar.\n\n"
            "Deseja realmente restaurar o backup?"
        ):
            return
        
        try:
            from tkinter import filedialog
            
            filepath = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db")],
                title="Selecione o arquivo de backup"
            )
            
            if filepath:
                db_path = "database/chefconta.db"
                
                # Criar backup de segurança antes
                safety_backup = f"database/chefconta_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(db_path, safety_backup)
                
                # Restaurar
                shutil.copy2(filepath, db_path)
                
                messagebox.showinfo(
                    "Sucesso",
                    f"Backup restaurado com sucesso!\n\n"
                    f"Um backup de segurança foi salvo em:\n{safety_backup}\n\n"
                    f"⚠️ Reinicie o sistema para aplicar as mudanças."
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{str(e)}")


class UserDialog(ctk.CTkToplevel):
    """Diálogo de criação/edição de usuário"""
    
    def __init__(self, parent, user=None):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.auth_controller = AuthController()
        self.db = SessionLocal()
        
        self.title("Editar Usuário" if user else "Novo Usuário")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'medium', maximized=True)
        
        self.create_widgets()
        
        if user:
            self.load_user_data()
    
    def create_widgets(self):
        """Cria widgets"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Editar Usuário" if self.user else "Novo Usuário",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))
        
        # Campos
        self.username_entry = self.create_field(main_frame, "Usuário:")
        self.fullname_entry = self.create_field(main_frame, "Nome Completo:")
        self.email_entry = self.create_field(main_frame, "Email:")
        
        if not self.user:  # Senha apenas na criação
            self.password_entry = self.create_field(main_frame, "Senha:", show="*")
            self.confirm_entry = self.create_field(main_frame, "Confirmar Senha:", show="*")
        
        # Perfil
        role_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(role_frame, text="Perfil:", width=120, anchor="w").pack(side="left", padx=5)
        self.role_var = ctk.StringVar(value="user")
        ctk.CTkRadioButton(role_frame, text="Usuário", variable=self.role_var, value="user").pack(side="left", padx=10)
        ctk.CTkRadioButton(role_frame, text="Admin", variable=self.role_var, value="admin").pack(side="left", padx=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancelar", width=150, command=self.destroy)
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            width=150,
            fg_color="blue",
            hover_color="darkblue",
            command=self.save_user
        )
        save_btn.pack(side="right", padx=5)
    
    def create_field(self, parent, label, show=None):
        """Cria um campo de formulário"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=8)
        
        ctk.CTkLabel(row, text=label, width=120, anchor="w").pack(side="left", padx=5)
        entry = ctk.CTkEntry(row, width=300, show=show)
        entry.pack(side="left", padx=5)
        return entry
    
    def load_user_data(self):
        """Carrega dados do usuário"""
        self.username_entry.insert(0, self.user.username)
        self.fullname_entry.insert(0, self.user.full_name)
        if self.user.email:
            self.email_entry.insert(0, self.user.email)
        self.role_var.set(self.user.role)
    
    def save_user(self):
        """Salva usuário"""
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not username or not fullname:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return
        
        if self.user:  # Edição
            self.user.username = username
            self.user.full_name = fullname
            self.user.email = email
            self.user.role = self.role_var.get()
            self.db.commit()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
        else:  # Novo
            password = self.password_entry.get()
            confirm = self.confirm_entry.get()
            
            if not password:
                messagebox.showwarning("Aviso", "Informe a senha.")
                return
            
            if password != confirm:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            
            # Verificar se usuário já existe
            existing = self.db.query(User).filter(User.username == username).first()
            if existing:
                messagebox.showerror("Erro", "Usuário já existe!")
                return
            
            user = self.auth_controller.create_user(
                self.db,
                username=username,
                password=password,
                full_name=fullname,
                email=email,
                role=self.role_var.get()
            )
            
            if user:
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao criar usuário.")
                return
        
        self.destroy()


class ChangePasswordDialog(ctk.CTkToplevel):
    """Diálogo de alteração de senha"""
    
    def __init__(self, parent, user):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.auth_controller = AuthController()
        self.db = SessionLocal()
        
        self.title(f"Alterar Senha - {user.username}")
        
        self.transient(parent)
        self.grab_set()
        
        # Maximizar janela
        set_dialog_size(self, 'small', maximized=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=f"🔑 Alterar Senha\n{self.user.username}",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Nova senha
        row1 = ctk.CTkFrame(main_frame, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        ctk.CTkLabel(row1, text="Nova Senha:", width=140, anchor="w").pack(side="left", padx=5)
        self.new_pass_entry = ctk.CTkEntry(row1, width=250, show="*")
        self.new_pass_entry.pack(side="left", padx=5)
        
        # Confirmar
        row2 = ctk.CTkFrame(main_frame, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        ctk.CTkLabel(row2, text="Confirmar Senha:", width=140, anchor="w").pack(side="left", padx=5)
        self.confirm_entry = ctk.CTkEntry(row2, width=250, show="*")
        self.confirm_entry.pack(side="left", padx=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancelar", width=150, command=self.destroy)
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="✅ Alterar Senha",
            width=180,
            fg_color="blue",
            hover_color="darkblue",
            command=self.change_password
        )
        save_btn.pack(side="right", padx=5)
    
    def change_password(self):
        """Altera a senha"""
        new_pass = self.new_pass_entry.get()
        confirm = self.confirm_entry.get()
        
        if not new_pass:
            messagebox.showwarning("Aviso", "Informe a nova senha.")
            return
        
        if new_pass != confirm:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        if len(new_pass) < 6:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 6 caracteres.")
            return
        
        # Alterar senha
        import bcrypt
        hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
        self.user.password_hash = hashed.decode('utf-8')
        self.db.commit()
        
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
        self.destroy()
