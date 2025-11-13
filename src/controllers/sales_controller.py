"""
Controller de Vendas
Gerencia vendas e itens de venda
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

class SalesController:
    """Controlador de vendas"""
    
    def generate_sale_number(self, db: Session) -> str:
        """Gera um número único de venda"""
        from src.models import Sale
        
        today = datetime.now().strftime("%Y%m%d")
        last_sale = db.query(Sale).filter(
            Sale.sale_number.like(f"VD{today}%")
        ).order_by(Sale.id.desc()).first()
        
        if last_sale:
            last_number = int(last_sale.sale_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"VD{today}{new_number:04d}"
    
    def create_sale(self, db: Session, user_id: int, items: List[dict], 
                    customer_id: int = None, discount: float = 0.0, 
                    payment_method: str = None, notes: str = None) -> Optional[object]:
        """Cria uma nova venda"""
        from src.models import Sale, SaleItem, Product
        from src.controllers.product_controller import ProductController
        
        try:
            # Calcular total
            total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
            final_amount = total_amount - discount
            
            # Gerar número da venda
            sale_number = self.generate_sale_number(db)
            
            # Criar venda
            sale = Sale(
                sale_number=sale_number,
                customer_id=customer_id,
                user_id=user_id,
                total_amount=total_amount,
                discount=discount,
                final_amount=final_amount,
                payment_method=payment_method,
                notes=notes
            )
            
            db.add(sale)
            db.flush()  # Para obter o ID da venda
            
            # Adicionar itens e atualizar estoque
            product_controller = ProductController()
            
            for item_data in items:
                # Criar item de venda
                item = SaleItem(
                    sale_id=sale.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['quantity'] * item_data['unit_price']
                )
                db.add(item)
                
                # Atualizar estoque
                product_controller.update_stock(
                    db, 
                    item_data['product_id'], 
                    item_data['quantity'],
                    "saida",
                    f"Venda {sale_number}",
                    sale.id,
                    "sale"
                )
            
            db.commit()
            db.refresh(sale)
            return sale
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar venda: {e}")
            return None
    
    def cancel_sale(self, db: Session, sale_id: int) -> bool:
        """Cancela uma venda e devolve itens ao estoque"""
        from src.models import Sale, SaleItem
        from src.controllers.product_controller import ProductController
        
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale or sale.is_cancelled:
                return False
            
            # Devolver itens ao estoque
            product_controller = ProductController()
            for item in sale.items:
                product_controller.update_stock(
                    db,
                    item.product_id,
                    item.quantity,
                    "entrada",
                    f"Cancelamento da venda {sale.sale_number}",
                    sale.id,
                    "sale_cancellation"
                )
            
            # Marcar venda como cancelada
            sale.is_cancelled = True
            sale.cancelled_at = datetime.now()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Erro ao cancelar venda: {e}")
            return False
    
    def get_sale(self, db: Session, sale_id: int) -> Optional[object]:
        """Busca uma venda por ID"""
        from src.models import Sale
        return db.query(Sale).filter(Sale.id == sale_id).first()
    
    def list_sales(self, db: Session, start_date: datetime = None, 
                   end_date: datetime = None, customer_id: int = None,
                   include_cancelled: bool = False) -> List:
        """Lista vendas com filtros"""
        from src.models import Sale
        
        query = db.query(Sale)
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        if customer_id:
            query = query.filter(Sale.customer_id == customer_id)
        if not include_cancelled:
            query = query.filter(Sale.is_cancelled == False)
        
        return query.order_by(Sale.sale_date.desc()).all()
    
    def get_sales_summary(self, db: Session, start_date: datetime = None, 
                          end_date: datetime = None) -> dict:
        """Retorna resumo de vendas"""
        from src.models import Sale
        from sqlalchemy import func
        
        query = db.query(
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.final_amount).label('total_revenue')
        ).filter(Sale.is_cancelled == False)
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        
        result = query.first()
        
        return {
            'total_sales': result.total_sales or 0,
            'total_revenue': float(result.total_revenue or 0)
        }
