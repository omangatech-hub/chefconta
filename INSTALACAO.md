# 🚀 INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO - ChefConta

## ✅ Etapa 1: Ativar o Ambiente Virtual

Abra o PowerShell no diretório do projeto e execute:

```powershell
cd e:\_chefconta
.\venv\Scripts\Activate.ps1
```

**Observação:** Se houver erro de permissão, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## ✅ Etapa 2: Instalar Dependências

Com o ambiente virtual ativado, instale as dependências:

```powershell
pip install -r requirements.txt
```

Este processo pode levar alguns minutos.

## ✅ Etapa 3: Inicializar o Banco de Dados

Crie as tabelas e o usuário admin padrão:

```powershell
python src/utils/init_db.py
```

Você verá mensagens de sucesso indicando que o banco foi criado.

## ✅ Etapa 4: Executar o Sistema

Inicie a aplicação:

```powershell
python main.py
```

## 🔐 Credenciais de Acesso

**Primeiro Acesso:**
- **Usuário:** admin
- **Senha:** admin123

⚠️ **IMPORTANTE:** Altere a senha padrão após o primeiro acesso!

## 📂 Estrutura do Projeto

```
chefconta/
├── venv/                    # Ambiente virtual (já criado)
├── src/
│   ├── models/              # Modelos do banco de dados
│   ├── controllers/         # Lógica de negócio
│   ├── views/               # Interface gráfica
│   └── utils/               # Utilitários
├── database/                # Banco de dados SQLite
├── static/                  # Recursos estáticos
├── config/                  # Configurações
├── reports/                 # Relatórios gerados
├── main.py                  # Arquivo principal
├── requirements.txt         # Dependências
└── .env                     # Variáveis de ambiente
```

## 🔧 Módulos Implementados

### ✅ Completos e Funcionais:
1. **Autenticação** - Login, logout, controle de permissões
2. **Banco de Dados** - Todas as tabelas criadas
3. **Controllers** - Vendas, produtos, despesas, compras
4. **Interface Gráfica** - Dashboard e navegação
5. **Relatórios** - Geração de PDF

### 🚧 Prontos para Expansão:
- Telas de cadastro detalhadas
- Formulários de entrada de dados
- Gráficos e visualizações
- Exportação para Excel
- Sistema de backup

## 💡 Próximos Passos

1. **Personalize as configurações** no arquivo `.env`
2. **Adicione produtos** usando o módulo de produtos
3. **Registre vendas e despesas**
4. **Gere relatórios** para análise
5. **Customize a interface** conforme suas necessidades

## 🐛 Solução de Problemas

### Erro ao ativar ambiente virtual
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro "módulo não encontrado"
```powershell
pip install -r requirements.txt
```

### Erro de banco de dados
```powershell
python src/utils/init_db.py
```

### Porta já em uso
Feche outras instâncias do programa.

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação no README.md

---

**ChefConta** - Sistema de Gestão Financeira
Desenvolvido com ❤️ em Python
