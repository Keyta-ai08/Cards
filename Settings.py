import flet as ft
import Login

def settings_view(page: ft.Page):
    import main
    # Lade die aktuellen Einstellungen
    current_settings = main.load_settings(page)
    
    # User Icon laden
    user_icon = None
    try:
        user_icon = Login.get_current_user_icon(page)
        if user_icon is None:
            user_icon = ft.Icons.HELP
    except Exception:
        user_icon = ft.Icons.HELP

    # UI-Elemente initialisieren
    theme_switch = ft.Switch(
        label="Dunkler Modus (Dark Mode)",
        value=current_settings.get("theme") == "dark"
    )

    # Resolution mapping
    resolutions = [
        {"label": "Mobil / Hochformat (485 x 1080)", "width": 485, "height": 1080},
        {"label": "Standard-Desktop (800 x 600)", "width": 800, "height": 600},
        {"label": "HD Ready (1280 x 720)", "width": 1280, "height": 720},
        {"label": "Full HD (1920 x 1080)", "width": 1920, "height": 1080}
    ]

    # Aktuelle Auflösung im Dropdown selektieren
    selected_key = None
    curr_w = int(current_settings.get("width", 485))
    curr_h = int(current_settings.get("height", 1080))
    for res in resolutions:
        if res["width"] == curr_w and res["height"] == curr_h:
            selected_key = f"{res['width']}x{res['height']}"
            break
    if not selected_key:
        selected_key = f"{curr_w}x{curr_h}"

    res_options = [
        ft.dropdown.Option(
            key=f"{res['width']}x{res['height']}",
            text=res["label"]
        ) for res in resolutions
    ]
    # Falls das geladene Format nicht in den Standard-Optionen ist, füge es hinzu
    if not any(opt.key == selected_key for opt in res_options):
        res_options.append(ft.dropdown.Option(key=selected_key, text=f"Custom ({curr_w} x {curr_h})"))

    resolution_dropdown = ft.Dropdown(
        label="Fenstergröße auswählen",
        expand=True,
        options=res_options,
        value=selected_key
    )

    def save_settings_event(e):
        # Neue Werte auslesen
        theme_val = "dark" if theme_switch.value else "light"
        
        w_val, h_val = 485, 1080
        if resolution_dropdown.value:
            parts = resolution_dropdown.value.split("x")
            if len(parts) == 2:
                w_val = int(parts[0])
                h_val = int(parts[1])

        # Settings Dictionary bauen
        new_settings = {
            "width": w_val,
            "height": h_val,
            "theme": theme_val
        }

        # Speichern in settings.json
        main.save_settings(page, new_settings)

        # Direkt anwenden
        page.theme_mode = ft.ThemeMode.DARK if theme_val == "dark" else ft.ThemeMode.LIGHT
        page.window.width = w_val
        page.window.height = h_val
        page.update()

        # Rückmeldung
        page.snack_bar = ft.SnackBar(ft.Text("Einstellungen erfolgreich gespeichert!"))
        page.snack_bar.open = True
        page.update()

    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("Einstellungen"),
            bgcolor=ft.Colors.GREEN,
            actions=[
                ft.Container(
                    content=ft.Icon(user_icon, size=24, color=ft.Colors.WHITE),
                    padding=10
                )
            ]
        ),
        route="/settings",
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=30,
                    content=ft.Column(
                        controls=[
                            ft.Text("App-Einstellungen", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Divider(),
                            ft.Container(height=10),
                            theme_switch,
                            ft.Container(height=10),
                            ft.Row([resolution_dropdown], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Container(height=30),
                            ft.ElevatedButton(
                                content="Einstellungen speichern",
                                icon=ft.Icons.SAVE,
                                on_click=save_settings_event,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREEN_700
                                )
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )