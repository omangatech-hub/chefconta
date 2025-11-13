"""
Controller de Autenticação
Gerencia login, logout e permissões de usuários
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AuthController:
    """Controlador de autenticação"""
    
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "chefconta-secret-key-2024")
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "chefconta-jwt-secret-2024")
        self.current_user = None
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def generate_token(self, user_id: int, username: str, role: str) -> str:
        """Gera um token JWT para o usuário"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verifica e decodifica um token JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def login(self, db, username: str, password: str) -> Optional[dict]:
        """Realiza login do usuário"""
        from src.models import User
        
        # Buscar usuário
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        # Verificar senha
        if not self.verify_password(password, user.password_hash):
            return None
        
        # Gerar token
        token = self.generate_token(user.id, user.username, user.role)
        
        # Armazenar usuário atual
        self.current_user = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role,
            'token': token
        }
        
        return self.current_user
    
    def logout(self):
        """Realiza logout do usuário"""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Verifica se há usuário autenticado"""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Verifica se o usuário atual é admin"""
        if not self.current_user:
            return False
        return self.current_user['role'] == 'admin'
    
    def has_permission(self, required_role: str) -> bool:
        """Verifica se o usuário tem a permissão necessária"""
        if not self.current_user:
            return False
        
        if self.current_user['role'] == 'admin':
            return True
        
        return self.current_user['role'] == required_role
    
    def get_current_user(self) -> Optional[dict]:
        """Retorna o usuário atual"""
        return self.current_user
    
    def change_password(self, db, user_id: int, old_password: str, new_password: str) -> bool:
        """Altera a senha do usuário"""
        from src.models import User
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Verificar senha antiga
        if not self.verify_password(old_password, user.password_hash):
            return False
        
        # Atualizar senha
        user.password_hash = self.hash_password(new_password)
        user.updated_at = datetime.now()
        db.commit()
        
        return True
    
    def create_user(self, db, username: str, password: str, full_name: str, email: str, role: str = 'operador'):
        """Cria um novo usuário"""
        from src.models import User
        
        try:
            # Verificar se usuário já existe
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                return None
            
            # Criar novo usuário
            new_user = User(
                username=username,
                password_hash=self.hash_password(password),
                full_name=full_name,
                email=email,
                role=role,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return {
                'id': new_user.id,
                'username': new_user.username,
                'full_name': new_user.full_name,
                'email': new_user.email,
                'role': new_user.role,
                'is_active': new_user.is_active
            }
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            db.rollback()
            return None
    
    def update_user(self, db, user_id: int, username: str = None, full_name: str = None, 
                    email: str = None, role: str = None, is_active: bool = None) -> bool:
        """Atualiza dados de um usuário"""
        from src.models import User
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            if username:
                # Verificar se novo username já existe
                existing = db.query(User).filter(
                    User.username == username,
                    User.id != user_id
                ).first()
                if existing:
                    return False
                user.username = username
            
            if full_name:
                user.full_name = full_name
            
            if email:
                user.email = email
            
            if role:
                user.role = role
            
            if is_active is not None:
                user.is_active = is_active
            
            user.updated_at = datetime.now()
            db.commit()
            
            return True
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            db.rollback()
            return False
    
    def delete_user(self, db, user_id: int) -> bool:
        """Deleta um usuário (desativa)"""
        from src.models import User
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Não permite deletar o próprio usuário ou o único admin
            if self.current_user and user.id == self.current_user['id']:
                return False
            
            # Verifica se é o último admin
            if user.role == 'admin':
                admin_count = db.query(User).filter(
                    User.role == 'admin',
                    User.is_active == True
                ).count()
                if admin_count <= 1:
                    return False
            
            # Desativar ao invés de deletar
            user.is_active = False
            user.updated_at = datetime.now()
            db.commit()
            
            return True
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            db.rollback()
            return False
    
    def list_users(self, db) -> list:
        """Lista todos os usuários"""
        from src.models import User
        
        try:
            users = db.query(User).filter(User.is_active == True).all()
            return [
                {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'role': user.role,
                    'is_active': user.is_active,
                    'created_at': user.created_at
                }
                for user in users
            ]
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
