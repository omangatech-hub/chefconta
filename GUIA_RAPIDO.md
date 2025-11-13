# 🎯 GUIA RÁPIDO - ChefConta

## 🚀 Inicialização Rápida

### Opção 1: Script Automático (Recomendado)
```powershell
.\run.ps1
```

### Opção 2: Manual
```powershell
# 1. Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar dependências (primeira vez)
pip install -r requirements.txt

# 3. Inicializar banco (primeira vez)
python src\utils\init_db.py

# 4. Executar sistema
python main.py
```

## 🔐 Login Padrão
- **Usuário:** admin
- **Senha:** admin123

## 📋 Funcionalidades Principais

### ✅ Módulos Implementados
1. **Dashboard** - Visão geral do sistema
2. **Autenticação** - Login seguro com bcrypt
3. **Banco de Dados** - SQLite com SQLAlchemy
4. **Controllers** - Lógica completa para:
   - Vendas
   - Produtos e Estoque
   - Despesas
   - Compras
5. **Relatórios** - Geração de PDF

### 🎨 Interface
- CustomTkinter (tema dark)
- Menu lateral intuitivo
- Navegação por módulos
- Dashboard com cards informativos

## 📊 Estrutura do Banco de Dados

### Tabelas Criadas:
- `users` - Usuários do sistema
- `customers` - Clientes
- `suppliers` - Fornecedores
- `categories` - Categorias de produtos
- `products` - Produtos e estoque
- `sales` - Vendas
- `sale_items` - Itens de venda
- `purchases` - Compras
- `purchase_items` - Itens de compra
- `expenses` - Despesas
- `stock_movements` - Movimentações de estoque
- `system_config` - Configurações
- `licenses` - Licenciamento (opcional)

## 🔧 Configurações

Edite o arquivo `.env` para personalizar:
- Nome da empresa
- CNPJ
- Endereço
- Chaves de segurança
- Outras configurações

## 📈 Próximas Etapas

1. **Cadastrar Produtos**
   - Acesse "Produtos"
   - Cadastre seus produtos
   - Defina estoque mínimo

2. **Registrar Vendas**
   - Acesse "Vendas"
   - Selecione produtos
   - Finalize a venda

3. **Controlar Despesas**
   - Acesse "Despesas"
   - Registre gastos
   - Acompanhe pagamentos

4. **Gerar Relatórios**
   - Acesse "Relatórios"
   - Escolha o período
   - Exporte em PDF

## 🛠️ Desenvolvimento Futuro

### Módulos a Expandir:
- [ ] Formulários completos de cadastro
- [ ] Gráficos de vendas
- [ ] Dashboard interativo
- [ ] Exportação Excel
- [ ] Sistema de backup
- [ ] Integração com nota fiscal
- [ ] App mobile

## 💡 Dicas de Uso

1. **Permissões**
   - Admin: acesso total
   - Operador: sem acesso a configurações

2. **Estoque**
   - Sistema atualiza automaticamente
   - Alertas de estoque baixo
   - Histórico de movimentações

3. **Relatórios**
   - Salvos em `/reports`
   - Formato PDF profissional
   - Dados consolidados

## 🐛 Problemas Comuns

**"Não foi possível resolver importação"**
- É normal durante desenvolvimento
- Execute: `pip install -r requirements.txt`

**"Banco não inicializado"**
- Execute: `python src\utils\init_db.py`

**"Erro ao fazer login"**
- Verifique se o banco foi inicializado
- Use: admin / admin123

## 📞 Suporte Técnico

Consulte os arquivos:
- `README.md` - Documentação completa
- `INSTALACAO.md` - Guia de instalação
- `.env.example` - Exemplo de configuração

---

**ChefConta v1.0**
Sistema completo de gestão financeira
Desenvolvido com Python + CustomTkinter + SQLAlchemy
