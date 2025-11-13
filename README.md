# 🍳 ChefConta - Sistema de Gestão Financeira

Sistema completo de gestão financeira local para pequenas e médias empresas, desenvolvido em Python com interface gráfica moderna e tema claro.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)

## 📸 Screenshots

### Dashboard Moderno
![Dashboard](docs/screenshots/dashboard.png)

### Módulo de Caixa
![Caixa](docs/screenshots/caixa.png)

### Gestão de Vendas
![Vendas](docs/screenshots/vendas.png)

> 💡 **Nota**: Screenshots serão adicionados em breve

## 📋 Funcionalidades

### 1. 🔐 Autenticação e Usuários
- ✅ Login e logout seguro
- ✅ Cadastro de usuários (admin, operador)
- ✅ Sistema de permissões por perfil
- ✅ Criptografia de senhas com bcrypt

### 2. 📊 Dashboard Moderno
- 📊 Visão geral de vendas, despesas e saldo
- 🎨 Interface moderna com tema claro
- 📈 Cards coloridos com indicadores
- ⚠️ Alertas de estoque baixo
- 💰 Contas a pagar e receber

### 3. 💰 Módulo de Caixa
- 📂 Abertura e fechamento de caixa
- 💵 Controle de vendas por comanda ou balcão
- 📊 Movimentações (sangria e reforço)
- 📈 Histórico completo de caixas
- 🔒 Controle de acesso por usuário

### 4. 🛒 Vendas
- 🛒 Cadastro rápido de vendas
- 🔍 Consulta e filtros avançados
- ↩️ Cancelamento/estorno
- 📑 Relatórios detalhados
- 💳 Múltiplas formas de pagamento

### 5. 📦 Produtos e Estoque
- 📦 Cadastro completo de produtos
- 📊 Controle de estoque (entrada/saída)
- ⚠️ Alerta de estoque mínimo
- � Atualização automática nas vendas
- �📋 Relatório de movimentação

### 6. 💸 Despesas
- 💸 Registro de despesas
- 🏷️ Categorização por tipo
- 👤 Controle de fornecedores
- � Controle de vencimentos
- �📊 Relatórios detalhados

### 7. 🛍️ Compras
- 🛍️ Registro de compras
- 🔄 Atualização automática do estoque
- � Gestão de fornecedores
- �📄 Relatório de compras

### 8. 📈 Relatórios
- 📈 Relatório financeiro consolidado
- 📅 Filtros por período personalizados
- 📊 Análises por produto, cliente, fornecedor
- 💾 Exportação para PDF e Excel
- 🎨 Interface moderna maximizada

### 9. ⚙️ Configurações
- ⚙️ Parâmetros do sistema
- 👥 Gerenciamento de usuários
- 🎨 Tema moderno claro
- 🖥️ Janelas maximizadas automaticamente
- 💾 Backup e restauração

## ✨ Destaques

- 🎨 **Interface Moderna**: Design limpo com tema claro
- 📱 **Responsivo**: Janelas maximizadas para melhor visualização
- � **Rápido**: Sistema local, sem dependência de internet
- 🔒 **Seguro**: Dados criptografados e armazenados localmente
- 📊 **Completo**: Todos os módulos necessários para gestão financeira

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

- **Python 3.10+** - Linguagem principal
- **CustomTkinter 5.2+** - Interface gráfica moderna
- **SQLAlchemy 2.0+** - ORM para banco de dados
- **SQLite** - Banco de dados local e rápido
- **Bcrypt** - Criptografia de senhas
- **ReportLab** - Geração de PDF
- **OpenPyXL** - Exportação para Excel
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Gráficos e visualizações

## 🎨 Design System

O sistema utiliza um tema moderno claro com:
- **Paleta de cores**: Azul escuro (#2C3E50), Verde (#27AE60), Laranja (#F39C12), Azul (#3498DB)
- **Tipografia**: Arial com hierarquia clara
- **Cards coloridos**: Indicadores visuais intuitivos
- **Janelas maximizadas**: Melhor aproveitamento da tela

## 📝 Licença

Sistema proprietário - Todos os direitos reservados © 2025 OmangaTech

## 👨‍💻 Desenvolvido por

**OmangaTech Hub**
- GitHub: [@omangatech-hub](https://github.com/omangatech-hub)
- Repositório: [chefconta](https://github.com/omangatech-hub/chefconta)

## 📞 Suporte

Para suporte e dúvidas:
- 📧 Email: urbiatecnologia@gmail.com
- 🌐 GitHub Issues: [Reportar problema](https://github.com/omangatech-hub/chefconta/issues)

---

Desenvolvido com ❤️ usando Python e CustomTkinter


