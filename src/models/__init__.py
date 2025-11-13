"""
Modelos do Banco de Dados - ChefConta
Definição de todas as tabelas do sistema
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

# Enums
class UserRole(enum.Enum):
    """Tipos de usuário"""
    ADMIN = "admin"
    OPERADOR = "operador"

class TransactionType(enum.Enum):
    """Tipos de transação de estoque"""
    ENTRADA = "entrada"
    SAIDA = "saida"
    AJUSTE = "ajuste"

class ExpenseType(enum.Enum):
    """Tipos de despesa"""
    FORNECEDOR = "fornecedor"
    ALUGUEL = "aluguel"
    SALARIO = "salario"
    IMPOSTO = "imposto"
    ENERGIA = "energia"
    AGUA = "agua"
    TELEFONE = "telefone"
    INTERNET = "internet"
    OUTROS = "outros"

# Tabela de Usuários
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="operador")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    sales = relationship("Sale", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")

# Tabela de Clientes
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    sales = relationship("Sale", back_populates="customer")

# Tabela de Fornecedores
class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    purchases = relationship("Purchase", back_populates="supplier")
    expenses = relationship("Expense", back_populates="supplier")

# Tabela de Categorias de Produtos
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    products = relationship("Product", back_populates="category")

# Tabela de Produtos
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    unit = Column(String(20), default="UN")  # UN, KG, L, etc
    cost_price = Column(Float, default=0.0)
    sale_price = Column(Float, nullable=False)
    stock_quantity = Column(Float, default=0.0)
    min_stock = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    category = relationship("Category", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")
    purchase_items = relationship("PurchaseItem", back_populates="product")
    stock_movements = relationship("StockMovement", back_populates="product")

# Tabela de Vendas
class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sale_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_cancelled = Column(Boolean, default=False)
    cancelled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    customer = relationship("Customer", back_populates="sales")
    user = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

# Tabela de Itens de Venda
class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relacionamentos
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

# Tabela de Compras
class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_number = Column(String(50), unique=True, nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purchase_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    supplier = relationship("Supplier", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")

# Tabela de Itens de Compra
class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relacionamentos
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")

# Tabela de Despesas
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    expense_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    expense_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=True)
    paid = Column(Boolean, default=False)
    paid_date = Column(DateTime, nullable=True)
    payment_method = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    user = relationship("User", back_populates="expenses")
    supplier = relationship("Supplier", back_populates="expenses")

# Tabela de Movimentação de Estoque
class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)  # entrada, saida, ajuste
    quantity = Column(Float, nullable=False)
    reason = Column(String(100), nullable=True)
    reference_id = Column(Integer, nullable=True)  # ID da venda/compra relacionada
    reference_type = Column(String(50), nullable=True)  # sale, purchase, adjustment
    previous_stock = Column(Float, nullable=False)
    new_stock = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    product = relationship("Product", back_populates="stock_movements")

# Tabela de Configurações
class SystemConfig(Base):
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Tabela de Licenciamento (opcional)
class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    activated_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    company_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

# Tabela de Caixa
class CashRegister(Base):
    __tablename__ = "cash_registers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opening_date = Column(DateTime, default=datetime.now, nullable=False)
    closing_date = Column(DateTime, nullable=True)
    opening_balance = Column(Float, nullable=False, default=0.0)  # Valor inicial do caixa
    closing_balance = Column(Float, nullable=True)  # Valor final do caixa
    total_sales = Column(Float, default=0.0)  # Total de vendas
    total_comanda = Column(Float, default=0.0)  # Total vendas por comanda
    total_balcao = Column(Float, default=0.0)  # Total vendas por balcão
    total_cash = Column(Float, default=0.0)  # Total em dinheiro
    total_card = Column(Float, default=0.0)  # Total em cartão
    total_pix = Column(Float, default=0.0)  # Total em PIX
    total_other = Column(Float, default=0.0)  # Outros pagamentos
    expected_balance = Column(Float, default=0.0)  # Saldo esperado
    difference = Column(Float, default=0.0)  # Diferença (quebra de caixa)
    notes = Column(Text, nullable=True)
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    user = relationship("User")
    movements = relationship("CashMovement", back_populates="cash_register", cascade="all, delete-orphan")

# Tabela de Movimentações do Caixa
class CashMovement(Base):
    __tablename__ = "cash_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    cash_register_id = Column(Integer, ForeignKey("cash_registers.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)  # entrada, saida, sangria, reforco
    sale_type = Column(String(20), nullable=True)  # comanda, balcao (para vendas)
    payment_method = Column(String(50), nullable=True)  # dinheiro, cartao, pix, outros
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    reference_id = Column(Integer, nullable=True)  # ID da venda relacionada
    reference_type = Column(String(50), nullable=True)  # sale
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    cash_register = relationship("CashRegister", back_populates="movements")
