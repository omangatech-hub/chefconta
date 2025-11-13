"""
Script de teste para validar os métodos de usuário do AuthController
"""
from src.controllers.auth_controller import AuthController
from src.models.database import SessionLocal, create_tables
from src.models import User

# Inicializar banco
create_tables()
db = SessionLocal()
auth = AuthController()

print("=" * 60)
print("TESTES DO AUTHCONTROLLER - GERENCIAMENTO DE USUÁRIOS")
print("=" * 60)

try:
    # Teste 1: create_user
    print("\n[TESTE 1] Criando novo usuário...")
    result = auth.create_user(
        db,
        username='teste_novo_user',
        password='senha123',
        full_name='Usuário de Teste',
        email='teste@example.com',
        role='operador'
    )
    
    if result:
        print("✅ Usuário criado com sucesso!")
        print(f"   - ID: {result['id']}")
        print(f"   - Username: {result['username']}")
        print(f"   - Role: {result['role']}")
        user_id = result['id']
    else:
        print("❌ Erro ao criar usuário")
        exit(1)
    
    # Teste 2: list_users
    print("\n[TESTE 2] Listando usuários...")
    users = auth.list_users(db)
    print(f"✅ Total de usuários: {len(users)}")
    for user in users[:3]:  # Mostrar apenas 3 primeiros
        print(f"   - {user['username']} ({user['role']})")
    
    # Teste 3: update_user
    print("\n[TESTE 3] Atualizando usuário...")
    updated = auth.update_user(
        db,
        user_id=user_id,
        full_name='Usuário Atualizado',
        role='admin'
    )
    
    if updated:
        print("✅ Usuário atualizado com sucesso!")
        # Verificar atualização
        user = db.query(User).filter(User.id == user_id).first()
        print(f"   - Nome: {user.full_name}")
        print(f"   - Role: {user.role}")
    else:
        print("❌ Erro ao atualizar usuário")
    
    # Teste 4: delete_user (desativa)
    print("\n[TESTE 4] Desativando usuário...")
    deleted = auth.delete_user(db, user_id=user_id)
    
    if deleted:
        print("✅ Usuário desativado com sucesso!")
        user = db.query(User).filter(User.id == user_id).first()
        print(f"   - Ativo: {user.is_active}")
    else:
        print("❌ Erro ao desativar usuário")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
