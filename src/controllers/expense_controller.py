"""
Controller de Despesas
Gerencia despesas da empresa
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

class ExpenseController:
    """Controlador de despesas"""
    
    def generate_expense_number(self, db: Session) -> str:
        """Gera um número único de despesa"""
        from src.models import Expense
        
        today = datetime.now().strftime("%Y%m%d")
        last_expense = db.query(Expense).filter(
            Expense.expense_number.like(f"DP{today}%")
        ).order_by(Expense.id.desc()).first()
        
        if last_expense:
            last_number = int(last_expense.expense_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"DP{today}{new_number:04d}"
    
    def create_expense(self, db: Session, user_id: int, expense_type: str,
                      description: str, amount: float, expense_date: datetime = None,
                      supplier_id: int = None, due_date: datetime = None,
                      paid: bool = False, payment_method: str = None,
                      notes: str = None) -> Optional[object]:
        """Cria uma nova despesa"""
        from src.models import Expense
        
        try:
            expense_number = self.generate_expense_number(db)
            
            expense = Expense(
                expense_number=expense_number,
                user_id=user_id,
                supplier_id=supplier_id,
                expense_type=expense_type,
                description=description,
                amount=amount,
                expense_date=expense_date or datetime.now(),
                due_date=due_date,
                paid=paid,
                paid_date=datetime.now() if paid else None,
                payment_method=payment_method,
                notes=notes
            )
            
            db.add(expense)
            db.commit()
            db.refresh(expense)
            return expense
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar despesa: {e}")
            return None
    
    def mark_as_paid(self, db: Session, expense_id: int, payment_method: str = None) -> bool:
        """Marca uma despesa como paga"""
        from src.models import Expense
        
        try:
            expense = db.query(Expense).filter(Expense.id == expense_id).first()
            if not expense:
                return False
            
            expense.paid = True
            expense.paid_date = datetime.now()
            if payment_method:
                expense.payment_method = payment_method
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Erro ao marcar despesa como paga: {e}")
            return False
    
    def get_expense(self, db: Session, expense_id: int) -> Optional[object]:
        """Busca uma despesa por ID"""
        from src.models import Expense
        return db.query(Expense).filter(Expense.id == expense_id).first()
    
    def list_expenses(self, db: Session, start_date: datetime = None,
                     end_date: datetime = None, expense_type: str = None,
                     supplier_id: int = None, paid: bool = None) -> List:
        """Lista despesas com filtros"""
        from src.models import Expense
        
        query = db.query(Expense)
        
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)
        if expense_type:
            query = query.filter(Expense.expense_type == expense_type)
        if supplier_id:
            query = query.filter(Expense.supplier_id == supplier_id)
        if paid is not None:
            query = query.filter(Expense.paid == paid)
        
        return query.order_by(Expense.expense_date.desc()).all()
    
    def get_expenses_summary(self, db: Session, start_date: datetime = None,
                            end_date: datetime = None) -> dict:
        """Retorna resumo de despesas"""
        from src.models import Expense
        from sqlalchemy import func
        
        # Total de despesas
        query_total = db.query(
            func.count(Expense.id).label('total_expenses'),
            func.sum(Expense.amount).label('total_amount')
        )
        
        if start_date:
            query_total = query_total.filter(Expense.expense_date >= start_date)
        if end_date:
            query_total = query_total.filter(Expense.expense_date <= end_date)
        
        total_result = query_total.first()
        
        # Despesas pagas
        query_paid = db.query(
            func.sum(Expense.amount).label('paid_amount')
        ).filter(Expense.paid == True)
        
        if start_date:
            query_paid = query_paid.filter(Expense.expense_date >= start_date)
        if end_date:
            query_paid = query_paid.filter(Expense.expense_date <= end_date)
        
        paid_result = query_paid.first()
        
        # Despesas pendentes
        query_pending = db.query(
            func.sum(Expense.amount).label('pending_amount')
        ).filter(Expense.paid == False)
        
        if start_date:
            query_pending = query_pending.filter(Expense.expense_date >= start_date)
        if end_date:
            query_pending = query_pending.filter(Expense.expense_date <= end_date)
        
        pending_result = query_pending.first()
        
        return {
            'total_expenses': total_result.total_expenses or 0,
            'total_amount': float(total_result.total_amount or 0),
            'paid_amount': float(paid_result.paid_amount or 0),
            'pending_amount': float(pending_result.pending_amount or 0)
        }
    
    def get_overdue_expenses(self, db: Session) -> List:
        """Retorna despesas vencidas e não pagas"""
        from src.models import Expense
        
        return db.query(Expense).filter(
            Expense.paid == False,
            Expense.due_date < datetime.now()
        ).order_by(Expense.due_date).all()
