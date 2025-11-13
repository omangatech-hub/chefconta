"""
Tema Moderno Claro para ChefConta
Cores e estilos modernos
"""

# Paleta de Cores Moderna
COLORS = {
    # Sidebar
    'sidebar_bg': '#2C3E50',  # Azul escuro elegante
    'sidebar_hover': '#34495E',  # Azul escuro hover
    'sidebar_text': '#FFFFFF',  # Branco
    'sidebar_text_secondary': '#BDC3C7',  # Cinza claro
    
    # Background principal
    'bg_main': '#ECF0F1',  # Cinza muito claro
    'bg_card': '#FFFFFF',  # Branco puro
    
    # Cards coloridos
    'success': '#27AE60',  # Verde moderno
    'success_hover': '#229954',
    'warning': '#F39C12',  # Laranja moderno
    'warning_hover': '#E67E22',
    'info': '#3498DB',  # Azul moderno
    'info_hover': '#2980B9',
    'danger': '#E74C3C',  # Vermelho moderno
    'danger_hover': '#C0392B',
    
    # Textos
    'text_primary': '#2C3E50',  # Azul escuro
    'text_secondary': '#7F8C8D',  # Cinza médio
    'text_light': '#95A5A6',  # Cinza claro
    'text_white': '#FFFFFF',
    
    # Bordas
    'border': '#BDC3C7',
    'border_light': '#ECF0F1',
    
    # Botões primários
    'primary': '#3498DB',
    'primary_hover': '#2980B9',
    
    # Botões secundários
    'secondary': '#95A5A6',
    'secondary_hover': '#7F8C8D',
}


def apply_card_style(frame, color_key='bg_card'):
    """Aplica estilo de card moderno a um frame"""
    frame.configure(
        fg_color=COLORS[color_key],
        corner_radius=12,
        border_width=1,
        border_color=COLORS['border_light']
    )


def create_colored_card(parent, title, value, subtitle, color, icon):
    """Cria um card colorido moderno"""
    import customtkinter as ctk
    
    card = ctk.CTkFrame(
        parent,
        fg_color=color,
        corner_radius=15,
        border_width=0
    )
    
    # Ícone
    icon_label = ctk.CTkLabel(
        card,
        text=icon,
        font=("Arial", 32),
        text_color="white"
    )
    icon_label.place(relx=0.85, rely=0.3, anchor="center")
    
    # Título
    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=("Arial", 13),
        text_color="white",
        anchor="w"
    )
    title_label.pack(anchor="w", padx=25, pady=(25, 5))
    
    # Valor
    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=("Arial", 32, "bold"),
        text_color="white",
        anchor="w"
    )
    value_label.pack(anchor="w", padx=25, pady=(0, 5))
    
    # Subtítulo
    subtitle_label = ctk.CTkLabel(
        card,
        text=subtitle,
        font=("Arial", 11),
        text_color="#E8E8E8",
        anchor="w"
    )
    subtitle_label.pack(anchor="w", padx=25, pady=(0, 25))
    
    return card


def create_info_card(parent, title):
    """Cria um card de informação branco"""
    import customtkinter as ctk
    
    card = ctk.CTkFrame(
        parent,
        fg_color=COLORS['bg_card'],
        corner_radius=15,
        border_width=1,
        border_color=COLORS['border_light']
    )
    
    # Título
    title_frame = ctk.CTkFrame(card, fg_color="transparent")
    title_frame.pack(fill="x", padx=25, pady=(20, 15))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text=title,
        font=("Arial", 18, "bold"),
        text_color=COLORS['text_primary'],
        anchor="w"
    )
    title_label.pack(side="left")
    
    return card
