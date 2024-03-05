# PDA

Repositorio con código base para el desarrollo de una arquitectura hexagonal siguiendo los principios y patrones de DDD.


## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma:

- **src**: En este directorio encuentra el código fuente para Propiedades de los Alpes.
- **src/pda**: En este directorio se encuentra el código fuente para la aplicación Flask.
- **src/notifications**: En este directorio se encuentra el código fuente para el módulo de notificaciones.
- **src/ui**: En este directorio se encuentra el código fuente para la app web/interfaz gráfica.
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **.gitpod.yml**: Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Gitpod
- **README.md**: El archivo que está leyendo
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms pda (librerias Python)
- **notification-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms notifications (librerias Python)
- **ui-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms ui (librerias Python)

## Escenarios de calidad a probar
- Escenario #9: Modificabilidad
- Escenario #2: Escalabilidad
- Escenario #6: Disponibilidad

## Video - Entrega 3

[](https://github.com/lmaero/MISW4406-PropiedadesAlpes/assets/60992168/d96e2d76-7657-456d-b775-07b22a2b7201)

## Video - Entrega 4
[](https://github.com/lmaero/MISW4406-PropiedadesAlpes/assets/98992754/f93900ed-a8e2-467d-901e-ad9ad97b1b0b)


## Ejecutar Aplicación

Para la ejecución de la aplicación, lo primero que se debe levantar es la infraestructura broker de Apache Pulsar, esta se encuentra configurada para que se monte utilizando contenedores de Docker, por ende, para correr dicho broker, se debe hacer con el siguiente comando de Docker Compose:

```bash
docker compose --profile pulsar up --build
```

Cabe destacar que dicho comando construira las imagenes de docker asociadas a Apache Pulsar (obtenidas desde el catálogos de imágenes de Docker), si es que estás existen.


Ahora es posible ejecutar los microservicios ui, pda/transactions y notifications. 

### UI
Desde el directorio principal ejecute el siguiente comando.

```bash
python src/ui/main.py
```

### Notifications
Desde el directorio principal ejecute el siguiente comando.

```bash
python src/ui/main.py
```
### PDA/Transactions
Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/pda/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/pda/api --debug run
```


## Request de ejemplo

Los siguientes JSON pueden ser usados para probar el API:

### Create Transaction (Async - using command)

- **Endpoint**: `/properties/transactions`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
    "leases": [
        {
            "payments": [
                {
                    "amount": 100.00,
                    "date": "2022-11-22T15:10:00Z"
                }
            ]
        }
    ]
}
```

### Get Transaction (Async - using query) [Work In Progress]

- **Endpoint**: `/properties/transactions/{id}`
- **Método**: `GET`
- **Headers**: `Content-Type='aplication/json'`
