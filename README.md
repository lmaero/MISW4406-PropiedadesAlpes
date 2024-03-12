# PDA

Repositorio con código base para el desarrollo de una arquitectura hexagonal siguiendo los principios y patrones de DDD.


## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma:

- **src**: En este directorio encuentra el código fuente para Propiedades de los Alpes.
- **src/pda**: En este directorio se encuentra el código fuente para la aplicación Flask.
- **src/notifications**: En este directorio se encuentra el código fuente para el módulo de notificaciones.
- **src/payments**: En este directorio se encuentra el código fuente para el módulo de pagos.
- **src/tenant**: En este directorio se encuentra el código fuente para el módulo de arrendatarios.
- **src/bff**: En este directorio se encuentra el código fuente para el módulo de Backend for Frontend.
- **src/ui**: En este directorio se encuentra el código fuente para la app web/interfaz gráfica.
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **.gitpod.yml**: Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Gitpod
- **README.md**: El archivo que está leyendo
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms pda (librerias Python)
- **notification-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms notifications (librerias Python)
- **ui-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms ui (librerias Python)
- **tenant-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms tenant (librerias Python)
- **payments-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms payments (librerias Python)
- **bff-requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del ms bff (librerias Python)

## Escenarios de calidad a probar
- Escenario #9: Modificabilidad
- Escenario #2: Escalabilidad
- Escenario #6: Disponibilidad

## Video - Entrega 3

[](https://github.com/lmaero/MISW4406-PropiedadesAlpes/assets/60992168/d96e2d76-7657-456d-b775-07b22a2b7201)

## Video - Entrega 4

[](https://github.com/lmaero/MISW4406-PropiedadesAlpes/assets/98992754/66e911d2-0032-4a33-b9c5-f75c30ff0d3d)



## Ejecutar Aplicación

Para la ejecución de la aplicación, lo primero que se debe levantar es la infraestructura broker de Apache Pulsar y la del motor MySQL, esta se encuentra configurada para que se monte utilizando contenedores de Docker, por ende, para correr dicho broker, se debe hacer con el siguiente comando de Docker Compose:

```bash
docker compose --profile pulsar up
```

y en otra terminal, levantar el perfil de base de datos en MySQL

```bash
docker compose --profile db up
```

Cabe destacar que dicho comando construira las imagenes de docker asociadas a Apache Pulsar y MySQL (obtenidas desde el catálogos de imágenes de Docker), si es que estás existen.


Ahora es posible ejecutar los microservicios ui, pda/transactions y notifications. 


### PDA/Transactions
Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/pda/api run --port 5001
```

### Tenant
Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn tenant.main:app --host localhost --port 8002 --reload
```

### Payments
Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn payments.main:app --host localhost --port 8001 --reload
```

### BFF
Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn bff.main:app --host localhost --port 8005 --reload 
```

### UI
Desde el directorio principal ejecute el siguiente comando.

```bash
python src/ui/main.py
```

### Notifications
Desde el directorio principal ejecute el siguiente comando.

```bash
python src/notifications/main.py
```

## Request de ejemplo

Los siguientes JSON pueden ser usados para probar el API:

### Create Transaction (by BFF)

- **Endpoint**: `/v1/properties/transactions`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
    "location": "Bucaramanga",
    "leases": [
        {
            "payments": [
                {
                    "amount": 100.00,
                    "date": "2022-11-22T15:10:00Z"
                }
            ]
        }
    ],
    "payment": {
        "amount": 100.00,
        "amount_vat": 119.00
    },
    "tenant": {
        "name": "Diego",
        "last_name": "Eslava"
    }

}
```

### Postman
Cabe destacar, que dentro del directorio del proyecto, viene la colección de postman asociada a la prueba realizada durante el experimento hecho en el video. El archivo se llama:
```
No Monoliticas - Entrega 9.postman_collection
```