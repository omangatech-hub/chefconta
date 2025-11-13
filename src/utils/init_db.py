"""
Utilitário para inicializar o banco de dados
Cria as tabelas e usuário admin padrão
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.database import create_tables, SessionLocal
from src.models import User, SystemConfig
from src.controllers.auth_controller import AuthController
from datetime import datetime

def init_database():
    """Inicializa o banco de dados e cria dados padrão"""
    print("🔧 Inicializando banco de dados ChefConta...")
    
    # Criar todas as tabelas
    create_tables()
    print("✅ Tabelas criadas com sucesso!")
    
    # Criar sessão
    db = SessionLocal()
    
    try:
        # Verificar se já existe usuário admin
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if not existing_admin:
            # Criar usuário admin padrão
            auth_controller = AuthController()
            password_hash = auth_controller.hash_password("admin123")
            
            admin_user = User(
                username="admin",
                email="admin@chefconta.com",
                password_hash=password_hash,
                full_name="Administrador",
                role="admin",
                is_active=True,
                created_at=datetime.now()
            )
            
            db.add(admin_user)
            db.commit()
            print("✅ Usuário admin criado!")
            print("   Usuário: admin")
            print("   Senha: admin123")
            print("   ⚠️  ALTERE A SENHA APÓS O PRIMEIRO ACESSO!")
        else:
            print("ℹ️  Usuário admin já existe")
        
        # Criar configurações padrão
        default_configs = [
            ("company_name", "Minha Empresa", "Nome da empresa"),
            ("company_cnpj", "", "CNPJ da empresa"),
            ("company_address", "", "Endereço da empresa"),
            ("theme", "dark", "Tema da interface (dark/light)"),
            ("currency", "BRL", "Moeda padrão"),
        ]
        
        for key, value, description in default_configs:
            existing_config = db.query(SystemConfig).filter(SystemConfig.key == key).first()
            if not existing_config:
                config = SystemConfig(key=key, value=value, description=description)
                db.add(config)
        
        db.commit()
        print("✅ Configurações padrão criadas!")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("Execute 'python main.py' para iniciar o sistema")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
