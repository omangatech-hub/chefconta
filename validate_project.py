#!/usr/bin/env python3
"""
Script de validação completa do projeto ChefConta
Verifica:
- Sintaxe Python
- Imports
- Estrutura de banco de dados
- Arquivos faltando
- Configurações
"""

import os
import sys
import ast
from pathlib import Path

class ProjectValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.successes = []

    def validate_all(self):
        """Executa todas as validações"""
        print("\n" + "="*70)
        print("VALIDAÇÃO COMPLETA DO PROJETO CHEFCONTA")
        print("="*70 + "\n")
        
        self.check_python_syntax()
        self.check_imports()
        self.check_required_files()
        self.check_database()
        self.check_env_vars()
        self.report()

    def check_python_syntax(self):
        """Verifica sintaxe de todos os arquivos Python"""
        print("[1/5] Verificando sintaxe Python...")
        py_files = list(self.project_root.glob("**/*.py"))
        
        for py_file in py_files:
            if "venv" in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
                self.successes.append(f"✅ Sintaxe OK: {py_file.relative_to(self.project_root)}")
            except SyntaxError as e:
                self.errors.append(f"❌ Erro de sintaxe em {py_file}: {e}")
            except Exception as e:
                self.errors.append(f"❌ Erro ao ler {py_file}: {e}")

    def check_imports(self):
        """Verifica se os imports principais funcionam"""
        print("[2/5] Verificando imports...")
        
        imports_to_check = [
            "src.controllers.auth_controller",
            "src.views.main_view",
            "src.utils.report_generator",
            "src.models.database",
            "src.utils.modern_theme",
        ]
        
        for module in imports_to_check:
            try:
                __import__(module)
                self.successes.append(f"✅ Import OK: {module}")
            except ImportError as e:
                self.errors.append(f"❌ Erro de import: {module} - {e}")
            except Exception as e:
                self.errors.append(f"❌ Erro ao importar {module}: {e}")

    def check_required_files(self):
        """Verifica se os arquivos essenciais existem"""
        print("[3/5] Verificando arquivos essenciais...")
        
        required_files = [
            "main.py",
            "requirements.txt",
            ".env.example",
            "src/__init__.py",
            "src/controllers/auth_controller.py",
            "src/views/main_view.py",
            "src/models/database.py",
            "config/settings.py",
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.successes.append(f"✅ Arquivo existe: {file_path}")
            else:
                self.warnings.append(f"⚠️  Arquivo faltando: {file_path}")

    def check_database(self):
        """Verifica estrutura do banco de dados"""
        print("[4/5] Verificando banco de dados...")
        
        try:
            from src.models.database import SessionLocal, create_tables, engine
            from sqlalchemy import text
            
            # Tentar criar tabelas
            create_tables()
            self.successes.append("✅ Banco de dados e tabelas OK")
            
            # Verificar conexão
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            self.successes.append("✅ Conexão com banco de dados OK")
        except Exception as e:
            self.errors.append(f"❌ Erro ao verificar banco de dados: {e}")

    def check_env_vars(self):
        """Verifica variáveis de ambiente"""
        print("[5/5] Verificando variáveis de ambiente...")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        if env_file.exists():
            self.successes.append("✅ Arquivo .env encontrado")
        else:
            if env_example.exists():
                self.warnings.append("⚠️  Arquivo .env não encontrado, mas .env.example existe")
            else:
                self.errors.append("❌ Arquivo .env e .env.example não encontrados")

    def report(self):
        """Gera relatório de validação"""
        print("\n" + "="*70)
        print("RELATÓRIO DE VALIDAÇÃO")
        print("="*70 + "\n")
        
        if self.successes:
            print(f"✅ SUCESSOS ({len(self.successes)}):\n")
            for success in self.successes[:10]:  # Mostrar os primeiros 10
                print(f"  {success}")
            if len(self.successes) > 10:
                print(f"  ... e mais {len(self.successes) - 10}")
            print()
        
        if self.warnings:
            print(f"⚠️  AVISOS ({len(self.warnings)}):\n")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if self.errors:
            print(f"❌ ERROS ({len(self.errors)}):\n")
            for error in self.errors:
                print(f"  {error}")
            print()
        
        print("="*70)
        if not self.errors:
            print("✅ VALIDAÇÃO COMPLETA - NENHUM ERRO CRÍTICO!")
        else:
            print(f"❌ {len(self.errors)} ERRO(S) CRÍTICO(S) ENCONTRADO(S)")
        print("="*70 + "\n")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    validator = ProjectValidator(Path(__file__).parent)
    success = validator.validate_all()
    sys.exit(0 if success else 1)
