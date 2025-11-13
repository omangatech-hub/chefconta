"""
Controller de Caixa
Gerencia abertura, fechamento e movimentações do caixa
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models import CashRegister, CashMovement, Sale

class CashRegisterController:
    """Controller para operações de caixa"""
    
    def get_open_cash_register(self, db: Session):
        """Retorna o caixa aberto do dia atual"""
        return db.query(CashRegister).filter(
            CashRegister.is_open == True
        ).order_by(CashRegister.opening_date.desc()).first()
    
    def open_cash_register(self, db: Session, user_id: int, opening_balance: float, notes: str = None):
        """Abre um novo caixa"""
        # Verificar se já existe caixa aberto
        open_cash = self.get_open_cash_register(db)
        if open_cash:
            return None, "Já existe um caixa aberto. Feche-o antes de abrir um novo."
        
        try:
            # Criar novo caixa
            cash_register = CashRegister(
                user_id=user_id,
                opening_balance=opening_balance,
                opening_date=datetime.now(),
                notes=notes,
                is_open=True
            )
            
            db.add(cash_register)
            db.commit()
            db.refresh(cash_register)
            
            # Registrar movimento de abertura
            if opening_balance > 0:
                movement = CashMovement(
                    cash_register_id=cash_register.id,
                    movement_type="entrada",
                    payment_method="dinheiro",
                    amount=opening_balance,
                    description="Abertura de caixa"
                )
                db.add(movement)
                db.commit()
            
            return cash_register, None
        except Exception as e:
            db.rollback()
            return None, f"Erro ao abrir caixa: {str(e)}"
    
    def close_cash_register(self, db: Session, cash_register_id: int, 
                           total_cash: float, total_card: float, total_pix: float, 
                           total_other: float, notes: str = None):
        """Fecha o caixa calculando totais e diferenças"""
        try:
            cash_register = db.query(CashRegister).filter(
                CashRegister.id == cash_register_id
            ).first()
            
            if not cash_register:
                return None, "Caixa não encontrado."
            
            if not cash_register.is_open:
                return None, "Este caixa já está fechado."
            
            # Calcular totais por tipo de venda
            movements = db.query(CashMovement).filter(
                CashMovement.cash_register_id == cash_register_id
            ).all()
            
            total_comanda = 0.0
            total_balcao = 0.0
            total_sales = 0.0
            
            for mov in movements:
                if mov.movement_type == "entrada" and mov.reference_type == "sale":
                    total_sales += mov.amount
                    if mov.sale_type == "comanda":
                        total_comanda += mov.amount
                    elif mov.sale_type == "balcao":
                        total_balcao += mov.amount
            
            # Calcular saldo esperado
            expected_balance = (
                cash_register.opening_balance + 
                total_sales + 
                sum(m.amount for m in movements if m.movement_type == "entrada" and m.reference_type != "sale") -
                sum(m.amount for m in movements if m.movement_type in ["saida", "sangria"])
            )
            
            # Calcular saldo informado (fechamento)
            closing_balance = total_cash + total_card + total_pix + total_other
            
            # Calcular diferença (quebra de caixa)
            difference = closing_balance - expected_balance
            
            # Atualizar caixa
            cash_register.closing_date = datetime.now()
            cash_register.closing_balance = closing_balance
            cash_register.total_sales = total_sales
            cash_register.total_comanda = total_comanda
            cash_register.total_balcao = total_balcao
            cash_register.total_cash = total_cash
            cash_register.total_card = total_card
            cash_register.total_pix = total_pix
            cash_register.total_other = total_other
            cash_register.expected_balance = expected_balance
            cash_register.difference = difference
            cash_register.is_open = False
            
            if notes:
                cash_register.notes = (cash_register.notes or "") + "\nFechamento: " + notes
            
            db.commit()
            db.refresh(cash_register)
            
            return cash_register, None
        except Exception as e:
            db.rollback()
            return None, f"Erro ao fechar caixa: {str(e)}"
    
    def add_movement(self, db: Session, cash_register_id: int, movement_type: str,
                    amount: float, description: str, payment_method: str = None,
                    sale_type: str = None, reference_id: int = None, 
                    reference_type: str = None):
        """Adiciona uma movimentação ao caixa"""
        try:
            movement = CashMovement(
                cash_register_id=cash_register_id,
                movement_type=movement_type,
                sale_type=sale_type,
                payment_method=payment_method,
                amount=amount,
                description=description,
                reference_id=reference_id,
                reference_type=reference_type
            )
            
            db.add(movement)
            db.commit()
            db.refresh(movement)
            
            return movement, None
        except Exception as e:
            db.rollback()
            return None, f"Erro ao adicionar movimentação: {str(e)}"
    
    def register_sale_in_cash(self, db: Session, sale_id: int, sale_type: str, 
                             payment_method: str, amount: float):
        """Registra uma venda no caixa aberto"""
        cash_register = self.get_open_cash_register(db)
        if not cash_register:
            return None, "Não há caixa aberto."
        
        return self.add_movement(
            db,
            cash_register_id=cash_register.id,
            movement_type="entrada",
            sale_type=sale_type,
            payment_method=payment_method,
            amount=amount,
            description=f"Venda #{sale_id} - {sale_type.upper()}",
            reference_id=sale_id,
            reference_type="sale"
        )
    
    def add_sangria(self, db: Session, amount: float, description: str):
        """Registra uma sangria (retirada de dinheiro)"""
        cash_register = self.get_open_cash_register(db)
        if not cash_register:
            return None, "Não há caixa aberto."
        
        return self.add_movement(
            db,
            cash_register_id=cash_register.id,
            movement_type="sangria",
            payment_method="dinheiro",
            amount=amount,
            description=f"Sangria: {description}"
        )
    
    def add_reforco(self, db: Session, amount: float, description: str):
        """Registra um reforço (entrada de dinheiro)"""
        cash_register = self.get_open_cash_register(db)
        if not cash_register:
            return None, "Não há caixa aberto."
        
        return self.add_movement(
            db,
            cash_register_id=cash_register.id,
            movement_type="reforco",
            payment_method="dinheiro",
            amount=amount,
            description=f"Reforço: {description}"
        )
    
    def get_cash_register_summary(self, db: Session, cash_register_id: int):
        """Retorna resumo do caixa com todas as movimentações"""
        cash_register = db.query(CashRegister).filter(
            CashRegister.id == cash_register_id
        ).first()
        
        if not cash_register:
            return None
        
        movements = db.query(CashMovement).filter(
            CashMovement.cash_register_id == cash_register_id
        ).order_by(CashMovement.created_at).all()
        
        # Calcular totais em tempo real
        total_vendas = sum(m.amount for m in movements if m.movement_type == "entrada" and m.reference_type == "sale")
        total_entradas = sum(m.amount for m in movements if m.movement_type == "entrada" and m.reference_type != "sale")
        total_saidas = sum(m.amount for m in movements if m.movement_type in ["saida", "sangria"])
        total_reforcos = sum(m.amount for m in movements if m.movement_type == "reforco")
        
        # Total por forma de pagamento
        total_dinheiro = sum(m.amount for m in movements if m.payment_method == "dinheiro" and m.movement_type == "entrada")
        total_cartao = sum(m.amount for m in movements if m.payment_method == "cartao" and m.movement_type == "entrada")
        total_pix_calc = sum(m.amount for m in movements if m.payment_method == "pix" and m.movement_type == "entrada")
        
        # Total por tipo de venda
        total_comanda = sum(m.amount for m in movements if m.sale_type == "comanda")
        total_balcao = sum(m.amount for m in movements if m.sale_type == "balcao")
        
        saldo_atual = (
            cash_register.opening_balance + 
            total_vendas + 
            total_entradas + 
            total_reforcos - 
            total_saidas
        )
        
        return {
            'cash_register': cash_register,
            'movements': movements,
            'total_vendas': total_vendas,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'total_reforcos': total_reforcos,
            'total_dinheiro': total_dinheiro,
            'total_cartao': total_cartao,
            'total_pix': total_pix_calc,
            'total_comanda': total_comanda,
            'total_balcao': total_balcao,
            'saldo_atual': saldo_atual,
            'quantidade_vendas': len([m for m in movements if m.reference_type == "sale"])
        }
    
    def list_cash_registers(self, db: Session, limit: int = 50):
        """Lista os caixas (mais recentes primeiro)"""
        return db.query(CashRegister).order_by(
            CashRegister.opening_date.desc()
        ).limit(limit).all()
