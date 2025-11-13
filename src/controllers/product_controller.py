"""
Controller de Produtos
Gerencia produtos e estoque
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

class ProductController:
    """Controlador de produtos"""
    
    def create_product(self, db: Session, **kwargs) -> Optional[object]:
        """Cria um novo produto"""
        from src.models import Product, Category
        
        try:
            # Verificar se código já existe
            existing = db.query(Product).filter(Product.code == kwargs['code']).first()
            if existing:
                return None
            
            product = Product(**kwargs)
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar produto: {e}")
            return None
    
    def update_product(self, db: Session, product_id: int, **kwargs) -> bool:
        """Atualiza um produto"""
        from src.models import Product
        
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            product.updated_at = datetime.now()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Erro ao atualizar produto: {e}")
            return False
    
    def delete_product(self, db: Session, product_id: int) -> bool:
        """Deleta um produto"""
        from src.models import Product
        
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            
            product.is_active = False
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return False
    
    def get_product(self, db: Session, product_id: int) -> Optional[object]:
        """Busca um produto por ID"""
        from src.models import Product
        return db.query(Product).filter(Product.id == product_id).first()
    
    def get_product_by_code(self, db: Session, code: str) -> Optional[object]:
        """Busca um produto por código"""
        from src.models import Product
        return db.query(Product).filter(Product.code == code).first()
    
    def list_products(self, db: Session, active_only: bool = True) -> List:
        """Lista todos os produtos"""
        from src.models import Product
        
        query = db.query(Product)
        if active_only:
            query = query.filter(Product.is_active == True)
        
        return query.all()
    
    def search_products(self, db: Session, search_term: str) -> List:
        """Busca produtos por nome ou código"""
        from src.models import Product
        
        search = f"%{search_term}%"
        return db.query(Product).filter(
            (Product.name.like(search)) | (Product.code.like(search))
        ).filter(Product.is_active == True).all()
    
    def update_stock(self, db: Session, product_id: int, quantity: float, 
                     movement_type: str, reason: str = None, 
                     reference_id: int = None, reference_type: str = None) -> bool:
        """Atualiza o estoque de um produto"""
        from src.models import Product, StockMovement
        
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            
            previous_stock = product.stock_quantity
            
            # Atualizar quantidade conforme o tipo de movimentação
            if movement_type == "entrada" or movement_type == "ajuste":
                product.stock_quantity += quantity
            elif movement_type == "saida":
                product.stock_quantity -= quantity
            
            new_stock = product.stock_quantity
            
            # Registrar movimentação
            movement = StockMovement(
                product_id=product_id,
                movement_type=movement_type,
                quantity=quantity,
                reason=reason,
                reference_id=reference_id,
                reference_type=reference_type,
                previous_stock=previous_stock,
                new_stock=new_stock
            )
            
            db.add(movement)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Erro ao atualizar estoque: {e}")
            return False
    
    def get_low_stock_products(self, db: Session) -> List:
        """Retorna produtos com estoque baixo"""
        from src.models import Product
        
        return db.query(Product).filter(
            Product.stock_quantity <= Product.min_stock,
            Product.is_active == True
        ).all()
    
    def get_stock_movements(self, db: Session, product_id: int = None) -> List:
        """Lista movimentações de estoque"""
        from src.models import StockMovement
        
        query = db.query(StockMovement)
        if product_id:
            query = query.filter(StockMovement.product_id == product_id)
        
        return query.order_by(StockMovement.created_at.desc()).all()
