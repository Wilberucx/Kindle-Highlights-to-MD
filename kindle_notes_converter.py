# kindle_notes_converter.py (v3 - El más intuitivo)
import sys
import os
import json
from bs4 import BeautifulSoup

# ... (la función clean_text sigue igual) ...
def clean_text(text):
    return ' '.join(text.split()).strip()

def load_config(config_path):
    # ... (esta función no necesita cambios) ...
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Archivo de configuracion no encontrado en '{config_path}'")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: El archivo de configuracion '{config_path}' tiene un formato JSON invalido.")
        return None

# --- ¡AQUÍ ESTÁ LA NUEVA LÓGICA! ---
def apply_template(template_lines, data):
    """
    Aplica datos a una lista de líneas de plantilla y las une en un string final.
    """
    processed_lines = []
    for line in template_lines:
        # Reemplaza los placeholders en cada línea individualmente
        for key, value in data.items():
            line = line.replace(f"{{{key}}}", str(value))
        processed_lines.append(line)
    
    # Une las líneas procesadas con saltos de línea para crear el bloque de texto final
    return '\n'.join(processed_lines)

# ... (El resto del script, como convert_kindle_html_to_markdown, necesita un pequeño ajuste) ...

def convert_kindle_html_to_markdown(input_html_path, output_md_path, config):
    # ... (lectura de HTML y sopa BeautifulSoup sin cambios) ...
    try:
        with open(input_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: El archivo de entrada no se encontro en '{input_html_path}'")
        return 1

    soup = BeautifulSoup(html_content, 'lxml')
    templates = config.get('templates', {})
    markdown_output = []

    # 1. Título del Libro
    book_title_tag = soup.find('div', class_='bookTitle')
    book_title = clean_text(book_title_tag.get_text()) if book_title_tag else "Título Desconocido"
    # --- Pequeño ajuste aquí ---
    # Ahora pasamos la lista de líneas de la plantilla a apply_template
    markdown_output.append(apply_template(templates.get('bookTitle', ['# {book_title}']), {'book_title': book_title}) + "\n\n")

    markdown_output.append("---\n")

    # 2. Procesar notas y highlights
    all_notes = soup.find_all('div', class_='noteText')
    current_section = ""

    for note_element in all_notes:
        # ... (la lógica de extracción de datos no cambia) ...
        note_content = clean_text(note_element.get_text())
        heading_element = note_element.find_previous_sibling('div', class_='noteHeading')
        if not heading_element: continue
        heading_text = clean_text(heading_element.get_text())
        note_type = "highlight" if heading_text.lower().startswith('highlight') else "note"
        page_info = ""
        section_title = ""
        parts = heading_text.split(' > ')
        if len(parts) > 1:
            page_info = parts[-1].strip()
            section_raw = ' > '.join(parts[:-1]).split(' - ', 1)[-1]
            section_title = section_raw.strip()

        # Agrupar por sección
        if section_title and section_title != current_section:
            current_section = section_title
            # --- Pequeño ajuste aquí ---
            markdown_output.append(apply_template(templates.get('sectionHeading', ['', '## {section_title}', '']), {'section_title': current_section}))
        
        # Aplicar plantilla correspondiente
        template_data = {'page_info': page_info, 'content': note_content}
        # --- Pequeño ajuste aquí ---
        # El fallback también es una lista de líneas ahora
        template_lines = templates.get(note_type, ['> {content}']) 
        markdown_output.append(apply_template(template_lines, template_data) + "\n\n")

    # ... (La parte de guardar el archivo no cambia) ...
    try:
        output_dir = os.path.dirname(output_md_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(''.join(markdown_output))
        print(f"INFO: Conversion completada. Archivo guardado en: {output_md_path}")
        return 0
    except Exception as e:
        print(f"ERROR: Al escribir el archivo Markdown: {e}")
        return 1

# ... (El bloque if __name__ == "__main__": no necesita cambios) ...
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("ERROR: Uso incorrecto.")
        print("Uso: python kindle_notes_converter.py <entrada.html> <salida.md> <config.json>")
        sys.exit(1)
    config = load_config(sys.argv[3])
    if not config:
        sys.exit(1)
    exit_code = convert_kindle_html_to_markdown(sys.argv[1], sys.argv[2], config)
    sys.exit(exit_code)