
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

    def get_card_sprite_pos(card_name: str):
        suit_map = {
            "Karo": 0,
            "Pik": 1,
            "Herz": 2,
            "Kreuz": 3
        }
        val_map = {
            "Ass": 0, "2": 1, "3": 2, "4": 3, "5": 4, 
            "6": 5, "7": 6, "8": 7, "9": 8, "10": 9, 
            "Bube": 10, "Dame": 11, "König": 12
        }
        parts = card_name.split(" ")
        suit = parts[0]
        val_str = parts[1] if len(parts) > 1 else ""
        
        row = suit_map.get(suit, 0)
        col = val_map.get(val_str, 0)
        return row, col

    def build_card_widget(card):
        row, col = get_card_sprite_pos(card["name"])
        
        # Original Image Size: 5916 x 2536
        # Ratio of card: width=115, height=160
        card_width = 115
        card_height = 160
        full_width = card_width * 13
        full_height = card_height * 4
        
        image_stack = ft.Stack(
            controls=[
                ft.Image(
                    src="cards.jpeg",
                    width=full_width,
                    height=full_height,
                    fit=ft.BoxFit.FILL,
                    left=-col * card_width,
                    top=-row * card_height,
                )
            ]
        )
        
        return ft.Container(
            content=image_stack,
            width=card_width,
            height=card_height,
            border_radius=8,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
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