import flet as ft
import requests
import webbrowser


def obtener_datos(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def filtrar_estaciones(estaciones, ciudad, tipo_combustible):
    ciudad = ciudad.lower()
    estaciones_filtradas = [
        estacion for estacion in estaciones
        if ciudad in estacion.get("Municipio", "").lower()
    ]
    if tipo_combustible:
        estaciones_filtradas = [
            estacion for estacion in estaciones_filtradas
            if estacion.get(tipo_combustible) not in (None, "N/A", "")
        ]
    return estaciones_filtradas


def main(page: ft.Page):
    page.title = "Gasoliprecio: Búsqueda de Estaciones de Servicio"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # URLs
    url_api = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    url_github = "https://github.com/sapoclay/gasoliprecio"

    # Controles principales
    ciudad_input = ft.TextField(label="Introduce la ciudad", expand=True)
    tipo_combustible_dropdown = ft.Dropdown(
        label="Seleccione el tipo de combustible",
        options=[
            ft.dropdown.Option("Precio Gasoleo A"),
            ft.dropdown.Option("Precio Gasolina 95 E5"),
            ft.dropdown.Option("Precio Gasoleo Premium"),
            ft.dropdown.Option("Precio Bioetanol"),
            ft.dropdown.Option("Precio GLP"),
        ],
        expand=True,
    )
    resultados_listview = ft.ListView(expand=True, spacing=10, padding=10)

    def mostrar_snackbar(mensaje):
        snackbar = ft.SnackBar(content=ft.Text(mensaje))
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def abrir_google_maps(nombre, direccion):
        if direccion and nombre:
            consulta = f"{nombre}, {direccion}".replace(" ", "+")
            url = f"https://www.google.com/maps/search/?api=1&query={consulta}"
            webbrowser.open(url)
        else:
            mostrar_snackbar("No se puede abrir Google Maps para esta estación.")

    def buscar_estaciones(e):
        ciudad = ciudad_input.value.strip()
        tipo_combustible = tipo_combustible_dropdown.value

        if not ciudad:
            mostrar_snackbar("Por favor, introduzca una ciudad.")
            return

        resultados_listview.controls.clear()
        resultados_listview.controls.append(
            ft.Container(ft.Text("Cargando...", size=20, color="blue"), alignment=ft.alignment.center, expand=True)
        )
        page.update()

        datos = obtener_datos(url_api)
        if not datos:
            mostrar_snackbar("Error al obtener datos de la API.")
            resultados_listview.controls.clear()
            page.update()
            return

        estaciones = datos.get("ListaEESSPrecio", [])
        estaciones_filtradas = filtrar_estaciones(estaciones, ciudad, tipo_combustible)

        if not estaciones_filtradas:
            mostrar_snackbar(f"No se encontraron estaciones en {ciudad}.")
            resultados_listview.controls.clear()
            page.update()
            return

        resultados_listview.controls.clear()
        for estacion in estaciones_filtradas:
            nombre = estacion.get("Rótulo", "N/A")
            direccion = estacion.get("Dirección", "N/A")
            precio = estacion.get(tipo_combustible, "N/A") if tipo_combustible else "No disponible"
            resultados_listview.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(f"Nombre: {nombre}", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Dirección: {direccion}"),
                                    ft.Text(f"Precio: {precio} €/L"),
                                ],
                                spacing=5,
                            ),
                            padding=10,
                            border=ft.border.all(1),
                            border_radius=5,
                            margin=5,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.MAP,
                            tooltip="Ver en Google Maps",
                            on_click=lambda e, n=nombre, d=direccion: abrir_google_maps(n, d),
                        ),
                    ],
                    spacing=10,
                )
            )
        mostrar_snackbar(f"Se encontraron {len(estaciones_filtradas)} estaciones en {ciudad}.")
        page.update()

    def abrir_github(e):
        webbrowser.open(url_github)

    def cambiar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    def mostrar_acerca_de(e):
        """Muestra una ventana con información sobre la aplicación."""
        # Crear una instancia del diálogo
        acerca_de_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Acerca de gasoliprecio"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="assets/img/logo.jpeg", width=150, height=150),
                        ft.Text(
                            "Esta aplicación permite buscar estaciones de servicio en España, "
                            "filtrando por ciudad y tipo de combustible. Desarrollado con Flet y Python."
                            "\nLa actualización de precios se realiza cada media hora, con los precios en vigor en ese momento.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Abrir repositorio en GitHub",
                            icon=ft.Icons.CODE,
                            on_click=abrir_github,
                        ),
                        ft.ElevatedButton(
                            "Cambiar tema",
                            icon=ft.Icons.LIGHT_MODE,
                            on_click=cambiar_tema,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.alignment.center,
                width=400,  # Ancho de la ventana
                height=400,  # Alto de la ventana
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda e: close_dialog(acerca_de_dialog),  # Cerrar el diálogo correctamente
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Agregar el diálogo al overlay de la página
        page.overlay.append(acerca_de_dialog)
        acerca_de_dialog.open = True
        page.update()

    def close_dialog(dialog):
        """Cierra el diálogo correctamente."""
        dialog.open = False  # Establecer open a False para cerrarlo
        page.update()  # Actualizar la página para reflejar el cambio



    opciones_button = ft.ElevatedButton(text="Opciones", icon=ft.Icons.MENU, on_click=mostrar_acerca_de)

    page.add(
        ft.Column(
            [
                opciones_button,
                ft.Row([ciudad_input, tipo_combustible_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ElevatedButton("Buscar", icon=ft.Icons.SEARCH, on_click=buscar_estaciones),
                resultados_listview,
            ],
            expand=True,
        )
    )


ft.app(target=main)
