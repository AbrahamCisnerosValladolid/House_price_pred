import os
import agentql
import csv
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time

# Cargar variables de entorno desde el archivo .env
load_dotenv()
os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")

URL = "https://www.realtor.com/international/mx/tijuana-baja-california/p1"

HOUSE_POSTS_QUERY = """
{
    house_posts[]{
        address
        property_type
        parking_spaces
        land_size
        building_size
        num_bedrooms
        num_bathrooms
        price
    }
}
"""

PAGINATION_QUERY = """
{
    pagination{
         next_page_btn
    }
}
"""

CSV_FILENAME = "house_posts.csv"

def save_to_csv(house_posts_data):
    # Definir los nombres de los campos según la estructura de los datos
    fieldnames = [
        'address', 
        'property_type', 
        'parking_spaces', 
        'land_size', 
        'building_size', 
        'num_bedrooms', 
        'num_bathrooms', 
        'price'
    ]
    
    # Verificar si el archivo ya existe para saber si se debe escribir la cabecera
    file_exists = os.path.isfile(CSV_FILENAME)
    
    with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Escribir la cabecera solo si es la primera vez
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(house_posts_data)
    
    print(f"Se han guardado {len(house_posts_data)} registros en {CSV_FILENAME}")

def accumulate_unique_posts(existing_posts, new_posts):
    """
    Combina registros nuevos con los existentes, evitando duplicados.
    Se asume que cada registro es un diccionario.
    """
    for post in new_posts:
        # Si el registro no se encuentra en la lista, se agrega.
        if post not in existing_posts:
            existing_posts.append(post)
    return existing_posts

def wait_for_house_posts(page, expected_count=25, max_attempts=10):
    """
    Acumula registros únicos (sin duplicados) de house_posts en varios intentos.
    - Si existe el botón "siguiente", se espera acumular 'expected_count' registros.
    - En la última página (sin botón "siguiente"), se retorna lo que se tenga.
    """
    unique_posts = []
    
    for attempt in range(max_attempts):
        # Realizar scroll hasta el final para activar cargas diferidas (lazy load)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)  # Esperar 1 segundo para que se carguen los elementos
        
        # Consultar los registros de house_posts
        house_posts_response = page.query_elements(HOUSE_POSTS_QUERY)
        new_data = house_posts_response.house_posts.to_data()
        
        # Acumular registros únicos
        unique_posts = accumulate_unique_posts(unique_posts, new_data)
        
        # Verificar si es la última página consultando el botón de "siguiente"
        paginations = page.query_elements(PAGINATION_QUERY)
        next_page_btn = paginations.pagination.next_page_btn

        if next_page_btn is None:
            print(f"Última página detectada. Registros únicos acumulados: {len(unique_posts)}")
            return unique_posts
        
        if len(unique_posts) >= expected_count:
            print(f"Intento {attempt+1}: Se han acumulado {len(unique_posts)} registros únicos.")
            # Retornar solo los primeros expected_count registros
            return unique_posts[:expected_count]
        else:
            print(f"Intento {attempt+1}: Registros únicos acumulados hasta ahora: {len(unique_posts)}. Esperando más...")
            time.sleep(0.5)
    
    # Si se agotaron los intentos, se retorna lo acumulado (aunque sea menor a expected_count)
    return unique_posts

def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        context = browser.new_context()
        page = agentql.wrap(context.new_page())
        
        page.goto(URL)
        status = True

        while status:
            current_url = page.url

            # Acumular registros únicos de la página actual hasta obtener 25 (o lo que se tenga en la última página)
            house_posts_data = wait_for_house_posts(page, expected_count=25, max_attempts=10)
            print(f"Se han obtenido {len(house_posts_data)} registros únicos en esta página:")
            print(house_posts_data)
            
            # Guardar los registros obtenidos en CSV
            save_to_csv(house_posts_data)

            # Manejar la paginación
            paginations = page.query_elements(PAGINATION_QUERY)
            next_page_btn = paginations.pagination.next_page_btn

            if next_page_btn:
                try:
                    next_page_btn.click()
                except Exception as e:
                    print("Error al hacer click en el botón de siguiente:", e)
                    break

                # Esperar a que la página se estabilice
                page.wait_for_load_state('networkidle')
                # Si la URL no cambia, significa que no hay más páginas
                if current_url == page.url:
                    status = False
            else:
                status = False
        
        browser.close()

if __name__ == "__main__":
    # Eliminar el archivo CSV existente para iniciar una nueva ejecución (opcional)
    if os.path.exists(CSV_FILENAME):
        os.remove(CSV_FILENAME)
    main()
