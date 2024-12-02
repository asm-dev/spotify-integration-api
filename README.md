# Spotify Integration API

API RESTful para consultar canciones/artistas mediante la integración con Spotify, desarrollada con FastAPI.

## Instalación

### Requisitos
- Python 3.8 o superior.
- Cuenta de desarrollador de Spotify para obtener `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` y `SPOTIFY_REDIRECT`.

### Configuración
1. Clona el repositorio en tu máquina local:
   ```bash
   git clone <URL del repositorio>
   cd <directorio del proyecto>

1.  ```bashCopy codepython -m venv envsource env/bin/activate # En Windows usa env\\Scripts\\activate
    
2.  ```bashCopy codepip install -r requirements.txt
    
3.  makefileCopy codeSPOTIFY\_CLIENT\_ID=SPOTIFY\_CLIENT\_SECRET=SPOTIFY\_REDIRECT=**Nota**: El SPOTIFY\_REDIRECT debe coincidir con el configurado en el portal de desarrolladores de Spotify.
    

### Uso

1.  ```bashpython launch.py

Esto lanzará el servidor en http://127.0.0.1:8000.
    
2.  Accede a la documentación interactiva generada automáticamente por FastAPI en Swagger UI: http://127.0.0.1:8000/docs
        

Endpoints Principales
---------------------

### 1\. Buscar canciones o artistas en Spotify

*   **Ruta**: /search
    
*   **Método**: GET
    
*   **Descripción**: Busca canciones o artistas según un término de búsqueda.
    
*   **Parámetros**:
    
    *   q: Término de búsqueda (obligatorio).
        
    *   type: Tipo de búsqueda (track, artist, etc.).
        
    *   limit: Número máximo de resultados (por defecto, 10).
        

### 2\. Obtener las canciones más reproducidas del usuario

*   **Ruta**: /top-tracks
    
*   **Método**: GET
    
*   **Descripción**: Recupera las canciones más escuchadas del usuario.
    
*   **Parámetros**:
    
    *   time\_range: Rango de tiempo (short\_term, medium\_term, long\_term).
        
    *   limit: Número máximo de resultados (por defecto, 10).
        

### 3\. Login y manejo de autenticación con Spotify

*   **Ruta**: /login y /callback
    
*   **Método**: GET
    
*   **Descripción**:
    
    *   /login: Redirige al usuario a Spotify para autenticar.
        
    *   /callback: Procesa el código de autorización y almacena los tokens de acceso.
        

Separación de Responsabilidades (SSP)
-------------------------------------

### spotify\_service.py

Este archivo maneja toda la lógica relacionada con la API de Spotify:

*   Generación de la URL de autorización.
    
*   Obtención y almacenamiento de tokens de acceso.
    
*   Refresco del token cuando expira.
    

### main.py

Este archivo define los endpoints de la API y gestiona la lógica de enrutamiento. Utiliza las funciones de spotify\_service.py para interactuar con Spotify, delegando la responsabilidad de autenticación y manejo de tokens.

Pruebas
-------

### Probar los Endpoints

1.  ```bashpython launch.py
    
2.  **Probar usando RapidAPI**:
    
    *   ```bashGET "http://127.0.0.1:8000/search?q=Coldplay&type=artist&limit=5"
        
    *   ```bashGET "http://127.0.0.1:8000/top-tracks?time\_range=medium\_term&limit=5"
        
    *   **Login**:Navega a http://127.0.0.1:8000/login para autenticar con Spotify.
        
3.  **Probar desde Swagger UI**:Abre http://127.0.0.1:8000/docs y utiliza los endpoints interactivos para enviar parámetros y ver respuestas.
