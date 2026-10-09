# Quest 1.4: Turn Messy Code into Clean Utilities
# Practice with functions, parameters, and return values

import random

# ===== UTILITY FUNCTIONS =====

def format_game_title(title: str) -> str:
    """
    Format a game title as a fancy header.
    
    Args:
        title: The game title to format.
    
    Returns:
        A formatted string with the title in uppercase.
    """
    return f"═══ {title.upper()} ═══"


def is_too_expensive(price: float, budget: float = 50.0) -> bool:
    """
    Check if a game exceeds the budget.
    
    Args:
        price: The game's price.
        budget: Maximum spending limit (default: $50).
    
    Returns:
        True if price exceeds budget, False otherwise.
    """
    return price > budget


def calculate_discount(price: float, percent: float) -> float:
    """
    Calculate the discounted price.
    
    Args:
        price: Original price.
        percent: Discount percentage (e.g., 20 for 20% off).
    
    Returns:
        The new price after discount.
    """
    discount_amount = price * (percent / 100)
    return price - discount_amount


def roll_dice(sides: int = 6, count: int = 1) -> list[int]:
    """
    Roll one or more dice.
    
    Args:
        sides: Number of sides on each die (default: 6).
        count: Number of dice to roll (default: 1).
    
    Returns:
        A list of roll results.
    """
    return [random.randint(1, sides) for _ in range(count)]


def calculate_damage(base: int, multiplier: float = 1.0, is_critical: bool = False) -> int:
    """
    Calculate damage with optional critical hit.
    
    Args:
        base: Base damage value.
        multiplier: Damage multiplier (default: 1.0).
        is_critical: Whether this is a critical hit (default: False).
    
    Returns:
        Final damage as an integer.
    """
    damage = base * multiplier
    if is_critical:
        damage *= 2.0
        print("   [!!] CRITICAL HIT!")
    return int(damage)


def format_stats(**stats) -> str:
    """
    Format any stats into a display string.
    
    Args:
        **stats: Any keyword arguments to display.
    
    Returns:
        A formatted multi-line string.
    """
    lines = ["[I] Character Stats:"]
    for stat_name, value in stats.items():
        # Convert snake_case to Title Case
        display_name = stat_name.replace("_", " ").title()
        lines.append(f"   {display_name}: {value}")
    return "\n".join(lines)


def find_item(inventory: list[dict], item_name: str) -> dict | None:
    """
    Find an item in inventory by name.
    
    Args:
        inventory: List of item dictionaries.
        item_name: Name to search for (case-insensitive).
    
    Returns:
        The item dictionary if found, None otherwise.
    """
    for item in inventory:
        if item.get("name", "").lower() == item_name.lower():
            return item
    return None


# ===== DEMONSTRATION =====

if __name__ == "__main__":
    print("=" * 50)
    print("         [I] UTILITY FUNCTIONS DEMO")
    print("=" * 50)
    print()
    
    # Test format_game_title
    print(format_game_title("hollow knight"))
    print(format_game_title("elden ring"))
    print()
    
    # Test is_too_expensive with different budgets
    games = [
        ("Indie Gem", 14.99),
        ("AAA Title", 59.99),
        ("Free to Play", 0.00),
        ("Deluxe Edition", 89.99)
    ]
    
    print("[I] Budget Check ($50 limit):")
    for name, price in games:
        status = "[!] Too Expensive" if is_too_expensive(price) else "[I] Affordable"
        print(f"   {name}: ${price:.2f} → {status}")
    print()
    
    # Test calculate_discount
    print("[I] Sale Prices (25% off):")
    for name, price in games:
        if price > 0:
            sale_price = calculate_discount(price, 25)
            print(f"   {name}: ${price:.2f} → ${sale_price:.2f}")
    print()
    
    # Test roll_dice
    print("[I] Dice Rolls:")
    print(f"   1d6: {roll_dice()}")
    rolls = roll_dice(6, 3)
    print(f"   3d6: {rolls} = {sum(rolls)}")
    print(f"   1d20: {roll_dice(20)}")
    print()
    
    # Test calculate_damage
    print("[I] Combat Calculations:")
    print(f"   Base Attack (10): {calculate_damage(10)}")
    print(f"   Power Attack (10 x 1.5): {calculate_damage(10, 1.5)}")
    print(f"   Critical Strike (10): {calculate_damage(10, 1.0, True)}")
    print()
    
    # Test format_stats
    print(format_stats(
        health=100,
        mana=50,
        strength=15,
        max_damage=25
    ))
    print()
    
    # Test find_item
    inventory = [
        {"name": "Sword", "damage": 10, "value": 100},
        {"name": "Shield", "defense": 5, "value": 75},
        {"name": "Potion", "healing": 25, "value": 15}
    ]
    
    print("[I] Inventory Search:")
    search_items = ["Sword", "Armor", "potion"]  # Note: "potion" is lowercase
    for item_name in search_items:
        found = find_item(inventory, item_name)
        if found:
            print(f"   Found '{found['name']}': {found}")
        else:
            print(f"   '{item_name}' not found in inventory")
    print()
    
    print("=" * 50)
    print("[I] Quest 1.4 Complete! +50 XP")
    print("=" * 50)
