"""
Gerador de Relatórios
Gera relatórios em PDF e Excel
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
import os

class ReportGenerator:
    """Gerador de relatórios"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
    
    def generate_sales_report(self, sales_data, start_date, end_date):
        """Gera relatório de vendas em PDF"""
        filename = f"relatorio_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        title = Paragraph("Relatório de Vendas", title_style)
        story.append(title)
        
        # Período
        period_text = f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
        period = Paragraph(period_text, self.styles['Normal'])
        story.append(period)
        story.append(Spacer(1, 20))
        
        # Tabela de vendas
        data = [['Nº Venda', 'Data', 'Cliente', 'Valor', 'Status']]
        
        for sale in sales_data:
            data.append([
                sale.sale_number,
                sale.sale_date.strftime('%d/%m/%Y'),
                sale.customer.name if sale.customer else 'N/A',
                f"R$ {sale.final_amount:.2f}",
                'Cancelada' if sale.is_cancelled else 'OK'
            ])
        
        table = Table(data, colWidths=[3*cm, 2.5*cm, 6*cm, 3*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total
        total = sum(s.final_amount for s in sales_data if not s.is_cancelled)
        total_text = f"<b>Total de Vendas: R$ {total:.2f}</b>"
        total_para = Paragraph(total_text, self.styles['Normal'])
        story.append(total_para)
        
        doc.build(story)
        return filepath
    
    def generate_expenses_report(self, expenses_data, start_date, end_date):
        """Gera relatório de despesas em PDF"""
        filename = f"relatorio_despesas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#d62728'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        title = Paragraph("Relatório de Despesas", title_style)
        story.append(title)
        
        # Período
        period_text = f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
        period = Paragraph(period_text, self.styles['Normal'])
        story.append(period)
        story.append(Spacer(1, 20))
        
        # Tabela de despesas
        data = [['Nº Despesa', 'Data', 'Tipo', 'Descrição', 'Valor', 'Status']]
        
        for expense in expenses_data:
            data.append([
                expense.expense_number,
                expense.expense_date.strftime('%d/%m/%Y'),
                expense.expense_type,
                expense.description[:30] + '...' if len(expense.description) > 30 else expense.description,
                f"R$ {expense.amount:.2f}",
                'Pago' if expense.paid else 'Pendente'
            ])
        
        table = Table(data, colWidths=[2.5*cm, 2*cm, 2.5*cm, 5*cm, 2.5*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d62728')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Totais
        total = sum(e.amount for e in expenses_data)
        paid = sum(e.amount for e in expenses_data if e.paid)
        pending = sum(e.amount for e in expenses_data if not e.paid)
        
        totals_text = f"""
        <b>Total de Despesas: R$ {total:.2f}</b><br/>
        <b>Despesas Pagas: R$ {paid:.2f}</b><br/>
        <b>Despesas Pendentes: R$ {pending:.2f}</b>
        """
        totals_para = Paragraph(totals_text, self.styles['Normal'])
        story.append(totals_para)
        
        doc.build(story)
        return filepath
    
    def generate_financial_report(self, sales_data, expenses_data, start_date, end_date):
        """Gera relatório financeiro consolidado em PDF"""
        filename = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        title = Paragraph("Relatório Financeiro Consolidado", title_style)
        story.append(title)
        
        # Período
        period_text = f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
        period = Paragraph(period_text, self.styles['Normal'])
        story.append(period)
        story.append(Spacer(1, 30))
        
        # Resumo Financeiro
        total_revenue = sum(s.final_amount for s in sales_data if not s.is_cancelled)
        total_expenses = sum(e.amount for e in expenses_data)
        balance = total_revenue - total_expenses
        
        summary_data = [
            ['Descrição', 'Valor'],
            ['Receitas (Vendas)', f"R$ {total_revenue:.2f}"],
            ['Despesas', f"R$ {total_expenses:.2f}"],
            ['Saldo', f"R$ {balance:.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[10*cm, 5*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen if balance >= 0 else colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(summary_table)
        
        doc.build(story)
        return filepath
