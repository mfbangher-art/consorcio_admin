#!/usr/bin/env python3
"""
setup.py – Crea la estructura mínima del proyecto y algunos archivos de ejemplo.
"""

import os
import sys
import textwrap

# ----------------------------------
# 1. Directorios que necesitaremos
# ----------------------------------
dirs = [
    "templates",
    "static/css",
    "static/js",
    "static/img",
    "pdf",
    "models",
    "views",
    "utils",
]

# ----------------------------------
# 2. Archivos de ejemplo
# ----------------------------------
files = {
    "main.py": textwrap.dedent("""
        # main.py – Punto de entrada del proyecto
        import sys
        from pathlib import Path

        def main():
            print("¡Consorcio Admin está listo!")
            # Aquí iría el código de la aplicación (GUI, API, etc.)

        if __name__ == "__main__":
            main()
    """),

    "requirements.txt": textwrap.dedent("""
        PyQt5
        reportlab
    """),

    "README.md": textwrap.dedent("""
        # Consorcio Admin
        Proyecto mínimo para gestionar expensas y PDFs.
    """),

    "pdf/template.pdf": textwrap.dedent("""
        (Este es un placeholder vacío. Reemplázalo con tu PDF real.)
    """),
}

# ----------------------------------
# 3. Crear directorios
# ----------------------------------
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Creado directorio: {d}")

# ----------------------------------
# 4. Crear archivos de ejemplo
# ----------------------------------
for filename, content in files.items():
    # Si el archivo está dentro de una subcarpeta, crea la ruta completa
    full_path = Path(filename)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Creado archivo: {full_path}")

print("\nEstructura inicial creada con éxito.")

