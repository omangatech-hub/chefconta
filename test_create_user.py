"""
Teste para validar o método create_user do AuthController
"""
from src.controllers.auth_controller import AuthController
from src.models.database import SessionLocal, create_tables
from src.models import User

# Inicializar banco
create_tables()
db = SessionLocal()
auth = AuthController()

print("=" * 70)
print("TESTE DE CRIAR NOVO USUÁRIO")
print("=" * 70)

try:
    # Verificar se o método existe
    print("\n[VERIFICAÇÃO] Verificando se o método create_user existe...")
    if hasattr(auth, 'create_user'):
        print("✅ Método create_user EXISTE na classe AuthController")
    else:
        print("❌ Método create_user NÃO EXISTE!")
        exit(1)
    
    # Tentar criar um novo usuário
    print("\n[TESTE 1] Criando novo usuário de teste...")
    result = auth.create_user(
        db,
        username='novo_teste_user_001',
        password='senha_teste_123',
        full_name='Usuário de Teste',
        email='teste@example.com',
        role='operador'
    )
    
    if result:
        print("✅ SUCESSO - Usuário criado!")
        print(f"   ID: {result['id']}")
        print(f"   Username: {result['username']}")
        print(f"   Full Name: {result['full_name']}")
        print(f"   Role: {result['role']}")
        print(f"   Email: {result['email']}")
    else:
        print("❌ FALHA - Retornou None")
        
except AttributeError as e:
    print(f"❌ ERRO DE ATRIBUTO: {e}")
    print("   Método create_user não está disponível!")
except Exception as e:
    print(f"❌ ERRO: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
    print("\n" + "=" * 70)
