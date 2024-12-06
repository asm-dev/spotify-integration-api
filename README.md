# Spotify Integration API

API RESTful para consultar canciones/artistas y realizar operaciones CRUD con las canciones favoritas del usuario mediante la integración con Spotify. Desarrollada con FastAPI.

![Screenshot 2024-12-06 192528](https://github.com/user-attachments/assets/5ef2576b-5d35-48f1-b6d0-aefbe5f13339)

## Instalación

### Requisitos
- Python 3.8 o superior.
- Cuenta de desarrollador de Spotify para obtener el client ID y client secret de la API.

### Configuración
1. Clona el repositorio.
2. Crea un fichero .env y agrega tus datos de acceso a la API de Spotify.
   
   ```
   SPOTIFY_CLIENT_ID="tu client ID"
   SPOTIFY_CLIENT_SECRET="tu client secret"
   ```
3. Instala las dependencias. Es posible que al instalar alguna de ellas se instalen también librerías asociadas.

   ```bash
   pip install -r requirements.txt
   
### Uso

1. Lanza el servidor en `http://127.0.0.1:8000` mediante el siguiente comando:
   ```
   python launch.py
   ```
2. Una vez resuelto el login deberías ser redirigido automáticamente `/login`, pero si no fuera así debido a la configuración de tu IDE o equipo, por favor accede manualmente. Este paso es muy importante, ya que sin el token no podrás acceder a los endpoints.

3. Explora la aplicación.

   - Puedes acceder a documentación interactiva autogenerada por FastAPI en Swagger UI en `http://127.0.0.1:8000/docs`. Alternativamente, puedes usar extensiones como RapidAPI.
   
   - Si quieres hacer una prueba rápida de comportamiento puedes probar a ir a `http://127.0.0.1:8000/search?q=Coldplay&type=artist&limit=5` o `http://localhost:8000/top-tracks?time_range=short_term&limit=3`
   
   - `/save-top-tracks` permite almacenar tus canciones favoritas en un JSON. Puedes crear, leer, eliminar o updatar estas canciones utilizando varios endpoints presentes en la aplicación.
   
&nbsp;

## Endpoints Principales

**Login y callback**, GET:
    
*   Manejan la autenticación del usuario, apoyándose en funcionalidad recogida en el `spotify_service.py` (SSP)
    
    *   `/login`: Redirige al usuario a Spotify para autenticar.
        
    *   `/callback`: Procesa el código de autorización y almacena los tokens de acceso a la API.

**Buscar canciones o artistas en Spotify**, GET:

*   `/search`: en base a un término de búsqueda `q` busca canciones o artistas. El parámetro de búsqueda `type` permite buscar por "track", "artist", etc. por defecto se busca canciones. `limit` refiere al número máximo de resultados (por defecto 5)
    

**Obtener las canciones más reproducidas del usuario**, GET:
    
*   `/top-tracks`: recupera las canciones más escuchadas del usuario. Por defecto este endpoint devuelve el top 10 de canciones escuchadas en los últimos 6 meses, pero puede modificarse cambiando `time_range` a short\_term o long\_term, y el número de resultados seteando `limit`.


**Guardar las canciones más reproducidas del usuario**, GET:

*   `/save-top-tracks`: obtiene las canciones más escuchadas del usuario desde el servicio de Spotify utilizando el endpoint `/top-tracks`. Las canciones recibidas se guardan en un archivo `user_songs.json`. Cada canción es añadida al archivo utilizando el endpoint `POST /songs`, lo que permite mantener una lista actualizada de las canciones favoritas del usuario.

**Operaciones CRUD en una lista de canciones**

*   **Create**, POST: `/songs`

*   **Read**, GET:  `/songs` y `/songs/{song_id}`

*   **Update**, PUT: `/songs/{song_id}`

*   **Delete**, DELETE: /songs y /songs/{song_id}

&nbsp;

## Aplicación de principios SOLID 

- **Responsabilidad Única**, SRP:  
   - `main.py` se enfoca en manejar la API REST y las interacciones del usuario.
   - `spotify_service.py` gestiona la comunicación con la API de Spotify, por ejemplo, la gestión del token de acceso.

- **Abierto/Cerrado**, Open/Closed: es fácil agregar nuevos endpoints o servicios sin necesidad de cambiar la funcionalidad existente, lo que facilita la expansión.

- **Sustitución de Liskov**, Liskov Substitution: aunque no se usa clases, se siguen principios de diseño modular ya que los módulos o componentes podrían ser sustituidos por otros sin afectar la duncionalidad de los demás.

- **Segregación de Interfaces**, Interface Segregation: cada función tiene una responsabilidad clara y especializada, por ejemplo `generate_auth_url`.

- **Inversión de Dependencias**, Dependency Inversion: la lógica de `main.py`está desacoplada de los detalles de la implementación de la lógica de la API de Spotify en el servicio `spotify_service.py`.

