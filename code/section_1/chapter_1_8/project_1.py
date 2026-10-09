import json
import random
from collections import Counter
from pathlib import Path
from typing import Optional


class LootTable:
    """A weighted loot table system for RPG-style item drops."""
    
    # Rarity weights (higher = more common)
    RARITY_WEIGHTS = {
        "common": 100,
        "uncommon": 50,
        "rare": 20,
        "epic": 5,
        "legendary": 1
    }
    
    RARITY_COLORS = {
        "common": "⬜",
        "uncommon": "🟩",
        "rare": "🟦",
        "epic": "🟪",
        "legendary": "🟨"
    }
    
    def __init__(self, name: str = "Default Loot Table"):
        self.name = name
        self.items: list[dict] = []
        self.drop_history: list[dict] = []
    
    def add_item(self, name: str, rarity: str, value: int = 0) -> None:
        """Add an item to the loot table."""
        if rarity not in self.RARITY_WEIGHTS:
            raise ValueError(f"Invalid rarity: {rarity}. Use one of {list(self.RARITY_WEIGHTS.keys())}")
        
        self.items.append({
            "name": name,
            "rarity": rarity,
            "value": value,
            "weight": self.RARITY_WEIGHTS[rarity]
        })
    
    def roll(self, count: int = 1) -> list[dict]:
        """Roll for loot drops."""
        if not self.items:
            return []
        
        weights = [item["weight"] for item in self.items]
        drops = random.choices(self.items, weights=weights, k=count)
        
        # Record in history
        for drop in drops:
            self.drop_history.append(drop.copy())
        
        return drops
    
    def roll_with_display(self, count: int = 1) -> list[dict]:
        """Roll for loot and display results."""
        drops = self.roll(count)
        
        print(f"\n[I] Rolling {count} time(s) from '{self.name}'...")
        print("-" * 40)
        
        for drop in drops:
            color = self.RARITY_COLORS[drop["rarity"]]
            print(f"  {color} {drop['name']} ({drop['rarity'].upper()}) - {drop['value']} gold")
        
        total_value = sum(d["value"] for d in drops)
        print("-" * 40)
        print(f"Total value: {total_value} gold")
        
        return drops
    
    def get_statistics(self) -> dict:
        """Get statistics about drop history."""
        if not self.drop_history:
            return {"message": "No drops recorded yet"}
        
        rarity_counts = Counter(d["rarity"] for d in self.drop_history)
        item_counts = Counter(d["name"] for d in self.drop_history)
        total_value = sum(d["value"] for d in self.drop_history)
        
        return {
            "total_drops": len(self.drop_history),
            "total_value": total_value,
            "average_value": total_value / len(self.drop_history),
            "by_rarity": dict(rarity_counts),
            "most_common_items": item_counts.most_common(5),
            "rarity_rates": {
                rarity: count / len(self.drop_history) * 100
                for rarity, count in rarity_counts.items()
            }
        }
    
    def display_statistics(self) -> None:
        """Display formatted statistics."""
        stats = self.get_statistics()
        
        if "message" in stats:
            print(stats["message"])
            return
        
        print(f"\n[I] Statistics for '{self.name}'")
        print("=" * 40)
        print(f"Total Drops: {stats['total_drops']}")
        print(f"Total Value: {stats['total_value']} gold")
        print(f"Average Value: {stats['average_value']:.2f} gold")
        
        print("\n[I] Drop Rates by Rarity:")
        for rarity in ["legendary", "epic", "rare", "uncommon", "common"]:
            if rarity in stats["rarity_rates"]:
                rate = stats["rarity_rates"][rarity]
                bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
                print(f"  {self.RARITY_COLORS[rarity]} {rarity:12} {bar} {rate:.1f}%")
        
        print("\n[I] Most Common Drops:")
        for item, count in stats["most_common_items"]:
            print(f"  {item}: {count}")
    
    def save(self, filepath: str) -> bool:
        """Save loot table to JSON file."""
        data = {
            "name": self.name,
            "items": self.items,
            "history_count": len(self.drop_history)
        }
        
        try:
            Path(filepath).write_text(json.dumps(data, indent=2))
            print(f"[I] Saved loot table to {filepath}")
            return True
        except IOError as e:
            print(f"[!] Failed to save: {e}")
            return False
    
    @classmethod
    def load(cls, filepath: str) -> Optional["LootTable"]:
        """Load loot table from JSON file."""
        try:
            data = json.loads(Path(filepath).read_text())
            table = cls(data["name"])
            table.items = data["items"]
            print(f"[I] Loaded '{table.name}' with {len(table.items)} items")
            return table
        except FileNotFoundError:
            print(f"[!] File not found: {filepath}")
            return None
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[!] Invalid loot table file: {e}")
            return None


# Demo usage
if __name__ == "__main__":
    # Create a loot table
    dungeon_loot = LootTable("Dark Forest Dungeon")
    
    # Add items
    dungeon_loot.add_item("Gold Coin", "common", 10)
    dungeon_loot.add_item("Health Potion", "common", 25)
    dungeon_loot.add_item("Iron Dagger", "uncommon", 50)
    dungeon_loot.add_item("Enchanted Ring", "uncommon", 75)
    dungeon_loot.add_item("Mystic Orb", "rare", 200)
    dungeon_loot.add_item("Dragon Scale", "rare", 300)
    dungeon_loot.add_item("Void Crystal", "epic", 1000)
    dungeon_loot.add_item("Excalibur", "legendary", 5000)
    
    # Roll for loot
    dungeon_loot.roll_with_display(5)
    
    # Simulate many drops
    print("\n🎰 Simulating 1000 drops...")
    dungeon_loot.roll(1000)
    dungeon_loot.display_statistics()
    
    # Save the loot table
    dungeon_loot.save("dungeon_loot.json")
