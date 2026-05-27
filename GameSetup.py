import flet as ft
import Login
import GameView
import GameSelection
from classes.Game20UP import Game20UP
from classes.Player import Player

def game_setup_view(page: ft.Page, user_icon, game_id):
    data = Login.load_data(page)
    game_mode= game_id
    existing_users = [u["username"] for u in data["users"]]
    
    slots = []
    for i in range(4):
        options = [ft.dropdown.Option("Gast (Eigener Name)"), ft.dropdown.Option("- Leer -")] + [ft.dropdown.Option(u) for u in existing_users]
        
        # Standardwerte: Die ersten 3 Spieler sind standardmäßig auf "Gast" eingestellt, der 4. auf "- Leer -"
        default_val = "Gast (Eigener Name)" if i < 3 else "- Leer -"
        
        dd = ft.Dropdown(
            label=f"Spieler {i+1}",
            options=options,
            value=default_val,
            width=200
        )
        tf = ft.TextField(label="Gast Name", value=f"Spieler {i+1}", visible=(dd.value == "Gast (Eigener Name)"), width=200)
        
        def on_change(e, idx=i):
            slots[idx]["tf"].visible = (slots[idx]["dd"].value == "Gast (Eigener Name)")
            page.update()
            
        dd.on_change = on_change
        slots.append({"dd": dd, "tf": tf})
        
    def start_game(e):
        players = []
        score = 0
        
        if game_mode == 1:
            score = 20
        
        for i, slot in enumerate(slots):
            dd = slot["dd"]
            tf = slot["tf"]
            
            name = ""
            is_guest = False
            if dd.value == "Gast (Eigener Name)":
                if tf.value.strip():
                    name = tf.value.strip()
                    is_guest = True
            elif dd.value != "- Leer -":
                name = dd.value
                
            if name:
                players.append(Player(name, score, is_guest=is_guest))
                
        if len(players) < 3:
            page.snack_bar = ft.SnackBar(ft.Text("Für 20-UP werden mindestens 3 Spieler benötigt!"))
            page.snack_bar.open = True
            page.update()
            return
            
        game_instance = Game20UP()
        for p in players:
            game_instance.add_player(p)
            
        page.navigate("/game_20up")
        page.views.append(GameView.game_view(page, user_icon, game_instance))
        page.update()
        
    def go_back(e):
        page.navigate("/game_selection")
        page.views.append(GameSelection.selection_view(page, user_icon))
        page.update()
        
    slot_controls = []
    for slot in slots:
        slot_controls.append(ft.Row([slot["dd"], slot["tf"]], alignment=ft.MainAxisAlignment.CENTER))
        
    return ft.View(
        route="/game_setup",
        appbar=ft.AppBar(
            title=ft.Text("Spiel-Setup (20-UP)"),
            bgcolor=ft.Colors.GREEN,
        ),
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text("Spieler konfigurieren (3-4 Spieler)", size=24, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            *slot_controls,
                            ft.Container(height=20),
                            ft.Row([
                                ft.ElevatedButton("Spiel Starten", on_click=start_game, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                                ft.ElevatedButton("Zurück", on_click=go_back, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )
