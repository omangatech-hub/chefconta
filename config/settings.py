"""
Configurações da Aplicação ChefConta
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# ===== BANCO DE DADOS =====
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/chefconta.db")

# ===== AUTENTICAÇÃO =====
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-aqui")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ===== UI/UX =====
APP_TITLE = "ChefConta"
APP_VERSION = "1.0.0"
THEME_MODE = "light"  # light ou dark
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# ===== PATHS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATABASE_DIR = os.path.join(BASE_DIR, "database")

# ===== FILAS E CACHE =====
CACHE_ENABLED = True
CACHE_TIMEOUT = 300  # segundos

# ===== LOGGING =====
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join(BASE_DIR, "logs", "chefconta.log")

# ===== FUNCIONALIDADES =====
ENABLE_DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENABLE_REPORTS = True
ENABLE_BACKUP = True

# ===== VALIDAÇÕES =====
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
