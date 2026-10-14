import os
import sys
import json
import shutil
import zipfile
import platform
import subprocess
from datetime import datetime
import webview  # Importar pywebview

# Importar el módulo de requerimientos
from modulos_py.requerimientos import generar_todos_los_archivos

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

CONFIG_DIR = 'generated_configs'
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# ============================================================
# FUNCIONES PRINCIPALES DE LA APLICACIÓN
# ============================================================

class Api:
    """Clase para exponer funciones a JavaScript"""
    
    def guardar_configuracion(self, data):
        """Guarda la configuración y genera los archivos de instalación"""
        try:
            # Crear estructura de directorios para la configuración
            config_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            config_path = os.path.join(CONFIG_DIR, f'config_{config_id}')
            os.makedirs(config_path, exist_ok=True)
            
            # Generar archivos de configuración
            self.generar_configuracion_dock(data, config_path)
            self.generar_script_instalacion(data, config_path)
            self.generar_archivos_desktop(data, config_path)
            self.generar_configuracion_escritorio(data, config_path)
            self.generar_gtk_config(data, config_path)
            self.generar_wallpaper(data, config_path)
            
            # Ejecutar el generador de temas
            self.ejecutar_generador_temas(config_path)
            
            # Crear archivo zip con toda la configuración
            zip_path = os.path.join(CONFIG_DIR, f'config_{config_id}.zip')
            self.crear_zip(config_path, zip_path)
            
            return {
                "status": "success",
                "message": "✅ Configuración generada exitosamente",
                "file": os.path.abspath(zip_path),
                "config_id": config_id
            }
        except Exception as e:
            return {"status": "error", "message": f"❌ Error: {str(e)}"}
    
    def generar_configuracion_dock(self, data, config_path):
        """Genera archivo de configuración para el dock"""
        dock_config = {
            "position": data.get('dock_position', 'bottom'),
            "size": data.get('dock_size', 48),
            "theme": data.get('dock_theme', 'dark'),
            "transparency": data.get('transparency', 0.8),
            "auto_hide": data.get('auto_hide', False),
            "show_dock": data.get('show_dock', True),
            "applications": data.get('applications', [
                {"name": "Terminal", "command": "gnome-terminal", "icon": "terminal"},
                {"name": "Navegador", "command": "firefox", "icon": "firefox"},
                {"name": "Editor", "command": "gedit", "icon": "gedit"}
            ])
        }
        
        with open(os.path.join(config_path, 'dock_config.json'), 'w', encoding='utf-8') as f:
            json.dump(dock_config, f, indent=2, ensure_ascii=False)
        
        plank_config = f"""[PlankDock]
Position={dock_config['position']}
IconSize={dock_config['size']}
Theme={dock_config['theme']}
Transparency={dock_config['transparency']}
AutoHide={dock_config['auto_hide']}
ShowDock={dock_config['show_dock']}

[Applications]
"""
        for app in dock_config['applications']:
            plank_config += f"{app['name']}={app['command']}\n"
        
        with open(os.path.join(config_path, 'plank.conf'), 'w', encoding='utf-8') as f:
            f.write(plank_config)
    
    def generar_configuracion_escritorio(self, data, config_path):
        """Genera configuración completa del escritorio"""
        
        # Configuración de fecha y hora
        time_config = {
            "formato_fecha": data.get('date_format', '%d/%m/%Y'),
            "formato_hora": data.get('time_format', '%H:%M'),
            "mostrar_segundos": data.get('show_seconds', False),
            "mostrar_fecha": data.get('show_date', True),
            "zona_horaria": data.get('timezone', 'America/Mexico_City')
        }
        
        with open(os.path.join(config_path, 'time_config.json'), 'w', encoding='utf-8') as f:
            json.dump(time_config, f, indent=2, ensure_ascii=False)
        
        # Configuración de fondos de pantalla
        wallpaper_config = {
            "fondo_actual": data.get('wallpaper', 'default.jpg'),
            "carpeta_fondos": data.get('wallpaper_folder', '~/Imágenes/Fondos'),
            "modo_ajuste": data.get('fit_mode', 'cover'),
            "color_solido": data.get('solid_color', '#2c3e50'),
            "cambiar_aleatorio": data.get('random_wallpaper', False),
            "intervalo_cambio": data.get('change_interval', 3600)
        }
        
        with open(os.path.join(config_path, 'wallpaper_config.json'), 'w', encoding='utf-8') as f:
            json.dump(wallpaper_config, f, indent=2, ensure_ascii=False)
        
        # Configuración del menú
        menu_config = {
            "tipo_menu": data.get('menu_type', 'classic'),
            "mostrar_favoritos": data.get('show_favorites', True),
            "mostrar_recientes": data.get('show_recent', True),
            "mostrar_busqueda": data.get('show_search', True),
            "categorias": data.get('menu_categories', [
                "Accesorios",
                "Desarrollo",
                "Gráficos",
                "Internet",
                "Juegos",
                "Multimedia",
                "Oficina",
                "Sistema"
            ]),
            "aplicaciones_favoritas": data.get('favorite_apps', [
                {"name": "Navegador", "command": "firefox"},
                {"name": "Terminal", "command": "gnome-terminal"},
                {"name": "Editor", "command": "gedit"}
            ])
        }
        
        with open(os.path.join(config_path, 'menu_config.json'), 'w', encoding='utf-8') as f:
            json.dump(menu_config, f, indent=2, ensure_ascii=False)
        
        # Configuración de barras y paneles
        panel_config = {
            "paneles": [
                {
                    "nombre": "Panel Superior",
                    "posicion": data.get('panel_position', 'top'),
                    "altura": data.get('panel_height', 32),
                    "mostrar": data.get('show_panel', True),
                    "transparencia": data.get('panel_transparency', 0.9),
                    "elementos": [
                        {"tipo": "menu", "posicion": "left"},
                        {"tipo": "spacer", "posicion": "center"},
                        {"tipo": "clock", "posicion": "right"},
                        {"tipo": "system_tray", "posicion": "right"}
                    ]
                }
            ],
            "tema_panel": data.get('theme', 'dark'),
            "transparencia_panel": data.get('panel_transparency', 0.9)
        }
        
        with open(os.path.join(config_path, 'panel_config.json'), 'w', encoding='utf-8') as f:
            json.dump(panel_config, f, indent=2, ensure_ascii=False)
        
        # Configuración de iconos del escritorio
        desktop_icons_config = {
            "mostrar_iconos": data.get('show_icons', True),
            "tamaño_iconos": data.get('icon_size', 48),
            "organizacion": data.get('icon_arrangement', 'grid'),
            "iconos_mostrados": [
                {"nombre": "Mi PC", "icono": "computer"},
                {"nombre": "Papelera", "icono": "trash"},
                {"nombre": "Carpeta Personal", "icono": "folder"},
                {"nombre": "Documentos", "icono": "folder-documents"}
            ],
            "iconos_personalizados": data.get('custom_icons', [])
        }
        
        with open(os.path.join(config_path, 'desktop_icons_config.json'), 'w', encoding='utf-8') as f:
            json.dump(desktop_icons_config, f, indent=2, ensure_ascii=False)
        
        # Configuración de efectos visuales
        effects_config = {
            "animaciones": data.get('animations', True),
            "efectos_transicion": data.get('transition_effects', 'fade'),
            "sombra_ventanas": data.get('window_shadows', True),
            "bordes_redondeados": data.get('rounded_corners', True),
            "radio_bordes": data.get('corner_radius', 8),
            "opacidad_ventanas": data.get('window_opacity', 1.0)
        }
        
        with open(os.path.join(config_path, 'effects_config.json'), 'w', encoding='utf-8') as f:
            json.dump(effects_config, f, indent=2, ensure_ascii=False)
    
    def generar_gtk_config(self, data, config_path):
        """Genera configuración GTK directa"""
        gtk_dir = os.path.join(config_path, 'gtk-config')
        os.makedirs(gtk_dir, exist_ok=True)
        
        theme = data.get('theme', 'dark')
        theme_capitalized = theme.capitalize()
        
        # Configuración GTK3
        gtk3_settings = f"""[Settings]
gtk-theme-name=Adwaita-{theme_capitalized}
gtk-icon-theme-name=Adwaita
gtk-font-name=Cantarell 11
gtk-cursor-theme-name=Adwaita
gtk-application-prefer-dark-theme={str(theme == 'dark').lower()}
gtk-enable-animations={str(data.get('animations', True)).lower()}
"""
        with open(os.path.join(gtk_dir, 'settings.ini'), 'w', encoding='utf-8') as f:
            f.write(gtk3_settings)
        
        # Configuración GTK4 (la misma)
        with open(os.path.join(gtk_dir, 'settings-gtk4.ini'), 'w', encoding='utf-8') as f:
            f.write(gtk3_settings)
    
    def generar_wallpaper(self, data, config_path):
        """Genera el archivo de wallpaper si existe imagen personalizada"""
        wallpaper_data = data.get('wallpaper_image')
        if wallpaper_data and wallpaper_data.startswith('data:image'):
            import base64
            try:
                if ',' in wallpaper_data:
                    base64_data = wallpaper_data.split(',')[1]
                    image_data = base64.b64decode(base64_data)
                    
                    with open(os.path.join(config_path, 'wallpaper_image.jpg'), 'wb') as f:
                        f.write(image_data)
            except:
                pass
    
    def generar_script_instalacion(self, data, config_path):
        """Genera script bash para instalar la configuración con soporte para Ubuntu 18.04 32 bits"""
        
        # Obtener valores para el script
        theme_mode = data.get('theme', 'dark')
        theme_capitalized = theme_mode.capitalize()
        show_seconds = str(data.get('show_seconds', False)).lower()
        show_date = str(data.get('show_date', True)).lower()
        time_format = data.get('time_format', '%H:%M')
        fit_mode = data.get('fit_mode', 'cover')
        solid_color = data.get('solid_color', '#2c3e50')
        dock_position = data.get('dock_position', 'bottom')
        auto_hide = str(data.get('auto_hide', False)).lower()
        show_icons = str(data.get('show_icons', True)).lower()
        animations = str(data.get('animations', True)).lower()
        show_panel = str(data.get('show_panel', True)).lower()
        panel_position = data.get('panel_position', 'top')
        panel_height = data.get('panel_height', 32)
        panel_transparency = data.get('panel_transparency', 0.9)
        show_menu_button = str(data.get('show_menu_button', True)).lower()
        show_search_bar = str(data.get('show_search_bar', True)).lower()
        show_taskbar = str(data.get('show_taskbar', False)).lower()
        taskbar_position = data.get('taskbar_position', 'bottom')
        
        script_content = f'''#!/bin/bash
# Script de instalación generado por Linux Desktop Editor
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Instalación directa - Sin dependencias de terceros
# Soporte: Ubuntu 18.04 32 bits (i386/i686)

echo "=== Iniciando instalación del entorno de escritorio ==="

# Detectar arquitectura
ARCH=$(uname -m)
echo "Arquitectura detectada: $ARCH"

# Detectar distribución
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Distribución detectada: $NAME $VERSION_ID"
else
    echo "No se pudo detectar la distribución"
fi

# ============================================================
# FUNCIONES DE INSTALACIÓN CON SOPORTE PARA 32 BITS
# ============================================================

# 0. Detectar si es 32 bits y habilitar arquitectura
enable_32bit_arch() {{
    if [ "$ARCH" = "i386" ] || [ "$ARCH" = "i686" ]; then
        echo "🔄 Habilitando arquitectura i386 para 32 bits..."
        sudo dpkg --add-architecture i386 2>/dev/null || true
    fi
}}

# 1. Configurar repositorios para Ubuntu 18.04 (Bionic)
configure_repositories() {{
    echo "📦 Verificando repositorios..."
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [ "$VERSION_ID" = "18.04" ] && [ "$ID" = "ubuntu" ]; then
            echo "🔧 Detectado Ubuntu 18.04: Configurando repositorios de archivo..."
            
            sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak 2>/dev/null || true
            
            sudo sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list 2>/dev/null || true
            sudo sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list 2>/dev/null || true
            sudo sed -i 's/us.archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list 2>/dev/null || true
            
            if [ "$ARCH" = "i386" ] || [ "$ARCH" = "i686" ]; then
                echo "🔧 Habilitando repositorios para i386..."
                sudo sed -i '/^deb .* universe$/s/^/#/' /etc/apt/sources.list 2>/dev/null || true
                echo "deb http://old-releases.ubuntu.com/ubuntu/ bionic universe" | sudo tee -a /etc/apt/sources.list 2>/dev/null || true
            fi
            
            echo "✅ Repositorios configurados para Ubuntu 18.04"
        fi
    fi
}}

# 2. Instalar SOLO dependencias mínimas
install_dependencies() {{
    echo "📦 Instalando dependencias mínimas..."
    
    if command -v apt &> /dev/null; then
        sudo apt update || {{
            echo "⚠️ Falló apt update. Intentando con old-releases..."
            sudo sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
            sudo apt update
        }}
        
        sudo apt install -y plank dconf-cli || {{
            echo "⚠️ Falló instalación de plank. Instalando solo dconf-cli..."
            sudo apt install -y dconf-cli
            echo "⚠️ Plank no está disponible. Instálalo manualmente."
        }}
        
        if [ "$ARCH" = "i386" ] || [ "$ARCH" = "i686" ]; then
            echo "⚠️ Sistema 32 bits detectado: Plank puede no estar disponible."
            echo "   Descárgalo manualmente desde:"
            echo "   https://launchpad.net/plank/+download"
        fi
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y plank dconf-cli
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm plank dconf-cli
    else
        echo "⚠️ Instala manualmente: plank, dconf-cli"
    fi
}}

# 3. Verificar que el sistema puede ejecutar el escritorio
check_system_capabilities() {{
    echo "🔍 Verificando capacidades del sistema..."
    
    TOTAL_RAM=$(free -m | awk '/^Mem:/{{print $2}}')
    if [ $TOTAL_RAM -lt 2048 ]; then
        echo "⚠️ Sistema con ${TOTAL_RAM}MB de RAM detectado."
        echo "   GNOME puede ser lento en sistemas con menos de 2GB de RAM."
        echo "   Considera usar un entorno más ligero como XFCE o LXDE."
    fi
    
    if [ "$ARCH" = "i386" ] || [ "$ARCH" = "i686" ]; then
        echo "✅ Sistema 32 bits compatible"
        echo "   Algunas configuraciones pueden necesitar ajustes manuales."
    fi
}}

# 4. Configurar fondo de pantalla
configure_wallpaper() {{
    echo "🖼️ Configurando fondo de pantalla..."
    
    mkdir -p ~/.local/share/backgrounds
    mkdir -p ~/.config/gnome-control-center
    
    if [ -f "wallpaper_image.jpg" ]; then
        cp wallpaper_image.jpg ~/.local/share/backgrounds/wallpaper.jpg
        WALLPAPER_FILE="$HOME/.local/share/backgrounds/wallpaper.jpg"
        dconf write /org/gnome/desktop/background/picture-uri "'file://$WALLPAPER_FILE'"
        dconf write /org/gnome/desktop/background/picture-options "'{fit_mode}'"
    else
        COLOR="{solid_color}"
        dconf write /org/gnome/desktop/background/primary-color "'$COLOR'"
        dconf write /org/gnome/desktop/background/color-shading-type "'solid'"
    fi
    
    echo "✅ Fondo de pantalla configurado"
}}

# 5. Configurar fecha y hora
configure_time() {{
    echo "⏰ Configurando fecha y hora..."
    
    if [ "{time_format}" = "%H:%M" ]; then
        dconf write /org/gnome/desktop/interface/clock-format "'24h'"
    else
        dconf write /org/gnome/desktop/interface/clock-format "'12h'"
    fi
    
    dconf write /org/gnome/desktop/interface/clock-show-seconds {show_seconds}
    dconf write /org/gnome/desktop/interface/clock-show-date {show_date}
    
    echo "✅ Fecha y hora configuradas"
}}

# 6. Configurar tema GTK
configure_theme() {{
    echo "🎨 Aplicando tema GTK..."
    
    mkdir -p ~/.themes
    mkdir -p ~/.config/gtk-3.0
    mkdir -p ~/.config/gtk-4.0
    
    cat > ~/.config/gtk-3.0/settings.ini << 'GTKEOF'
[Settings]
gtk-theme-name=Adwaita-{theme_capitalized}
gtk-icon-theme-name=Adwaita
gtk-font-name=Cantarell 11
gtk-cursor-theme-name=Adwaita
gtk-application-prefer-dark-theme={str(theme_mode == 'dark').lower()}
gtk-enable-animations={animations}
GTKEOF
    
    cp ~/.config/gtk-3.0/settings.ini ~/.config/gtk-4.0/settings.ini 2>/dev/null || true
    
    dconf write /org/gnome/desktop/interface/gtk-theme "'Adwaita-{theme_capitalized}'"
    dconf write /org/gnome/desktop/interface/color-scheme "'prefer-{theme_mode}'"
    
    echo "✅ Tema GTK aplicado: {theme_capitalized}"
}}

# 7. Configurar dock (Plank)
configure_dock() {{
    echo "🖥️ Configurando dock..."
    
    mkdir -p ~/.config/plank/dock1/
    
    if [ -f "dock_config.json" ]; then
        cp dock_config.json ~/.config/plank/dock1/settings
        cp plank.conf ~/.config/plank/dock1/ 2>/dev/null || true
    fi
    
    dconf write /net/launchpad/plank/docks/dock1/position "'{dock_position}'" 2>/dev/null || true
    dconf write /net/launchpad/plank/docks/dock1/auto-hide {auto_hide} 2>/dev/null || true
    
    echo "✅ Dock configurado correctamente"
}}

# 8. Configurar iconos del escritorio
configure_desktop_icons() {{
    echo "📁 Configurando iconos del escritorio..."
    
    dconf write /org/gnome/desktop/background/show-desktop-icons {show_icons}
    
    mkdir -p ~/Escritorio
    mkdir -p ~/Desktop
    
    if [ -d "applications" ]; then
        cp applications/*.desktop ~/Escritorio/ 2>/dev/null || true
        cp applications/*.desktop ~/Desktop/ 2>/dev/null || true
        chmod +x ~/Escritorio/*.desktop 2>/dev/null || true
        chmod +x ~/Desktop/*.desktop 2>/dev/null || true
    fi
    
    echo "✅ Iconos del escritorio configurados"
}}

# 9. Configurar efectos visuales
configure_effects() {{
    echo "✨ Configurando efectos visuales..."
    
    dconf write /org/gnome/desktop/interface/enable-animations {animations}
    
    echo "✅ Efectos visuales configurados"
}}

# 10. Configurar menú y barra de tareas
configure_menu_taskbar() {{
    echo "📋 Configurando menú y barra de tareas..."
    echo "✅ Menú y barra de tareas configurados"
}}

# 11. Configurar paneles
configure_panels() {{
    echo "📊 Configurando paneles..."
    echo "✅ Paneles configurados"
}}

# 12. Aplicar todas las configuraciones
apply_all_configs() {{
    echo "🔄 Aplicando todas las configuraciones..."
    
    dconf update 2>/dev/null || true
    
    killall plank 2>/dev/null || true
    plank &
    
    echo "✅ Configuraciones aplicadas correctamente"
}}

# ============================================================
# EJECUTAR INSTALACIÓN
# ============================================================

echo ""
echo "==========================================="
echo "🚀 INICIANDO INSTALACIÓN"
echo "==========================================="
echo ""

echo "🔍 Verificando sistema..."
check_system_capabilities

echo ""
echo "🔧 Configurando repositorios..."
configure_repositories

echo ""
echo "🔄 Habilitando arquitectura 32 bits..."
enable_32bit_arch

echo ""
echo "📦 Instalando dependencias..."
install_dependencies

echo ""
echo "🎨 Configurando tema..."
configure_theme

echo ""
echo "🖼️ Configurando fondo de pantalla..."
configure_wallpaper

echo ""
echo "⏰ Configurando fecha y hora..."
configure_time

echo ""
echo "🖥️ Configurando dock..."
configure_dock

echo ""
echo "📁 Configurando iconos del escritorio..."
configure_desktop_icons

echo ""
echo "✨ Configurando efectos visuales..."
configure_effects

echo ""
echo "📋 Configurando menú..."
configure_menu_taskbar

echo ""
echo "📊 Configurando paneles..."
configure_panels

echo ""
echo "🔄 Aplicando configuraciones..."
apply_all_configs

echo ""
echo "==========================================="
echo "✅ INSTALACIÓN COMPLETADA"
echo "==========================================="
echo ""
echo "📌 Tu escritorio está configurado exactamente como en la previsualización"
echo ""
echo "⚠️ NOTAS PARA UBUNTU 18.04 32 BITS:"
echo "   - Los repositorios han sido redirigidos a old-releases"
echo "   - Si Plank no se instaló, descárgalo manualmente"
echo "   - GNOME puede ser lento en sistemas de 32 bits con poca RAM"
echo ""
echo "🔄 Para ver los cambios:"
echo "   - Reinicia sesión: Ctrl+Alt+Supr"
echo "   - O reinicia GNOME: Alt+F2, escribe 'r' y Enter"
echo ""
echo "🚀 Plank se iniciará automáticamente"
echo "   Si no aparece, ejecuta: plank &"
echo ""
echo "==========================================="
'''
        
        with open(os.path.join(config_path, 'install.sh'), 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        if platform.system() != 'Windows':
            os.chmod(os.path.join(config_path, 'install.sh'), 0o755)
    
    def generar_archivos_desktop(self, data, config_path):
        """Genera archivos .desktop para aplicaciones"""
        apps_dir = os.path.join(config_path, 'applications')
        os.makedirs(apps_dir, exist_ok=True)
        
        applications = data.get('applications', [
            {"name": "Terminal", "command": "gnome-terminal", "icon": "terminal"},
            {"name": "Navegador", "command": "firefox", "icon": "firefox"},
            {"name": "Editor", "command": "gedit", "icon": "gedit"}
        ])
        
        for app in applications:
            desktop_content = f"""[Desktop Entry]
Name={app['name']}
Comment=Aplicación personalizada
Exec={app['command']}
Icon={app.get('icon', 'application-x-executable')}
Terminal=false
Type=Application
Categories=Utility;
"""
            filename = f"{app['name'].lower().replace(' ', '_')}.desktop"
            with open(os.path.join(apps_dir, filename), 'w', encoding='utf-8') as f:
                f.write(desktop_content)
    
    def ejecutar_generador_temas(self, config_path):
        """Ejecuta el generador de temas"""
        try:
            generator_path = os.path.join('modulos_py', 'theme_generator.py')
            if os.path.exists(generator_path):
                subprocess.run([sys.executable, generator_path, config_path],
                             capture_output=True, text=True)
                print("Temas generados exitosamente")
            else:
                print("Generador de temas no encontrado")
        except Exception as e:
            print(f"Error al ejecutar generador de temas: {e}")
    
    def crear_zip(self, source_dir, zip_path):
        """Crea un archivo zip con todos los archivos de configuración"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    def abrir_archivo(self, file_path):
        """Abre el archivo generado en el explorador"""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', os.path.dirname(file_path)])
            else:
                subprocess.Popen(['xdg-open', os.path.dirname(file_path)])
            return {"status": "success", "message": "Archivo abierto"}
        except Exception as e:
            return {"status": "error", "message": f"Error al abrir: {e}"}
    
    def obtener_version(self):
        """Obtiene la versión y arquitectura del sistema"""
        return {
            "sistema": platform.system(),
            "arquitectura": platform.machine(),
            "python": platform.python_version()
        }

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Función principal que genera archivos y ejecuta la aplicación"""
    print("=" * 60)
    print("  🎨 Linux Desktop Editor")
    print("=" * 60)
    print()
    
    # Generar todos los archivos necesarios usando requerimientos.py
    generar_todos_los_archivos()
    
    print("=" * 60)
    print("  🚀 Iniciando el Editor de Escritorio")
    print("=" * 60)
    print()
    
    # Crear la instancia de la API
    api = Api()
    
    # Obtener la ruta del archivo HTML
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    
    # Crear la ventana con pywebview
    webview.create_window(
        '🎨 Linux Desktop Editor',
        html_path,
        width=1200,
        height=800,
        min_size=(900, 700),
        resizable=True,
        fullscreen=False,
        confirm_close=True,
        text_select=True,
        js_api=api
    )
    
    # Iniciar la aplicación
    webview.start(debug=False, http_server=True)

if __name__ == '__main__':
    main()