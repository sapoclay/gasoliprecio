# Gasoliprecio

**Gasoliprecio** es una aplicación desarrollada en Python utilizando el framework [Flet](https://flet.dev/), que permite a los usuarios buscar estaciones de servicio en España, filtrando por ciudad y tipo de combustible. Además, proporciona información sobre los precios de los combustibles en tiempo real y permite abrir la ubicación de las estaciones en Google Maps.

## Características

- **Búsqueda de estaciones de servicio**: Filtra las estaciones de servicio en España por ciudad y tipo de combustible.
- **Precios actualizados**: Los precios de los combustibles se actualizan automáticamente cada media hora.
- **Interfaz gráfica**: Se ha creado utilizando Flet para crear una interfaz sencilla y fácil de usar.
- **Cambio de tema**: Permite cambiar entre un tema claro y oscuro.
- **Accesibilidad del código fuente**: Enlace directo al repositorio de GitHub para ver el código fuente y colaborar.

## Requisitos

Para ejecutar este proyecto, necesitas tener Python instalado en tu sistema. Además, necesitarás instalar las dependencias que se encuentran en el archivo `requirements.txt`.

### Dependencias

Las dependencias se encuentran en el archivo `requirements.txt` y se pueden instalar utilizando `pip`:

- requests: Para realizar las solicitudes HTTP y obtener los datos de la API de precios de combustibles.
- flet: Framework para crear interfaces gráficas interactivas en Python.

## Instalación

### Clonar el repositorio:

```
git clone https://github.com/sapoclay/gasoliprecio.git
cd gasolina
```

### Crear y activar el entorno virtual:

Ejecuta el siguiente script para crear un entorno virtual en tu máquina:

```
python run_app.py
``` 

Este script creará un entorno virtual llamado venv, instalará las dependencias desde requirements.txt y ejecutará la aplicación.

## Funcionalidades

- Introducir ciudad: Permite al usuario ingresar una ciudad y buscar las estaciones de servicio disponibles en esa área.
- Seleccionar tipo de combustible: Filtra las estaciones por tipo de combustible como Gasóleo A, Gasolina 95, GLP, etc.
- Ver estaciones en Google Maps: Al hacer clic en el icono de un mapa, se abrirá la ubicación de la estación de servicio en Google Maps.
- Mostrar información sobre la aplicación: A través del botón de opciones, el usuario puede acceder a la información sobre la aplicación y cambiar el tema de la interfaz.

## Licencia

Este proyecto está bajo la GPL-3.0 license. Para más detalles, consulta el archivo LICENSE.