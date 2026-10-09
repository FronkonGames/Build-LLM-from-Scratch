from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class ShopItem:
    """Represents an item in the shop.
    
    The @dataclass decorator auto-generates __init__, __repr__, and __eq__
    based on the fields below. No boilerplate needed.
    """
    name: str
    price: float
    item_type: str
    
    def with_discount(self, discount: float) -> "ShopItem":
        """Return a new item with discounted price."""
        return ShopItem(
            name=self.name,
            price=self.price * (1 - discount),
            item_type=self.item_type
        )
    
    def __str__(self) -> str:
        return f"{self.name} ({self.item_type}) - ${self.price:.2f}"


class Shop:
    """A shop inventory management system."""
    
    DEFAULT_TAX_RATE = 0.15
    
    def __init__(self, name: str = "Shop", tax_rate: float = DEFAULT_TAX_RATE):
        self.name = name
        self.tax_rate = tax_rate
        self._items: list[ShopItem] = []
    
    @property
    def items(self) -> list[ShopItem]:
        """Get all items (read-only copy)."""
        return self._items.copy()
    
    def add_item(self, name: str, price: float, item_type: str) -> ShopItem:
        """Add an item to the shop."""
        item = ShopItem(name, price, item_type)
        self._items.append(item)
        return item
    
    def add_items(self, items_data: list[dict]) -> list[ShopItem]:
        """Add multiple items from dictionaries."""
        return [
            self.add_item(item["name"], item["price"], item["type"])
            for item in items_data
        ]
    
    def remove_item(self, name: str) -> bool:
        """Remove an item by name."""
        for i, item in enumerate(self._items):
            if item.name == name:
                self._items.pop(i)
                return True
        return False
    
    def calculate_total(self, include_tax: bool = True) -> float:
        """Calculate total price of all items."""
        subtotal = sum(item.price for item in self._items)
        if include_tax:
            return subtotal * (1 + self.tax_rate)
        return subtotal
    
    def filter_by_type(self, item_type: str) -> list[ShopItem]:
        """Get all items of a specific type."""
        return [item for item in self._items if item.item_type == item_type]
    
    def filter_by(self, condition: Callable[[ShopItem], bool]) -> list[ShopItem]:
        """Filter items by a custom condition."""
        return [item for item in self._items if condition(item)]
    
    def find_most_expensive(self) -> Optional[ShopItem]:
        """Find the most expensive item."""
        if not self._items:
            return None
        return max(self._items, key=lambda item: item.price)
    
    def find_cheapest(self) -> Optional[ShopItem]:
        """Find the cheapest item."""
        if not self._items:
            return None
        return min(self._items, key=lambda item: item.price)
    
    def apply_discount(self, discount: float) -> list[ShopItem]:
        """Return items with discount applied (doesn't modify originals)."""
        return [item.with_discount(discount) for item in self._items]
    
    def get_price_range(self, min_price: float, max_price: float) -> list[ShopItem]:
        """Get items within a price range."""
        return [
            item for item in self._items
            if min_price <= item.price <= max_price
        ]
    
    def sort_by_price(self, ascending: bool = True) -> list[ShopItem]:
        """Get items sorted by price."""
        return sorted(self._items, key=lambda item: item.price, reverse=not ascending)
    
    def get_statistics(self) -> dict:
        """Get statistical information about the shop."""
        if not self._items:
            return {"message": "No items in shop"}
        
        prices = [item.price for item in self._items]
        types = {}
        for item in self._items:
            types[item.item_type] = types.get(item.item_type, 0) + 1
        
        return {
            "total_items": len(self._items),
            "total_value": sum(prices),
            "average_price": sum(prices) / len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "items_by_type": types
        }
    
    def display_inventory(self) -> None:
        """Display formatted inventory."""
        print(f"\n🏪 {self.name} Inventory")
        print("=" * 50)
        
        for item_type in set(item.item_type for item in self._items):
            type_items = self.filter_by_type(item_type)
            print(f"\n[I] {item_type.upper()}:")
            for item in type_items:
                print(f"   • {item.name}: ${item.price:.2f}")
        
        print("\n" + "=" * 50)
        stats = self.get_statistics()
        print(f"Total Items: {stats['total_items']}")
        print(f"Total Value: ${stats['total_value']:.2f}")
        print(f"With Tax ({self.tax_rate*100:.0f}%): ${self.calculate_total():.2f}")


# Demo usage
if __name__ == "__main__":
    # Create shop
    shop = Shop("Adventure Supplies", tax_rate=0.15)
    
    # Add items (using both methods)
    shop.add_item("Sword", 100, "weapon")
    shop.add_item("Shield", 75, "armor")
    
    shop.add_items([
        {"name": "Potion", "price": 25, "type": "consumable"},
        {"name": "Bow", "price": 120, "type": "weapon"},
        {"name": "Helmet", "price": 60, "type": "armor"},
    ])
    
    # Display inventory
    shop.display_inventory()
    
    # Find weapons
    print("\n[I] Weapons available:")
    for weapon in shop.filter_by_type("weapon"):
        print(f"   {weapon}")
    
    # Most expensive
    expensive = shop.find_most_expensive()
    print(f"\n[I] Most expensive: {expensive}")
    
    # Apply discount
    print("\n[I] 20% Discount Sale:")
    for item in shop.apply_discount(0.20):
        print(f"   {item}")
    
    # Custom filter
    print("\n[I] Items under $80:")
    affordable = shop.filter_by(lambda x: x.price < 80)
    for item in affordable:
        print(f"   {item}")
