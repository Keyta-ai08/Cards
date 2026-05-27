def get_card_suit_and_value(card_name: str):
    parts = card_name.split(" ")
    suit = parts[0]
    val_str = parts[1] if len(parts) > 1 else ""
    return suit, val_str

def is_trump(card_name: str, trump_suit: str) -> bool:
    if not card_name:
        return False
    suit, val = get_card_suit_and_value(card_name)
    # Buben sind immer Trumpf!
    if val == "Bube":
        return True
    return suit == trump_suit

def get_card_power(card_name: str, lead_suit: str, trump_suit: str) -> int:
    """
    Returns an integer power value for a card. Higher is better.
    Hierarchy (lowest to highest):
    1. Normal cards (not lead suit, not trump) -> 0 to 9
    2. Lead suit cards -> 10 to 19
    3. Trump suit cards -> 20 to 29
    4. Buben -> 30 to 33 (Karo < Pik < Herz < Kreuz)
    """
    suit, val = get_card_suit_and_value(card_name)
    
    # Val hierarchy
    val_hier = {"7": 1, "8": 2, "9": 3, "10": 4, "Dame": 5, "König": 6, "Ass": 7}
    
    # Buben
    if val == "Bube":
        bube_hier = {"Karo": 30, "Pik": 31, "Herz": 32, "Kreuz": 33}
        return bube_hier.get(suit, 30)
        
    # Trump suit
    if suit == trump_suit:
        return 20 + val_hier.get(val, 0)
        
    # Lead suit
    if suit == lead_suit:
        return 10 + val_hier.get(val, 0)
        
    # Other suits (can't win the trick)
    return val_hier.get(val, 0)

def compare_cards(card1_name: str, card2_name: str, lead_suit: str, trump_suit: str) -> int:
    """
    Returns 1 if card1 > card2, -1 if card1 < card2, 0 if equal.
    """
    p1 = get_card_power(card1_name, lead_suit, trump_suit)
    p2 = get_card_power(card2_name, lead_suit, trump_suit)
    if p1 > p2:
        return 1
    elif p1 < p2:
        return -1
    return 0
