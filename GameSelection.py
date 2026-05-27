import flet as ft
import GameView
from classes.Game20UP import Game20UP
import Menu

def selection_view(page: ft.Page, user_icon):
    
    def on_game_select(page: ft.Page, game_id: int):
        if game_id == 1:
            page.navigate("/game_20up")
            page.views.append(GameView.game_view(page, user_icon, Game20UP()))
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Dieses Spiel ist noch nicht verfügbar!"))
            page.snack_bar.open = True
            page.update()
            
    def on_back(page: ft.Page):
        page.navigate("/menu")
        page.views.append(Menu.menu(page))
        page.update()

    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("Spieleauswahl"),
            bgcolor=ft.Colors.GREEN,
            actions=[
                ft.Container(
                    content=ft.Icon(user_icon, size=24, color=ft.Colors.WHITE),
                    padding=10
                )
            ]
        ),
        route="/game_selection",
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text("Verfügbare Spiele", size=30, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Container(height=20),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Icon(ft.Icons.CASINO, size=50, color=ft.Colors.GREEN),
                                            ft.Text("20-UP", size=20, weight=ft.FontWeight.BOLD),
                                            ft.Text("Erreiche genau 20 Punkte!", text_align=ft.TextAlign.CENTER)
                                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        width=200,
                                        height=200,
                                        bgcolor=ft.Colors.GREEN_50,
                                        border_radius=10,
                                        border=ft.Border.all(2, ft.Colors.GREEN_400),
                                        on_click=lambda e: on_game_select(page, 1),
                                        ink=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Icon(ft.Icons.LOCK, size=50, color=ft.Colors.GREY),
                                            ft.Text("Coming Soon", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY),
                                            ft.Text("Weitere Spiele folgen in Kürze...", text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY)
                                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        width=200,
                                        height=200,
                                        bgcolor=ft.Colors.GREY_200,
                                        border_radius=10,
                                        border=ft.Border.all(2, ft.Colors.GREY_400),
                                        on_click=lambda e: on_game_select(page, 2),
                                        ink=True
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                wrap=True,
                                spacing=20
                            ),
                            ft.Container(height=40),
                            ft.ElevatedButton(
                                content="Zurück zum Hauptmenü",
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e: on_back(page),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED_700
                                )
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )
