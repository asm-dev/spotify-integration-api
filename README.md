# Spotify Integration API

API RESTful para consultar canciones/artistas y las canciones favoritas del usuario mediante la integración con Spotify. Desarrollada con FastAPI.

## Instalación

### Requisitos
- Python 3.8 o superior.
- Cuenta de desarrollador de Spotify para obtener el client ID y client secret de la API.

### Configuración
1. Clona el repositorio    
2. Crea un fichero .env en el que agreges
   
   ```
   SPOTIFY_CLIENT_ID="tu client ID"
   SPOTIFY_CLIENT_SECRET="tu client secret"
   ```
3. Instala las dependencias. Es posible que al instalar alguna de ellas se instalen también librerías asociadas. Puedes realizar la instalación con este comando:

   ```bash
   pip install -r requirements.txt
   
### Uso

Lanza el servidor en `http://127.0.0.1:8000` mediante el siguiente comando:
1.  ```bash
    python launch.py
    
2. Explora la aplicación. Puedes acceder a documentación interatviva autogenerada por FastAPI en Swagger UI en `http://127.0.0.1:8000/docs`


Principios SOLID aplicados al proyecto 
-------------------------------------

### Separación de Responsabilidades (SSP)

main.py define los endpoints de la API y la lógica de enrutamiento, delegando a spotify\_service.py el manejo de toda la lógica relativa a la API de Spotify, por ejemplo, el almacenamiento y refresco del token de acceso cuando expira.

    
Endpoints Principales
---------------------

### 1\. Login y callback

*   **Ruta**: /login y /callback
    
*   **Método**: GET
    
*   **Descripción**: Manejan la autenticación del usuario, apoyándose en funcionalidad recogida en el `spotify_service.py` (SSP)
    
    *   /login: Redirige al usuario a Spotify para autenticar.
        
    *   /callback: Procesa el código de autorización y almacena los tokens de acceso a la API.

### 2\. Buscar canciones o artistas en Spotify

*   **Ruta**: /search
    
*   **Método**: GET
    
*   **Descripción**: En base a un término de búsqueda `q` busca canciones o artistas. El parámetro de búsqueda `type` permite buscar por "track", "artist", etc. por defecto se busca canciones. `limit` refiere al número máximo de resultados (por defecto 5)
    

### 3\. Obtener las canciones más reproducidas del usuario

*   **Ruta**: /top-tracks
    
*   **Método**: GET
    
*   **Descripción**: Recupera las canciones más escuchadas del usuario. Por defecto este endpoint devuelve el top 10 de canciones escuchadas en los últimos 6 meses, pero puede modificarse cambiando `time_range` a short\_term o long\_term, y el número de resultados seteando `limit`.
        

Pruebas
-------

### Probar con RapidAPI

1.  ```bashpython launch.py
    
2.  **Probar usando RapidAPI**:
    
    * **Login**: antes que nada navega a http://127.0.0.1:8000/login para autenticar con Spotify.
    *   ```
        GET "http://127.0.0.1:8000/search?q=Coldplay&type=artist&limit=5"
        
    *   ```
        GET "http://127.0.0.1:8000/top-tracks?time\_range=medium\_term&limit=5"
        
3.  **Probar desde Swagger UI**:Abre http://127.0.0.1:8000/docs y utiliza los endpoints interactivos para enviar parámetros y ver respuestas.
