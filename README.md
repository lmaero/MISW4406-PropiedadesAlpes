# PDA

Repositorio con código base para el desarrollo de una arquitectura hexagonal siguiendo los principios y patrones de DDD.


## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma:

- **src**: En este directorio encuentra el código fuente para Propiedades de los Alpes.
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **.gitpod.yml**: Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Gitpod
- **README.md**: El archivo que está leyendo
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del proyecto (librerias Python)

## Escenarios de calidad a probar
- Escenario #9: Modificabilidad
- Escenario #2: Escalabilidad
- Escenario #6: Disponibilidad

## Video

[](https://github.com/lmaero/MISW4406-PropiedadesAlpes/assets/60992168/d96e2d76-7657-456d-b775-07b22a2b7201)


## Ejecutar Aplicación

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

### Create Transaction

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

### Get Transaction

- **Endpoint**: `/properties/transactions/{id}`
- **Método**: `GET`
- **Headers**: `Content-Type='aplication/json'`
