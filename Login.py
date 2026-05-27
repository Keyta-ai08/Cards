from pathlib import Path
import json
import os
import hashlib

#Eigene Imports
import Menu
import flet as ft
import local_storage

DATA_FILE = Path("storage/data.json") # Deprecated, not used anymore

current_user = None

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + pwd_hash.hex()

def verify_password(password: str, hashed: str) -> bool:
    if ':' not in hashed:
        return password == hashed
    try:
        salt_hex, hash_hex = hashed.split(':', 1)
        salt = bytes.fromhex(salt_hex)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return pwd_hash.hex() == hash_hex
    except ValueError:
        return False

# Icons Mapping für sichere Konvertierung
icon_map=[
    {"name":"PERSON", "path": ft.Icons.PERSON},
    {"name":"WOMAN", "path": ft.Icons.WOMAN},
    {"name":"STAR", "path": ft.Icons.STAR},
    {"name":"HEART", "path": ft.Icons.FAVORITE},
    {"name":"ROCKET", "path": ft.Icons.ROCKET},
    {"name":"SHIELD", "path": ft.Icons.SHIELD}
]

def load_data(page: ft.Page) -> dict:
    data = local_storage.get("data")
    if not isinstance(data, dict):
        return {"users": [], "current_user": None}
    return {"users": [], "current_user": None, **data}

def save_data(page: ft.Page, data: dict) -> None:
    local_storage.set("data", data)

def get_options() -> list[ft.DropdownOption]:
    return [
        ft.DropdownOption(key=icon["name"], leading_icon=icon["path"])
        for icon in icon_map
    ]

def get_current_user_icon(page: ft.Page):
    """Lädt das Icon des aktuellen Users aus der JSON."""
    data = load_data(page)
    current_user = data.get("current_user")
    
    if current_user is None:
        return None
    
    print(f"Aktueller User: {current_user}")
    for user in data["users"]:
        if user["username"] == current_user:
            icon_key = user.get("icon")
            print(f"Icon des aktuellen Users: {icon_key}")
            if not icon_key:
                return None
            if user["username"] == "Phil":
                #print(f"Gefundenes Icon: {icon['name']} -> {icon['path']}")
                return ft.Icons.WINDOW
            for icon in icon_map:
                if icon["name"] == icon_key:
                    icon_path = icon["path"]
                    print(f"Gefundenes Icon: {icon['name']} -> {icon_path}")
                    return icon["path"]
    return None
    
def login(page: ft.Page):
    username_field = ft.TextField(label="Benutzername")
    password_field = ft.TextField(label="Passwort", password=True)
    
    def login_check(page: ft.Page, username: str, password: str) -> bool:
        if not username or not password:
            page.snack_bar = ft.SnackBar(ft.Text("Bitte Benutzernamen und Passwort eingeben!"))
            page.snack_bar.open = True
            page.update()
            return False
            
        data = load_data(page)
        for user in data["users"]:
            if user["username"] == username and verify_password(password, user["password"]):
                data["current_user"] = username
                save_data(page, data)
                page.navigate("/menu")
                page.views.append(Menu.menu(page))
                page.update()
                return True
        fwd_to_register(page)
        return False

    def fwd_to_register(page: ft.Page):
        page.navigate("/register")
        page.views.append(register(page))
        page.update()
    
    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("20-UP"),
            bgcolor=ft.Colors.GREEN,
        ),
        route="/login",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Login", size=30, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            content=ft.Text("Benutzername", size=15, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            username_field
                                        ),
                                        ft.Container(
                                            content=ft.Text("Passwort", size=15, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            password_field
                                        ),
                                        ft.Container(
                                            content=ft.Button("Einloggen", on_click=lambda e: login_check(page, username_field.value, password_field.value))
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
                                            content=ft.Text("Noch kein Konto? Registriere dich jetzt!", size=16)
                                        ),
                                        ft.Container(
                                            ft.Button("Registrieren", on_click=lambda e: fwd_to_register(page))
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
    
def register(page: ft.Page):
    username_field = ft.TextField(label="Benutzername")
    password_field = ft.TextField(label="Passwort", password=True)
    
    icon_choice = ft.Dropdown(
        expand=True,
        value="PERSON",
        label="Icon auswählen",
        options=get_options()
    )
    
    def register_user(page: ft.Page, username: str, password: str, icon: str): 
        if not username or not password:
            page.snack_bar = ft.SnackBar(ft.Text("Bitte alle Felder ausfüllen!"))
            page.snack_bar.open = True
            page.update()
            return False
            
        data = load_data(page)
        for user in data["users"]:
            if user["username"] == username:
                page.snack_bar = ft.SnackBar(ft.Text("Benutzername existiert bereits!"))
                page.snack_bar.open = True
                page.update()
                return False
                
        # Erstelle die Flag-Datei, um anzuzeigen, dass der erste Start abgeschlossen ist
        flag_file = Path.home() / ".meine_app_wurde_gestartet"
        if not flag_file.exists():
            flag_file.touch()
            
        hashed_password = hash_password(password)
        if username != "Phil":
            data["users"].append({"username": username, "password": hashed_password, "icon": icon})
        else:
            data["users"].append({"username": username, "password": hashed_password, "icon": "WINDOW"})
        data["current_user"] = username
        save_data(page, data)
        page.navigate("/menu")
        page.views.append(Menu.menu(page))
        page.update()
        return True
    
    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("20-UP"),
            bgcolor=ft.Colors.GREEN,
        ),
        route="/register",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Registrieren", size=30, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            content=ft.Text("Benutzernamen", size=15, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            username_field
                                        ),
                                        ft.Container(
                                            content=ft.Text("Passwort", size=15, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            password_field
                                        ),
                                        ft.Container(
                                            content=ft.Row([icon_choice], alignment=ft.MainAxisAlignment.CENTER)
                                        ),
                                        ft.Container(
                                            content=ft.Button("Registrieren", on_click=lambda e: register_user(page, username_field.value, password_field.value, icon_choice.value))
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