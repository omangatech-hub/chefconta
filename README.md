# 🍳 ChefConta - Sistema de Gestão Financeira

Sistema completo de gestão financeira local para pequenas e médias empresas, desenvolvido em Python com interface gráfica moderna.

## 📋 Funcionalidades

### 1. Autenticação e Usuários
- ✅ Login e logout seguro
- ✅ Cadastro de usuários (admin, operador)
- ✅ Sistema de permissões por perfil
- ✅ Criptografia de senhas

### 2. Dashboard
- 📊 Visão geral de vendas, despesas e saldo
- 📈 Gráficos e indicadores em tempo real
- ⚠️ Alertas de estoque baixo
- 💰 Contas a pagar e receber

### 3. Vendas
- 🛒 Cadastro rápido de vendas
- 🔍 Consulta e filtros avançados
- ↩️ Cancelamento/estorno
- 📑 Relatórios detalhados

### 4. Produtos e Estoque
- 📦 Cadastro completo de produtos
- 📊 Controle de estoque (entrada/saída)
- ⚠️ Alerta de estoque mínimo
- 📋 Relatório de movimentação

### 5. Despesas
- 💸 Registro de despesas
- 🏷️ Categorização por tipo
- 👤 Controle de fornecedores
- 📊 Relatórios detalhados

### 6. Compras
- 🛍️ Registro de compras
- 🔄 Atualização automática do estoque
- 📄 Relatório de compras

### 7. Relatórios
- 📈 Relatório financeiro consolidado
- 📅 Filtros por período
- 📊 Análises por produto, cliente, fornecedor
- 💾 Exportação para PDF e Excel

### 8. Configurações
- ⚙️ Parâmetros do sistema
- 👥 Gerenciamento de usuários
- 🎨 Personalização visual
- 💾 Backup e restauração

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- Windows 10/11

### Passo a Passo

1. **Clone ou extraia o projeto**
```powershell
cd e:\_chefconta
```

2. **Ative o ambiente virtual**
```powershell
.\venv\Scripts\Activate.ps1
```

3. **Instale as dependências**
```powershell
pip install -r requirements.txt
```

4. **Configure o ambiente**
```powershell
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicialize o banco de dados**
```powershell
python src/utils/init_db.py
```

6. **Execute o sistema**
```powershell
python main.py
```

## 📁 Estrutura do Projeto

```
chefconta/
├── src/
│   ├── models/          # Modelos do banco de dados
│   ├── controllers/     # Lógica de negócio
│   ├── views/           # Interface gráfica
│   └── utils/           # Utilitários
├── database/            # Banco de dados SQLite
├── static/              # Recursos estáticos
│   ├── images/
│   └── icons/
├── config/              # Arquivos de configuração
├── reports/             # Relatórios gerados
├── main.py              # Arquivo principal
└── requirements.txt     # Dependências
```

## 🔐 Usuário Padrão

Após a primeira execução:
- **Usuário:** admin
- **Senha:** admin123

⚠️ **Importante:** Altere a senha padrão após o primeiro acesso!

## 🛠️ Tecnologias

- **Python 3.10+**
- **CustomTkinter** - Interface gráfica moderna
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local
- **ReportLab** - Geração de PDF
- **Pandas** - Manipulação de dados
- **Matplotlib** - Gráficos

## 📝 Licença

Sistema proprietário - Todos os direitos reservados

## 👨‍💻 Suporte

Para suporte e dúvidas, entre em contato através do email: suporte@chefconta.com

---

Desenvolvido com ❤️ para facilitar a gestão financeira do seu negócio
