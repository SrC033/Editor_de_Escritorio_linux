"""
Módulo para generar todos los archivos necesarios del proyecto
"""

import os
import platform

def generar_requirements_txt():
    contenido = "eel==0.16.0\n"
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ requirements.txt generado")

def generar_launcher_bat():
    contenido = '@echo off\n'
    contenido += 'chcp 65001 >nul\n'
    contenido += 'title Linux Desktop Editor\n'
    contenido += 'color 0C\n'
    contenido += '\n'
    contenido += 'echo ========================================\n'
    contenido += 'echo  🎨 Linux Desktop Editor\n'
    contenido += 'echo ========================================\n'
    contenido += 'echo.\n'
    contenido += 'echo  Iniciando el editor de escritorio...\n'
    contenido += 'echo.\n'
    contenido += '\n'
    contenido += 'REM Verificar Python\n'
    contenido += 'python --version >nul 2>&1\n'
    contenido += 'if errorlevel 1 (\n'
    contenido += '    echo ❌ Python no esta instalado.\n'
    contenido += '    echo.\n'
    contenido += '    echo Por favor, instala Python desde:\n'
    contenido += '    echo https://www.python.org/downloads/\n'
    contenido += '    echo.\n'
    contenido += '    pause\n'
    contenido += '    exit /b 1\n'
    contenido += ')\n'
    contenido += '\n'
    contenido += 'REM Instalar Eel\n'
    contenido += 'echo 📦 Instalando dependencias...\n'
    contenido += 'pip install eel >nul 2>&1\n'
    contenido += '\n'
    contenido += 'REM Iniciar aplicación\n'
    contenido += 'echo 🚀 Abriendo el editor...\n'
    contenido += 'echo.\n'
    contenido += 'python main.py\n'
    contenido += '\n'
    contenido += 'pause\n'
    
    with open('launcher.bat', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ launcher.bat generado")

def generar_launcher_sh():
    contenido = '#!/bin/bash\n'
    contenido += '\n'
    contenido += 'echo "========================================="\n'
    contenido += 'echo " 🎨 Linux Desktop Editor"\n'
    contenido += 'echo "========================================="\n'
    contenido += 'echo " Iniciando el editor de escritorio..."\n'
    contenido += 'echo\n'
    contenido += '\n'
    contenido += '# Verificar Python\n'
    contenido += 'if ! command -v python3 &> /dev/null; then\n'
    contenido += '    echo "❌ Python3 no esta instalado."\n'
    contenido += '    echo "Instálalo con: sudo apt install python3 (Debian/Ubuntu)"\n'
    contenido += '    echo "o sudo dnf install python3 (Fedora)"\n'
    contenido += '    exit 1\n'
    contenido += 'fi\n'
    contenido += '\n'
    contenido += '# Instalar Eel\n'
    contenido += 'echo "📦 Instalando dependencias..."\n'
    contenido += 'pip3 install eel > /dev/null 2>&1\n'
    contenido += '\n'
    contenido += '# Iniciar aplicación\n'
    contenido += 'echo "🚀 Abriendo el editor..."\n'
    contenido += 'python3 main.py\n'
    
    with open('launcher.sh', 'w', encoding='utf-8') as f:
        f.write(contenido)
    if platform.system() != 'Windows':
        os.chmod('launcher.sh', 0o755)
    print("✅ launcher.sh generado")

def generar_readme():
    """Genera el archivo README.md"""
    contenido = '# 🎨 Linux Desktop Editor\n'
    contenido += '\n'
    contenido += 'Editor de escritorio para Linux que permite personalizar y generar instaladores.\n'
    contenido += '\n'
    contenido += '## 📋 Requisitos\n'
    contenido += '\n'
    contenido += '- Python 3.6 o superior\n'
    contenido += '- Windows, Linux o macOS\n'
    contenido += '\n'
    contenido += '## 🚀 Instalación\n'
    contenido += '\n'
    contenido += '1. **Clonar o descargar el proyecto**\n'
    contenido += '\n'
    contenido += '2. **Instalar dependencias**:\n'
    contenido += '```bash\n'
    contenido += 'pip install -r requirements.txt\n'
    contenido += '```\n'
    contenido += '\n'
    contenido += '3. **Ejecutar el editor**:\n'
    contenido += '```bash\n'
    contenido += 'python main.py\n'
    contenido += '```\n'
    contenido += '\n'
    contenido += '## 🛠️ Características\n'
    contenido += '\n'
    contenido += '- 🎨 Personalización del tema (claro/oscuro)\n'
    contenido += '- 📐 Configuración del dock (posición, tamaño, transparencia)\n'
    contenido += '- 📱 Generación de archivos de instalación\n'
    contenido += '- 🖥️ Soporte para múltiples arquitecturas\n'
    contenido += '- 📦 Exportación a ZIP\n'
    contenido += '\n'
    contenido += '## 📁 Estructura del proyecto\n'
    contenido += '\n'
    contenido += '```\n'
    contenido += 'Linux-Desktop-Editor/\n'
    contenido += '├── main.py                 # Archivo principal\n'
    contenido += '├── modulos_py/            # Módulos Python\n'
    contenido += '│   ├── requerimientos.py   # Generador de archivos\n'
    contenido += '│   └── theme_generator.py  # Generador de temas\n'
    contenido += '├── templates/             # Interfaz HTML\n'
    contenido += '│   └── index.html\n'
    contenido += '├── generated_configs/     # Configuraciones generadas\n'
    contenido += '├── requirements.txt       # Dependencias\n'
    contenido += '├── launcher.bat          # Lanzador para Windows\n'
    contenido += '├── launcher.sh           # Lanzador para Linux\n'
    contenido += '└── README.md             # Este archivo\n'
    contenido += '```\n'
    contenido += '\n'
    contenido += '## 📝 Uso\n'
    contenido += '\n'
    contenido += '1. Ejecuta el lanzador correspondiente a tu sistema:\n'
    contenido += '   - Windows: `launcher.bat`\n'
    contenido += '   - Linux: `./launcher.sh`\n'
    contenido += '\n'
    contenido += '2. Configura las opciones de personalización\n'
    contenido += '\n'
    contenido += '3. Haz clic en "Generar configuración"\n'
    contenido += '\n'
    contenido += '4. Descarga el archivo ZIP generado\n'
    contenido += '\n'
    contenido += '5. Ejecuta el script de instalación en tu sistema Linux\n'
    contenido += '\n'
    contenido += '## 🤝 Contribuir\n'
    contenido += '\n'
    contenido += 'Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.\n'
    contenido += '\n'
    contenido += '## 📄 Licencia\n'
    contenido += '\n'
    contenido += 'Este proyecto está bajo la Licencia MIT.\n'
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ README.md generado")

def generar_gitignore():
    """Genera el archivo .gitignore"""
    contenido = '# Python\n'
    contenido += '__pycache__/\n'
    contenido += '*.py[cod]\n'
    contenido += '*$py.class\n'
    contenido += '*.so\n'
    contenido += '.Python\n'
    contenido += 'env/\n'
    contenido += 'venv/\n'
    contenido += 'ENV/\n'
    contenido += 'build/\n'
    contenido += 'develop-eggs/\n'
    contenido += 'dist/\n'
    contenido += 'downloads/\n'
    contenido += 'eggs/\n'
    contenido += '.eggs/\n'
    contenido += 'lib/\n'
    contenido += 'lib64/\n'
    contenido += 'parts/\n'
    contenido += 'sdist/\n'
    contenido += 'var/\n'
    contenido += 'wheels/\n'
    contenido += '*.egg-info/\n'
    contenido += '.installed.cfg\n'
    contenido += '*.egg\n'
    contenido += 'MANIFEST\n'
    contenido += '\n'
    contenido += '# Eel\n'
    contenido += '*.pyc\n'
    contenido += 'templates/__pycache__/\n'
    contenido += '\n'
    contenido += '# Configuraciones generadas\n'
    contenido += 'generated_configs/\n'
    contenido += '*.zip\n'
    contenido += '\n'
    contenido += '# IDE\n'
    contenido += '.vscode/\n'
    contenido += '.idea/\n'
    contenido += '*.swp\n'
    contenido += '*.swo\n'
    contenido += '*~\n'
    contenido += '.DS_Store\n'
    contenido += '\n'
    contenido += '# Logs\n'
    contenido += '*.log\n'
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ .gitignore generado")

# ============================================================
# FUNCIÓN PRINCIPAL PARA GENERAR TODOS LOS ARCHIVOS
# ============================================================

def generar_todos_los_archivos():
    """
    Genera todos los archivos necesarios para el proyecto
    """
    print("=" * 50)
    print("📦 Generando archivos del proyecto...")
    print("=" * 50)
    print()
    
    generar_requirements_txt()
    generar_launcher_bat()
    generar_launcher_sh()
    generar_readme()
    generar_gitignore()
    
    print()
    print("=" * 50)
    print("✅ Todos los archivos generados exitosamente!")
    print("=" * 50)
    print()
    print("📁 Archivos generados:")
    print("   ✅ requirements.txt")
    print("   ✅ launcher.bat (Windows)")
    print("   ✅ launcher.sh (Linux)")
    print("   ✅ README.md")
    print("   ✅ .gitignore")
    print()
    print("🚀 Para ejecutar la aplicación:")
    print("   Windows: Ejecuta 'launcher.bat'")
    print("   Linux:   Ejecuta './launcher.sh'")
    print()

# ============================================================
# EJECUCIÓN DIRECTA DEL MÓDULO
# ============================================================

if __name__ == '__main__':
    generar_todos_los_archivos()