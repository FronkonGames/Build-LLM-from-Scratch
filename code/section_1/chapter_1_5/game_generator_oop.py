# Quest 1.5: Create a GameNameGenerator Class
# Practice with classes, objects, and methods

import random
from datetime import datetime


class GameNameGenerator:
    """
    A class that generates random game names.
    
    This generator combines prefixes, core words, and suffixes
    to create unique game titles.
    
    Attributes:
        author: The name of the generator's creator.
        version: Version number of the generator.
        specialty: The generator's area of expertise.
        history: List of all generated names.
    """
    
    # Class attributes (shared by all instances)
    DEFAULT_PREFIXES = [
        "Dark", "Super", "Final", "Stardew", "Hollow", 
        "Celeste", "Dead", "Ori", "Cult", "Fire"
    ]
    
    DEFAULT_CORES = [
        "Souls", "Mario", "Fantasy", "Valley", "Knight",
        "Cells", "Emblem", "Watcher", "Lamb", "Emblem"
    ]
    
    DEFAULT_SUFFIXES = [
        "", "II", "III", "IV", "V",
        "Odyssey", "Deluxe", "Remastered", "Online", "Ultimate"
    ]
    
    def __init__(self, author: str, version: str = "1.0.0", specialty: str = "All Genres"):
        """
        Initialize a new GameNameGenerator.
        
        Args:
            author: Name of the creator.
            version: Version string (default: "1.0.0").
            specialty: Area of expertise (default: "All Genres").
        """
        self.author = author
        self.version = version
        self.specialty = specialty
        self.history: list[dict] = []
        self._creation_time = datetime.now()
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"GameNameGenerator v{self.version} by {self.author} ({self.specialty})"
    
    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"GameNameGenerator(author='{self.author}', version='{self.version}')"
    
    def __len__(self) -> int:
        """Return the number of names generated."""
        return len(self.history)
    
    @property
    def stats(self) -> dict:
        """Get generator statistics."""
        return {
            "total_names": len(self.history),
            "author": self.author,
            "version": self.version,
            "specialty": self.specialty,
            "created": self._creation_time.strftime("%Y-%m-%d %H:%M")
        }
    
    def generate(self, prefix: str = None, core: str = None, suffix: str = None) -> dict:
        """
        Generate a new game name.
        
        Args:
            prefix: Specific prefix (random if None).
            core: Specific core word (random if None).
            suffix: Specific suffix (random if None, can be empty).
        
        Returns:
            A dictionary containing the complete game name.
        """
        # Use provided values or pick randomly
        name_prefix = prefix or random.choice(self.DEFAULT_PREFIXES)
        name_core = core or random.choice(self.DEFAULT_CORES)
        name_suffix = suffix if suffix is not None else random.choice(self.DEFAULT_SUFFIXES)
        
        # Build the full name
        full_name = f"{name_prefix} {name_core}".strip()
        if name_suffix:
            full_name += f" {name_suffix}"
        
        # Create the name entry
        name_entry = {
            "id": len(self.history) + 1,
            "prefix": name_prefix,
            "core": name_core,
            "suffix": name_suffix,
            "full_name": full_name,
            "length": len(full_name),
            "timestamp": datetime.now().isoformat(),
            "author": self.author
        }
        
        # Add to history
        self.history.append(name_entry)
        
        return name_entry
    
    def display_name(self, name_entry: dict) -> None:
        """Display a formatted game name."""
        print(f"╔{'═' * 50}╗")
        print(f"║ [I] GAME NAME #{name_entry['id']:<38}║")
        print(f"╠{'═' * 50}╣")
        print(f"║ Full Name: {name_entry['full_name'][:36]:<36}║")
        print(f"║ Length:    {name_entry['length']} characters{'':<29}║")
        print(f"╚{'═' * 50}╝")
    
    def generate_and_display(self, **kwargs) -> dict:
        """Generate a name and display it immediately."""
        name_entry = self.generate(**kwargs)
        self.display_name(name_entry)
        return name_entry
    
    def get_history(self, limit: int = None) -> list[dict]:
        """
        Get the generation history.
        
        Args:
            limit: Maximum number of names to return (most recent first).
        
        Returns:
            List of name dictionaries.
        """
        if limit:
            return list(reversed(self.history[-limit:]))
        return list(reversed(self.history))
    
    def rate_name(self, name_id: int, rating: int) -> bool:
        """
        Rate an existing name (1-5 stars).
        
        Args:
            name_id: The ID of the name to rate.
            rating: Rating from 1 to 5.
        
        Returns:
            True if successful, False if name not found.
        """
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5!")
            return False
        
        for name_entry in self.history:
            if name_entry["id"] == name_id:
                name_entry["rating"] = rating
                name_entry["rating_display"] = "*" * rating + "o" * (5 - rating)
                return True
        
        return False
    
    def show_stats(self) -> None:
        """Display generator statistics."""
        stats = self.stats
        print(f"\n[I] Generator Statistics:")
        print(f"   Author: {stats['author']}")
        print(f"   Version: {stats['version']}")
        print(f"   Specialty: {stats['specialty']}")
        print(f"   Total Names: {stats['total_names']}")
        print(f"   Created: {stats['created']}")


# ===== DEMONSTRATION =====

if __name__ == "__main__":
    print("=" * 54)
    print("         [I] GAME NAME GENERATOR")
    print("=" * 54)
    print()
    
    # Create a generator instance
    my_gen = GameNameGenerator(
        author="Player One",
        version="0.6.0",
        specialty="Indie Games"
    )
    
    print(f"Created: {my_gen}")
    print()
    
    # Generate some names
    print("Generating names...\n")
    
    # Random name
    my_gen.generate_and_display()
    print()
    
    # Specific prefix
    my_gen.generate_and_display(prefix="Dark")
    print()
    
    # Fully specified
    my_gen.generate_and_display(
        prefix="Super",
        core="Mario",
        suffix="Odyssey"
    )
    print()
    
    # Rate a name
    my_gen.rate_name(1, 4)
    my_gen.rate_name(2, 5)
    
    # Show history
    print("[I] Recent Names:")
    for name_entry in my_gen.get_history(limit=3):
        rating = name_entry.get("rating_display", "Not rated")
        print(f"   #{name_entry['id']}: {name_entry['full_name']} - {rating}")
    print()
    
    # Show stats
    my_gen.show_stats()
    print()
    
    print("=" * 54)
    print("[I] Quest 1.5 Complete! +60 XP")
    print("=" * 54)
