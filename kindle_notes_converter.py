import sys
import os
from bs4 import BeautifulSoup

def clean_text(text):
    """Limpia espacios extra y saltos de línea del texto."""
    return ' '.join(text.split()).strip()

def convert_kindle_html_to_markdown(input_html_path, output_md_path):
    """
    Convierte un archivo HTML de anotaciones de Kindle a Markdown
    con una estética personalizada.
    Retorna 0 si es exitoso, 1 si hay un error.
    """
    try:
        with open(input_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: El archivo de entrada no se encontró en '{input_html_path}'")
        return 1
    except Exception as e:
        print(f"ERROR: Al leer el archivo HTML: {e}")
        return 1

    soup = BeautifulSoup(html_content, 'lxml')
    markdown_output = []

    # 1. Extraer Título del Libro
    book_title_tag = soup.find('div', class_='bookTitle')
    if book_title_tag:
        book_title = clean_text(book_title_tag.get_text())
        markdown_output.append(f"# {book_title}\n")
    else:
        book_title = "Título Desconocido"
        markdown_output.append("# Título Desconocido (No se encontró el título del libro)\n")

    markdown_output.append("---\n") # Separador inicial

    # 2. Recorrer el contenido principal (bodyContainer)
    body_container = soup.find('div', class_='bodyContainer')
    if not body_container:
        print("ERROR: No se encontró el contenedor principal 'bodyContainer'.")
        return 1

    current_section_title = None
    
    all_content_divs = body_container.find_all(['div'], class_=['sectionHeading', 'noteHeading', 'noteText'])

    i = 0
    while i < len(all_content_divs):
        element = all_content_divs[i]

        if 'sectionHeading' in element.get('class', []):
            section_text = clean_text(element.get_text())
            if section_text != current_section_title:
                current_section_title = section_text
            i += 1
            continue

        if 'noteHeading' in element.get('class', []):
            note_heading_text = clean_text(element.get_text())
            
            j = i + 1
            note_content_tag = None
            while j < len(all_content_divs) and 'noteText' not in all_content_divs[j].get('class', []):
                j += 1
            
            if j < len(all_content_divs) and 'noteText' in all_content_divs[j].get('class', []):
                note_content = clean_text(all_content_divs[j].get_text())
            else:
                # No se encontró noteText después del noteHeading, saltar
                print(f"ADVERTENCIA: noteHeading sin noteText encontrado en la posición {i}: '{note_heading_text}'. Saltando.")
                i += 1
                continue

            # Extracción del título de la sección y la página del noteHeading
            parts = note_heading_text.split(' > ')
            page_info = ""
            section_in_highlight_heading = ""

            if len(parts) > 1:
                page_part = parts[-1].strip()
                if page_part.lower().startswith('page'):
                    page_info = page_part
                
                section_raw = ' > '.join(parts[:-1])
                
                if note_heading_text.startswith("Highlight"):
                    section_in_highlight_heading = section_raw.split(' - ', 1)[1].strip() if ' - ' in section_raw else ""
                elif note_heading_text.startswith("Note"):
                    section_in_highlight_heading = section_raw.split(' - ', 1)[1].strip() if ' - ' in section_raw else ""
                
            # Aplicar la lógica de agrupación por sección antes de añadir la anotación
            if section_in_highlight_heading and section_in_highlight_heading != current_section_title:
                markdown_output.append(f"\n## {section_in_highlight_heading}\n")
                current_section_title = section_in_highlight_heading
            
            # Formatear la anotación (Highlight o Note)
            if note_heading_text.startswith("Highlight"):
                markdown_output.append(f">[!quote] {page_info}\n>\n> {note_content}\n\n") # Doble salto de línea
                
            elif note_heading_text.startswith("Note"):
                markdown_output.append(f"**Note**\n- {note_content}\n\n") # Doble salto de línea
            
            i = j + 1
            continue
        
        i += 1

    # Guardar el archivo Markdown
    try:
        # Asegurarse de que el directorio de salida exista
        output_dir = os.path.dirname(output_md_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(''.join(markdown_output))
        print(f"INFO: Conversión completada exitosamente. Archivo guardado en: {output_md_path}")
        return 0
    except Exception as e:
        print(f"ERROR: Al escribir el archivo Markdown: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: Uso incorrecto.")
        print("Uso: python kindle_notes_converter.py <ruta_archivo_html_entrada> <ruta_archivo_md_salida>")
        print("Ejemplo: python kindle_notes_converter.py C:\\Users\\Wilber\\Documents\\KindleNotes.html C:\\Users\\Wilber\\Downloads\\MyBookNotes.md")
        sys.exit(1)

    input_html = sys.argv[1]
    output_md = sys.argv[2]

    # No necesitamos esta lógica de inferir el nombre del archivo de salida aquí
    # porque el PowerShell le pasará la ruta COMPLETA del archivo de salida.
    
    # Ejecutar la conversión y salir con el código de retorno
    exit_code = convert_kindle_html_to_markdown(input_html, output_md)
    sys.exit(exit_code)