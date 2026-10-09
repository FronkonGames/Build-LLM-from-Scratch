# Quest 1.1: Game Name Generator (Manual)
# Practice with variables, types, and f-strings

# ===== NAME COMPONENTS =====
# These are our building blocks for creating game names - try changing them!

prefix = "Stardew"      # e.g., "Dark", "Super", "Final"
core = "Valley"         # e.g., "Souls", "Fantasy", "Craft"
suffix = ""             # e.g., "III", "Odyssey", "Online" (can be empty!)

# Alternative examples to try:
# prefix = "Dark"
# core = "Souls"
# suffix = "III"

# ===== BASIC NAME =====

print("=" * 50)
print("         [I] GAME NAME GENERATOR")
print("=" * 50)
print()

print("[I] Name Components:")
print(f"   Prefix:  '{prefix}'")
print(f"   Core:    '{core}'")
print(f"   Suffix:  '{suffix}'")
print()

# ===== FORMATTED GAME NAME =====

# Combine components, stripping extra spaces if suffix is empty
game_name = f"{prefix} {core} {suffix}".strip()
print("💡 Generated Game Name:")
print(f"   {game_name}")
print()

# ===== CATCHINESS SCORE =====
# Let's calculate a "catchiness score" based on name length and alliteration

total_characters = len(prefix) + len(core) + len(suffix)
# Ideal game names are typically 10-30 characters
catchiness_score = max(0, 100 - abs(20 - total_characters) * 5)

print("[I] Stats:")
print(f"   Total Characters: {total_characters}")
print(f"   Catchiness Score: {catchiness_score}/100")
print(f"   Name Length: {len(game_name)} characters")
print()

# Visual score bar
filled = catchiness_score // 10
empty = 10 - filled
print(f"   [{'█' * filled}{'░' * empty}] {catchiness_score}%")
print()

# ===== TYPE INFORMATION =====
# Let's explore the types of our variables

print("[I] Variable Types (for learning):")
print(f"   prefix is a {type(prefix).__name__}: '{prefix}'")
print(f"   core is a {type(core).__name__}: '{core}'")
print(f"   catchiness_score is an {type(catchiness_score).__name__}: {catchiness_score}")
print()

print("=" * 50)
print("[I] Quest 1.1 Complete! +20 XP")
print("=" * 50)

# ===== CHALLENGE =====
# Try using input() to get values from the user!
# Example:
# prefix = input("Enter a name prefix (or press Enter to skip): ")
# core = input("Enter the core word: ")
# suffix = input("Enter a suffix (or press Enter to skip): ")
