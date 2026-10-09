# Quest 1.6: Load Game Names from Disk Safely
# Practice with file I/O, exceptions, and JSON

import json
from pathlib import Path
from datetime import datetime


class GameNameDatabase:
    """
    A database for storing and retrieving game names.
    
    Supports both text and JSON storage formats with
    error handling and backup functionality.
    """
    
    def __init__(self, db_path: str = "names.json"):
        """
        Initialize the database.
        
        Args:
            db_path: Path to the database file.
        """
        self.db_path = Path(db_path)
        self.names: list[dict] = []
        self._load()
    
    def _load(self) -> None:
        """Load names from the database file."""
        if not self.db_path.exists():
            print(f"[I] Database not found at {self.db_path}")
            print("   Creating new database...")
            self._create_default()
            return
        
        try:
            content = self.db_path.read_text(encoding="utf-8")
            self.names = json.loads(content)
            print(f"[I] Loaded {len(self.names)} names from {self.db_path}")
        except json.JSONDecodeError as e:
            print(f"[!] Error: Database file is corrupted!")
            print(f"   Details: {e}")
            self._create_backup()
            self._create_default()
        except Exception as e:
            print(f"[!] Unexpected error loading database: {e}")
            self.names = []
    
    def _save(self) -> bool:
        """Save names to the database file."""
        try:
            content = json.dumps(self.names, indent=2, ensure_ascii=False)
            self.db_path.write_text(content, encoding="utf-8")
            return True
        except IOError as e:
            print(f"[!] Error saving database: {e}")
            return False
    
    def _create_default(self) -> None:
        """Create a default database with sample names."""
        self.names = [
            {
                "id": 1,
                "full_name": "Stardew Valley",
                "length": 14,
                "created": datetime.now().isoformat()
            },
            {
                "id": 2,
                "full_name": "Dark Souls III",
                "length": 14,
                "created": datetime.now().isoformat()
            },
            {
                "id": 3,
                "full_name": "Celeste",
                "length": 7,
                "created": datetime.now().isoformat()
            }
        ]
        self._save()
        print(f"[I] Created default database with {len(self.names)} names")
    
    def _create_backup(self) -> None:
        """Create a backup of the current database file."""
        if self.db_path.exists():
            backup_path = self.db_path.with_suffix(".backup.json")
            try:
                backup_path.write_bytes(self.db_path.read_bytes())
                print(f"[I] Backup created at {backup_path}")
            except IOError as e:
                print(f"[W] Could not create backup: {e}")
    
    def add_name(self, full_name: str) -> dict:
        """
        Add a new name to the database.
        
        Args:
            full_name: The complete game name.
        
        Returns:
            The newly created name dictionary.
        """
        # Generate new ID
        new_id = max((name["id"] for name in self.names), default=0) + 1
        
        name = {
            "id": new_id,
            "full_name": full_name,
            "length": len(full_name),
            "created": datetime.now().isoformat()
        }
        
        self.names.append(name)
        
        if self._save():
            print(f"[I] Added name #{new_id}: {full_name}")
        
        return name
    
    def remove_name(self, name_id: int) -> bool:
        """
        Remove a name by ID.
        
        Args:
            name_id: The ID of the name to remove.
        
        Returns:
            True if removed, False if not found.
        """
        for i, name in enumerate(self.names):
            if name["id"] == name_id:
                removed = self.names.pop(i)
                self._save()
                print(f"[I] Removed name #{name_id}: {removed['full_name']}")
                return True
        
        print(f"[!] Name #{name_id} not found")
        return False
    
    def search(self, keyword: str) -> list[dict]:
        """
        Search names by keyword.
        
        Args:
            keyword: Text to search for (case-insensitive).
        
        Returns:
            List of matching names.
        """
        keyword = keyword.lower()
        return [
            name for name in self.names
            if keyword in name["full_name"].lower()
        ]
    
    def get_all(self) -> list[dict]:
        """Get all names."""
        return self.names.copy()
    
    def get_by_id(self, name_id: int) -> dict | None:
        """Get a specific name by ID."""
        for name in self.names:
            if name["id"] == name_id:
                return name
        return None
    
    def get_stats(self) -> dict:
        """Get database statistics."""
        total_length = sum(name.get("length", 0) for name in self.names)
        avg_length = total_length / len(self.names) if self.names else 0
        
        return {
            "total_names": len(self.names),
            "avg_name_length": round(avg_length, 1),
            "database_path": str(self.db_path)
        }
    
    def display_all(self) -> None:
        """Display all names in a formatted table."""
        print(f"\n{'═' * 60}")
        print(f"  [I] GAME NAMES DATABASE ({len(self.names)} names)")
        print(f"{'═' * 60}")
        
        for name in self.names:
            print(f"\n  #{name['id']:3} | {name['full_name']} ({name['length']} chars)")
        
        print(f"\n{'═' * 60}")


# ===== SIMPLE TEXT FILE OPERATIONS =====

def load_text_file(filepath: str) -> list[str]:
    """
    Load lines from a text file safely.
    
    Args:
        filepath: Path to the text file.
    
    Returns:
        List of lines (stripped of whitespace).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            print(f"[I] Loaded {len(lines)} lines from {filepath}")
            return lines
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        return []
    except IOError as e:
        print(f"[!] Error reading file: {e}")
        return []


def save_text_file(filepath: str, lines: list[str]) -> bool:
    """
    Save lines to a text file.
    
    Args:
        filepath: Path to the text file.
        lines: List of lines to save.
    
    Returns:
        True if successful, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[I] Saved {len(lines)} lines to {filepath}")
        return True
    except IOError as e:
        print(f"[!] Error writing file: {e}")
        return False


# ===== DEMONSTRATION =====

if __name__ == "__main__":
    print("=" * 60)
    print("         [I] FILE I/O & DATABASE DEMO")
    print("=" * 60)
    print()
    
    # Initialize database (will create default if not exists)
    db = GameNameDatabase("code/python_basics/game_names.json")
    print()
    
    # Display all names
    db.display_all()
    
    # Add a new name
    print("\n[I] Adding new name...")
    db.add_name("Hollow Knight")
    
    # Search for names
    print("\n[I] Searching for 'dark'...")
    results = db.search("dark")
    for name in results:
        print(f"   Found: {name['full_name']}")
    if not results:
        print("   No matches found")
    
    # Show statistics
    print("\n[I] Database Stats:")
    stats = db.get_stats()
    print(f"   Total Names: {stats['total_names']}")
    print(f"   Avg Length: {stats['avg_name_length']} chars")
    print(f"   Location: {stats['database_path']}")
    
    # Text file demo
    print("\n" + "=" * 60)
    print("         [I] TEXT FILE DEMO")
    print("=" * 60)
    
    text_file = "code/python_basics/names.txt"
    
    # Try to load, create default if not exists
    lines = load_text_file(text_file)
    
    if not lines:
        print("\nCreating default text file...")
        default_lines = [
            "Stardew Valley",
            "Dark Souls III",
            "Celeste"
        ]
        save_text_file(text_file, default_lines)
        lines = load_text_file(text_file)
    
    print("\n[I] Names from text file:")
    for i, line in enumerate(lines, 1):
        print(f"   {i}. {line}")
    
    print()
    print("=" * 60)
    print("[I] Quest 1.6 Complete! +70 XP")
    print("=" * 60)
