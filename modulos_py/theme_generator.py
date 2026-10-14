#!/usr/bin/env python3
"""
Generador de temas GTK para diferentes arquitecturas
"""

import os
import json
import platform
import sys

class ThemeGenerator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.arch = platform.machine()
        self.load_config()
    
    def load_config(self):
        config_file = os.path.join(self.config_path, 'dock_config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "theme": "dark",
                "size": 48,
                "transparency": 0.8,
                "position": "bottom"
            }
    
    def generate_gtk_theme(self):
        """Genera un tema GTK básico"""
        theme_name = f"CustomTheme_{self.arch}"
        # Guardar en la carpeta de configuración, no en el sistema
        theme_dir = os.path.join(self.config_path, 'themes', theme_name)
        os.makedirs(theme_dir, exist_ok=True)
        
        # Crear archivo index.theme
        index_content = f"""[Desktop Entry]
Type=X-GNOME-Metatheme
Name={theme_name}
Comment=Custom theme for {self.arch}

[GNOME/GTK]
GtkTheme={theme_name}
Metatheme={theme_name}
"""
        with open(os.path.join(theme_dir, 'index.theme'), 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        # Crear GTK settings
        gtk_settings = {
            "gtk-theme-name": theme_name,
            "gtk-icon-theme-name": "Adwaita",
            "gtk-font-name": "Cantarell 11",
            "gtk-cursor-theme-name": "Adwaita",
            "gtk-application-prefer-dark-theme": self.config.get('theme', 'dark') == 'dark'
        }
        
        gtk_dir = os.path.join(self.config_path, 'gtk-config')
        os.makedirs(gtk_dir, exist_ok=True)
        
        with open(os.path.join(gtk_dir, 'settings.ini'), 'w', encoding='utf-8') as f:
            f.write("[Settings]\n")
            for key, value in gtk_settings.items():
                f.write(f"{key}={value}\n")
        
        return theme_name
    
    def generate_plank_theme(self):
        """Genera tema para Plank dock"""
        theme_name = f"plank-theme-{self.arch}"
        plank_dir = os.path.join(self.config_path, 'plank-themes', theme_name)
        os.makedirs(plank_dir, exist_ok=True)
        
        # Crear archivo de tema
        theme_config = {
            "name": theme_name,
            "author": "Linux Desktop Editor",
            "description": f"Tema para arquitectura {self.arch}",
            "settings": {
                "theme": self.config.get('theme', 'dark'),
                "icon-size": self.config.get('size', 48),
                "transparency": self.config.get('transparency', 0.8),
                "position": self.config.get('position', 'bottom')
            }
        }
        
        with open(os.path.join(plank_dir, 'theme'), 'w', encoding='utf-8') as f:
            json.dump(theme_config, f, indent=2, ensure_ascii=False)
        
        return theme_name

if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        generator = ThemeGenerator(config_path)
        
        print("Generando tema GTK...")
        gtk_theme = generator.generate_gtk_theme()
        print(f"Tema GTK generado: {gtk_theme}")
        
        print("Generando tema Plank...")
        plank_theme = generator.generate_plank_theme()
        print(f"Tema Plank generado: {plank_theme}")
        
        print("¡Temas generados exitosamente!")
        
        # Guardar resumen
        with open(os.path.join(config_path, 'temas_generados.txt'), 'w', encoding='utf-8') as f:
            f.write(f"Temas generados para {config_path}\n")
            f.write(f"GTK Theme: {gtk_theme}\n")
            f.write(f"Plank Theme: {plank_theme}\n")
            f.write(f"Arquitectura: {platform.machine()}\n")
    else:
        print("Uso: python theme_generator.py <config_path>")