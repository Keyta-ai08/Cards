#Eigene Imports
import GameSelection
import Game20UP
import Login
import Settings

import flet as ft

def menu(page: ft.Page):
    
    choice = None
    
    user_icon = None
    try:
        user_icon = Login.get_current_user_icon(page)
        print(f"Icon des aktuellen Users: {user_icon}")
        
        if user_icon is None:
            print("Bitte einloggen!")
            page.navigate("/login")
            return Login.login(page)
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")
        user_icon = ft.Icons.HELP
    
    def on_click(page: ft.Page, option, user_icon):
        nonlocal choice
        choice = option
        if choice == 1:
            page.navigate("/game_selection")
            page.views.append(GameSelection.selection_view(page,user_icon))
            page.update()
        elif choice == 2:
            page.navigate("/settings")
            page.views.append(Settings.settings_view(page))
            page.update()
        elif choice == 3:
            from main import home
            page.navigate("/main")
            page.views.append(home(page))
            page.update()
       
    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("Spiele-Zentrale"),
            bgcolor=ft.Colors.GREEN,
            actions=[
                ft.Container(
                    content=ft.Icon(user_icon, size=24, color=ft.Colors.WHITE),
                    padding=10
                )
            ]
        ),
        route="/menu",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Hauptmenü", size=30, weight=ft.FontWeight.BOLD)
                                        ),
                                        ft.Container(
                                            content=ft.Button("Spieleauswahl", on_click=lambda e: on_click(page, 1, user_icon))
                                        ),
                                        ft.Container(
                                            content=ft.Button("Einstellungen", on_click=lambda e: on_click(page, 2, user_icon))
                                        ),
                                        ft.Container(
                                            content=ft.Button("Logout", on_click=lambda e: on_click(page, 3, user_icon))
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