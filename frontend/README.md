# TestMind Frontend

Este proyecto es el frontend de la aplicación **TestMind**, diseñado para interactuar con el backend y proporcionar una interfaz de usuario para la generación de casos de prueba basados en archivos Excel y tickets de Jira. Está construido con **React** y utiliza **Ant Design** para los componentes de la interfaz.

## Estructura del Proyecto
```
frontend/ ├── .gitignore # Archivos ignorados por Git ├── docker-compose.yml # Configuración de Docker Compose ├── Dockerfile # Configuración de Docker para el frontend ├── eslint.config.js # Configuración de ESLint ├── index.html # Archivo HTML principal ├── package.json # Dependencias del proyecto ├── vite.config.js # Configuración de Vite ├── public/ # Archivos públicos │ └── vite.svg # Icono de Vite ├── src/ # Código fuente principal │ ├── App.css # Estilos globales de la aplicación │ ├── App.jsx # Componente principal de la aplicación │ ├── index.css # Estilos globales │ ├── main.jsx # Punto de entrada de la aplicación │ ├── api/ # Módulos para llamadas a la API │ │ ├── api.js # Funciones para interactuar con el backend │ │ └── axiosInstance.js # Configuración de Axios │ ├── assets/ # Recursos estáticos │ │ └── react.svg # Icono de React │ ├── components/ # Componentes de la interfaz │ │ ├── ResultComponent.jsx # Componente para mostrar resultados │ │ ├── SegmentedComponent.jsx # Componente para controles segmentados │ │ └── StepsComponent.jsx # Componente principal de pasos
```

## Instalación

### Requisitos

- **Node.js 20**
- **npm** o **yarn**

### Pasos

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd frontend

2. Instala las dependencias:
    `npm install`

3. Inicia el servidor de desarrollo:
    `npm run dev`

4. Accede a la aplicación en:
    `http://localhost:5173`

Configuración
Variables de Entorno
El frontend utiliza un archivo de configuración para Axios (axiosInstance.js) que define la URL base del backend. Por defecto, está configurado para http://localhost:8000.

Si necesitas cambiar la URL base, edita el archivo:
```
    // [axiosInstance.js](http://_vscodecontentref_/14)
    const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 200000,
    });
```

Docker
Construcción y Ejecución
1. Construye y ejecuta el contenedor con Docker Compose:
    `docker-compose up --build`

2. Accede a la aplicación en:
    `http://localhost:5173`


Servicios
Frontend: Disponible en `http://localhost:5173`.
Funcionalidades
Componentes Principales
StepsComponent: Componente principal que guía al usuario a través de los pasos para subir archivos, seleccionar tickets de Jira y generar casos de prueba.
SegmentedComponent: Control segmentado para alternar entre opciones.
ResultComponent: Muestra el resultado de las acciones realizadas (éxito o error).
Integración con el Backend
El frontend interactúa con el backend mediante los siguientes endpoints:

* `GET /excel/list`: Listar archivos Excel disponibles.
* `POST /excel/upload`: Subir un archivo Excel.
* `GET /jira/issues`: Obtener tickets de Jira según filtros.
* `POST /test-cases/generate`: Generar casos de prueba basados en un archivo Excel y tickets de Jira.
Pruebas
Actualmente, no se han configurado pruebas automatizadas para el frontend.

Desarrollo
Linter
Ejecuta el linter para verificar errores de estilo y código:
`npm run lint`

Construcción para Producción
Genera una versión optimizada para producción:
`npm run build`