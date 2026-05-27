
#Lokale Imports
from classes.DeckManager import DeckManager as DM

import flet as ft

def game20up_view(page: ft.Page, current_user_icon):
    deck_manager = DM(draw_amount=5)
    current_hand = []

    # Controls
    hand_container = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )
    
    score_text = ft.Text(
        value="Gesamtpunktzahl: 0",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )
    
    status_text = ft.Text(
        value="Ziehe eine Karte, um das Spiel zu starten!",
        size=16,
        color=ft.Colors.GREEN_300
    )

    def get_suit_style(card_name: str):
        if "Kreuz" in card_name:
            return "♣", ft.Colors.BLUE_GREY_100, ft.Colors.BLACK
        elif "Pik" in card_name:
            return "♠", ft.Colors.BLUE_GREY_100, ft.Colors.BLUE_900
        elif "Herz" in card_name:
            return "♥", ft.Colors.RED_50, ft.Colors.RED_ACCENT
        elif "Karo" in card_name:
            return "♦", ft.Colors.ORANGE_50, ft.Colors.ORANGE_900
        return "?", ft.Colors.WHITE, ft.Colors.BLACK

    def build_card_widget(card):
        suit_char, bg_color, text_color = get_suit_style(card["name"])
        parts = card["name"].split(" ")
        card_value_str = parts[1] if len(parts) > 1 else card["name"]
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(suit_char, size=32, color=text_color, weight=ft.FontWeight.BOLD),
                    ft.Text(card_value_str, size=16, color=text_color, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Wert: {card['value']}", size=12, color=ft.Colors.GREY_700),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=110,
            height=160,
            bgcolor=bg_color,
            border_radius=12,
            border=ft.border.all(2, text_color),
            alignment=ft.alignment.Alignment(0, 0),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(2, 2)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

    def update_ui():
        hand_container.controls.clear()
        total_score = sum(c["value"] for c in current_hand)
        
        for card in current_hand:
            hand_container.controls.append(build_card_widget(card))
            
        score_text.value = f"Gesamtpunktzahl: {total_score}"
        
        if total_score == 0:
            status_text.value = "Ziehe eine Karte, um das Spiel zu starten!"
            status_text.color = ft.Colors.GREY_400
        elif total_score >= 20:
            status_text.value = "Glückwunsch! Du hast das Ziel von 20 Punkten erreicht oder überschritten!"
            status_text.color = ft.Colors.GREEN_ACCENT_400
        else:
            status_text.value = f"Noch {20 - total_score} Punkte bis zum Ziel!"
            status_text.color = ft.Colors.LIGHT_BLUE_200

    def on_draw_click(e):
        card = deck_manager.draw_card()
        if card:
            current_hand.append(card)
            update_ui()
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Keine Karten mehr im Stapel!"))
            page.snack_bar.open = True
            page.update()

    def on_reset_click(e):
        current_hand.clear()
        deck_manager.reset_deck()
        update_ui()
        page.update()

    # Init UI controls initially
    update_ui()

    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text("20-UP - Spielbereich"),
            bgcolor=ft.Colors.GREEN,
            actions=[
                ft.Container(
                    content=ft.Icon(current_user_icon, size=24, color=ft.Colors.WHITE),
                    padding=10
                )
            ]
        ),
        route="/game_20up",
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        score_text,
                                        status_text,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                margin=ft.margin.Margin(bottom=20)
                            ),
                            ft.Container(
                                content=hand_container,
                                alignment=ft.alignment.Alignment(0, 0),
                                height=200,
                            ),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        content="Karte ziehen",
                                        icon=ft.Icons.ADD,
                                        on_click=on_draw_click,
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.WHITE,
                                            bgcolor=ft.Colors.GREEN_700,
                                        )
                                    ),
                                    ft.ElevatedButton(
                                        content="Zurücksetzen",
                                        icon=ft.Icons.REFRESH,
                                        on_click=on_reset_click,
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.WHITE,
                                            bgcolor=ft.Colors.RED_700,
                                        )
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                                margin=ft.margin.Margin(top=30)
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            )
        ]
    )