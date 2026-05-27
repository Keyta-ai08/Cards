import pathlib
import json


#Lokale Imports
import Login
import Menu
import local_storage

import flet as ft

def load_settings(page: ft.Page) -> dict:
    data = local_storage.get("settings")
    if isinstance(data, dict):
        return data
    default_settings = {"width": 485, "height": 1080, "theme": "dark"}
    save_settings(page, default_settings)
    return default_settings

def save_settings(page: ft.Page, settings_dict: dict):
    local_storage.set("settings", settings_dict)

def is_first_run():
    # Wir prüfen auf die versteckte Datei im Home-Verzeichnis des Nutzers
    flag_file = pathlib.Path.home() / ".meine_app_wurde_gestartet"
    return not flag_file.exists()


def home(page: ft.Page):
    
    settings = load_settings(page)
    
    page.window.width = int(settings["width"]) if isinstance(settings["width"], str) else settings["width"]
    page.window.height = int(settings["height"]) if isinstance(settings["height"], str) else settings["height"]
    page.theme_mode = ft.ThemeMode.DARK if settings["theme"] == "dark" else ft.ThemeMode.LIGHT
    page.update()
        
    def on_key_press(e: ft.KeyboardEvent):
        if e.key == "Enter":
            # Shortcut für Entwicklung: Automatisch als erster User anmelden
            data = Login.load_data(page)
            if data["users"]:
                first_user = data["users"][0]
                data["current_user"] = first_user["username"]
                Login.save_data(page, data)
            
            page.navigate("/menu")
            page.views.append(Menu.menu(page))
            page.update()
    
    page.on_keyboard_event = on_key_press
    
    # Icon des aktuellen Users laden
    user_icon = None
    try:
        user_icon = Login.get_current_user_icon(page)
        if user_icon is None:
            user_icon = ft.Icons.HELP
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")
        user_icon = ft.Icons.HELP

    return ft.View(
        route="/",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Willkommen zu 20-UP!", size=30, weight=ft.FontWeight.BOLD)
                                        )  
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Button("Los geht's!", on_click=lambda e: on_button_click(page))
                                        )
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            )
        ]
    )
    
def on_button_click(page: ft.Page):
    if is_first_run():
        print("Erster Start erkannt!")
        page.navigate("/register")
        page.views.append(Login.register(page))
    else:
        page.navigate("/login")
        page.views.append(Login.login(page))
    page.update()

def main(page: ft.Page):
    page.title = "20-UP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    if not is_first_run():
        page.navigate("/")
        page.views.append(home(page))
    else:
        page.navigate("/register")
        page.views.append(Login.register(page))
        page.update()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)