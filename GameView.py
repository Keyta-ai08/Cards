import flet as ft
import asyncio
from classes.Game20UP import Game20UP

def game_view(page: ft.Page, current_user_icon, game_instance: Game20UP):
    # Controls
    turn_text = ft.Text(
        value="Aktueller Zug:",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.AMBER_400
    )
    
    trump_text = ft.Text(
        value="Trumpf: Noch nicht gewählt",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_200
    )
    
    scoreboard_container = ft.Column(
        spacing=5
    )

    table_container = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )
    
    hand_container = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )
    
    status_text = ft.Text(
        value="",
        size=18,
        color=ft.Colors.GREEN_300
    )

    # Make sure we start the first round when we load the view
    if game_instance.state == game_instance.DEALING_3 and not game_instance.players[0].hand:
        game_instance.start_round()

    def get_card_sprite_pos(card_name: str):
        suit_map = {"Karo": 0, "Pik": 1, "Herz": 2, "Kreuz": 3}
        val_map = {
            "Ass": 0, "2": 1, "3": 2, "4": 3, "5": 4, 
            "6": 5, "7": 6, "8": 7, "9": 8, "10": 9, 
            "Bube": 10, "Dame": 11, "König": 12
        }
        parts = card_name.split(" ")
        suit = parts[0]
        val_str = parts[1] if len(parts) > 1 else ""
        return suit_map.get(suit, 0), val_map.get(val_str, 0)

    def build_card_widget(card, on_click_handler=None, disabled=False):
        row, col = get_card_sprite_pos(card["name"])
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
        
        card_img = ft.Container(
            content=image_stack,
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
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_click=on_click_handler if not disabled else None,
            ink=not disabled,
            opacity=0.5 if disabled else 1.0
        )

    def on_card_click(e, card):
        current_player = game_instance.get_current_player()
        if not current_player: return
        
        if game_instance.state == game_instance.PLAYING_TRICK:
            if not game_instance.can_play_card(current_player, card):
                page.snack_bar = ft.SnackBar(ft.Text("Farbzwang! Du musst die angespielte Farbe bedienen."))
                page.snack_bar.open = True
                page.update()
                return
            
            success = game_instance.play_card(current_player, card)
            if success:
                update_ui()
                if game_instance.state == game_instance.ROUND_EVALUATION:
                    # Delay for 2 seconds then evaluate
                    page.run_task(delayed_evaluation)

    async def delayed_evaluation():
        await asyncio.sleep(2)
        game_instance.evaluate_trick()
        update_ui()

    def show_trump_dialog(current_player):
        def on_trump_selected(e, suit):
            dlg.open = False
            game_instance.set_trump(suit)
            update_ui()
            page.update()
            
        def build_trump_button(card):
            suit = card["name"].split(" ")[0]
            # Map suits to icons/colors
            color = ft.Colors.RED if suit in ["Herz", "Karo"] else ft.Colors.BLACK
            icon = ft.Icons.FAVORITE if suit == "Herz" else (ft.Icons.SPORTS_ESPORTS if suit == "Kreuz" else ft.Icons.WINDOW)
            if suit == "Karo": icon = ft.Icons.DIAMOND
            
            return ft.ElevatedButton(
                content=ft.Text(suit),
                icon=icon,
                color=color,
                on_click=lambda e, s=suit: on_trump_selected(e, s)
            )

        buttons = []
        # Unique suits from hand
        suits_seen = set()
        for c in current_player.hand:
            s = c["name"].split(" ")[0]
            if s not in suits_seen:
                buttons.append(build_trump_button(c))
                suits_seen.add(s)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{current_player.name}, wähle den Trumpf!"),
            content=ft.Column(controls=buttons, tight=True),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def update_ui():
        current_player = game_instance.get_current_player()
        
        # Turn Info
        if current_player:
            turn_text.value = f"Aktueller Zug: {current_player.name}"
        else:
            turn_text.value = "Spiel beendet"
            
        # Trump Info
        if game_instance.trump_suit:
            mult = "(x2 Punkte)" if game_instance.trump_suit == "Kreuz" else ""
            trump_text.value = f"Trumpf: {game_instance.trump_suit} {mult}"
        else:
            trump_text.value = "Trumpf: Noch nicht gewählt"

        # Scoreboard
        scoreboard_container.controls.clear()
        scoreboard_container.controls.append(ft.Text("Punkte:", weight=ft.FontWeight.BOLD, size=18))
        for p in game_instance.get_all_players():
            color = ft.Colors.AMBER if p == current_player else ft.Colors.WHITE
            weight = ft.FontWeight.BOLD if p == current_player else ft.FontWeight.NORMAL
            stiche = f" (Stiche: {p.tricks_won})" if game_instance.trump_suit else ""
            scoreboard_container.controls.append(ft.Text(f"{p.name}: {p.score}{stiche}", color=color, weight=weight))

        # Table Cards
        table_container.controls.clear()
        if game_instance.current_trick:
            for p, c in game_instance.current_trick:
                table_container.controls.append(
                    ft.Column([
                        ft.Text(p.name, size=12, color=ft.Colors.GREY_400),
                        build_card_widget(c, disabled=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
        else:
            table_container.controls.append(
                ft.Container(
                    content=ft.Text("Tisch ist leer", color=ft.Colors.GREY_600),
                    width=250, height=150, alignment=ft.alignment.Alignment(0,0)
                )
            )
            
        # Hand Cards
        hand_container.controls.clear()
        is_my_turn = (game_instance.state == game_instance.PLAYING_TRICK)
        for card in game_instance.current_hand:
            disabled = not is_my_turn
            hand_container.controls.append(
                build_card_widget(card, on_click_handler=lambda e, c=card: on_card_click(e, c), disabled=disabled)
            )
        
        status_text.value = game_instance.get_status()
        if game_instance.state == game_instance.GAME_OVER:
            status_text.color = ft.Colors.GREEN_ACCENT_400
        else:
            status_text.color = ft.Colors.LIGHT_BLUE_200

        page.update()

        # Handle Trump Selection Popup
        if game_instance.state == game_instance.WAITING_FOR_TRUMP and current_player:
            show_trump_dialog(current_player)

    def on_reset_click(e):
        game_instance.reset_game()
        update_ui()

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
                    content=ft.Row(
                        controls=[
                            # Scoreboard an der Seite
                            ft.Container(
                                content=scoreboard_container,
                                width=150,
                                alignment=ft.alignment.Alignment(-1, -1),
                                border=ft.border.Border(right=ft.BorderSide(1, ft.Colors.GREY_800)),
                                padding=10
                            ),
                            # Haupt-Spielbereich
                            ft.Container( # !!!!Dies muss ein Container bleiben!!!!!
                                content=ft.Column(
                                    controls=[
                                        trump_text,
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    status_text,
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            margin=ft.margin.Margin(bottom=20)
                                        ),
                                        ft.Container(
                                            content=table_container,
                                            alignment=ft.alignment.Alignment(0, 0),
                                            height=200,
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    turn_text,
                                                    hand_container
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                                            border_radius=10,
                                            padding=10,
                                            alignment=ft.alignment.Alignment(0, 0),
                                            height=250,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.ElevatedButton(
                                                    content="Spiel Neu Starten",
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
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
