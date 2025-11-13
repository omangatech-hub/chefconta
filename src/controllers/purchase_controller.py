"""
Controller de Compras
Gerencia compras de produtos para estoque
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

class PurchaseController:
    """Controlador de compras"""
    
    def generate_purchase_number(self, db: Session) -> str:
        """Gera um número único de compra"""
        from src.models import Purchase
        
        today = datetime.now().strftime("%Y%m%d")
        last_purchase = db.query(Purchase).filter(
            Purchase.purchase_number.like(f"CP{today}%")
        ).order_by(Purchase.id.desc()).first()
        
        if last_purchase:
            last_number = int(last_purchase.purchase_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"CP{today}{new_number:04d}"
    
    def create_purchase(self, db: Session, user_id: int, supplier_id: int,
                       items: List[dict], notes: str = None) -> Optional[object]:
        """Cria uma nova compra"""
        from src.models import Purchase, PurchaseItem
        from src.controllers.product_controller import ProductController
        
        try:
            # Calcular total
            total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
            
            # Gerar número da compra
            purchase_number = self.generate_purchase_number(db)
            
            # Criar compra
            purchase = Purchase(
                purchase_number=purchase_number,
                supplier_id=supplier_id,
                user_id=user_id,
                total_amount=total_amount,
                notes=notes
            )
            
            db.add(purchase)
            db.flush()  # Para obter o ID da compra
            
            # Adicionar itens e atualizar estoque
            product_controller = ProductController()
            
            for item_data in items:
                # Criar item de compra
                item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['quantity'] * item_data['unit_price']
                )
                db.add(item)
                
                # Atualizar estoque (entrada)
                product_controller.update_stock(
                    db,
                    item_data['product_id'],
                    item_data['quantity'],
                    "entrada",
                    f"Compra {purchase_number}",
                    purchase.id,
                    "purchase"
                )
            
            db.commit()
            db.refresh(purchase)
            return purchase
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar compra: {e}")
            return None
    
    def get_purchase(self, db: Session, purchase_id: int) -> Optional[object]:
        """Busca uma compra por ID"""
        from src.models import Purchase
        return db.query(Purchase).filter(Purchase.id == purchase_id).first()
    
    def list_purchases(self, db: Session, start_date: datetime = None,
                      end_date: datetime = None, supplier_id: int = None) -> List:
        """Lista compras com filtros"""
        from src.models import Purchase
        
        query = db.query(Purchase)
        
        if start_date:
            query = query.filter(Purchase.purchase_date >= start_date)
        if end_date:
            query = query.filter(Purchase.purchase_date <= end_date)
        if supplier_id:
            query = query.filter(Purchase.supplier_id == supplier_id)
        
        return query.order_by(Purchase.purchase_date.desc()).all()
    
    def get_purchases_summary(self, db: Session, start_date: datetime = None,
                             end_date: datetime = None) -> dict:
        """Retorna resumo de compras"""
        from src.models import Purchase
        from sqlalchemy import func
        
        query = db.query(
            func.count(Purchase.id).label('total_purchases'),
            func.sum(Purchase.total_amount).label('total_amount')
        )
        
        if start_date:
            query = query.filter(Purchase.purchase_date >= start_date)
        if end_date:
            query = query.filter(Purchase.purchase_date <= end_date)
        
        result = query.first()
        
        return {
            'total_purchases': result.total_purchases or 0,
            'total_amount': float(result.total_amount or 0)
        }
