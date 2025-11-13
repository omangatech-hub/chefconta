"""
Utilitários para janelas
Funções para ajustar tamanho e posição de janelas
"""

def center_window(window, width_percent=0.7, height_percent=0.8, min_width=400, min_height=300, max_width=1400, max_height=900):
    """
    Centraliza e ajusta o tamanho da janela baseado na resolução da tela
    
    Args:
        window: Janela CTk ou CTkToplevel
        width_percent: Porcentagem da largura da tela (0.0 a 1.0)
        height_percent: Porcentagem da altura da tela (0.0 a 1.0)
        min_width: Largura mínima em pixels
        min_height: Altura mínima em pixels
        max_width: Largura máxima em pixels
        max_height: Altura máxima em pixels
    """
    # Atualizar para garantir que temos as informações da tela
    window.update_idletasks()
    
    # Obter tamanho da tela
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calcular tamanho da janela baseado na porcentagem
    width = int(screen_width * width_percent)
    height = int(screen_height * height_percent)
    
    # Aplicar limites mínimos e máximos
    width = max(min_width, min(width, max_width))
    height = max(min_height, min(height, max_height))
    
    # Calcular posição central
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Garantir que a janela não fique fora da tela
    x = max(0, x)
    y = max(0, y)
    
    # Aplicar geometria
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    return width, height


def maximize_window(window):
    """
    Maximiza a janela
    
    Args:
        window: Janela CTk ou CTkToplevel
    """
    try:
        # Tenta usar o método state do tkinter
        window.state('zoomed')
    except:
        # Se falhar, usa geometria manual
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.geometry(f'{screen_width}x{screen_height}+0+0')


def set_dialog_size(window, preset='medium', maximized=True):
    """
    Define tamanho de diálogo baseado em presets
    
    Args:
        window: Janela CTkToplevel
        preset: 'small', 'medium', 'large', 'extra-large'
        maximized: Se True, abre maximizado; se False, usa o preset
    """
    if maximized:
        maximize_window(window)
    else:
        presets = {
            'small': {'width_percent': 0.3, 'height_percent': 0.4, 'min_width': 400, 'min_height': 300, 'max_width': 600, 'max_height': 500},
            'medium': {'width_percent': 0.5, 'height_percent': 0.6, 'min_width': 500, 'min_height': 400, 'max_width': 900, 'max_height': 700},
            'large': {'width_percent': 0.65, 'height_percent': 0.75, 'min_width': 700, 'min_height': 600, 'max_width': 1100, 'max_height': 850},
            'extra-large': {'width_percent': 0.8, 'height_percent': 0.85, 'min_width': 900, 'min_height': 700, 'max_width': 1400, 'max_height': 1000}
        }
        
        config = presets.get(preset, presets['medium'])
        return center_window(window, **config)
