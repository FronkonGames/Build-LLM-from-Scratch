# Quest 1.3: Store a Mini Steam-like Catalog
# Practice with lists, dictionaries, and data structures

# ===== DATA STRUCTURES =====

# A list of genres
genres = ["Action", "RPG", "Simulation", "Puzzle", "Strategy", "Horror"]

# A catalog of games (List of Dictionaries)
catalog = [
    {
        "title": "Stardew Valley",
        "genre": "Simulation",
        "price": 14.99,
        "rating": 9.5,
        "tags": ["relaxing", "farming", "pixel-art"]
    },
    {
        "title": "Elden Ring",
        "genre": "RPG",
        "price": 59.99,
        "rating": 9.8,
        "tags": ["difficult", "open-world", "fantasy"]
    },
    {
        "title": "Portal 2",
        "genre": "Puzzle",
        "price": 9.99,
        "rating": 9.9,
        "tags": ["physics", "co-op", "humor"]
    },
    {
        "title": "Hades",
        "genre": "Action",
        "price": 24.99,
        "rating": 9.7,
        "tags": ["roguelike", "mythology", "fast-paced"]
    },
    {
        "title": "Civilization VI",
        "genre": "Strategy",
        "price": 29.99,
        "rating": 8.8,
        "tags": ["turn-based", "historical", "4X"]
    }
]

# ===== CATALOG REPORT =====

print("=" * 60)
print("              [I] STEAM MINI-CATALOG")
print("=" * 60)
print()

print(f"[I] Catalog Statistics:")
print(f"   Total Games: {len(catalog)}")
print(f"   Genres Available: {len(genres)}")
print()

# ===== LIST ALL GAMES =====

print("[I] Full Catalog:")
print("-" * 60)

for game in catalog:
    title = game["title"]
    genre = game["genre"]
    price = game["price"]
    rating = game["rating"]
    
    # Star rating visualization
    stars = "*" * int(rating // 2) + "o" * (5 - int(rating // 2))
    
    print(f"   {title}")
    print(f"      Genre: {genre} | Price: ${price:.2f} | Rating: {stars} ({rating})")
    print(f"      Tags: {', '.join(game['tags'])}")
    print()

# ===== FILTERING EXAMPLES =====

print("=" * 60)
print("              [I] FILTERED VIEWS")
print("=" * 60)
print()

# Filter: Games under $20
print("[I] Budget-Friendly (Under $20):")
budget_games = [g for g in catalog if g["price"] < 20]
for game in budget_games:
    print(f"   • {game['title']} - ${game['price']:.2f}")
print()

# Filter: Games by genre
target_genre = "RPG"
print(f"[I] {target_genre} Games:")
genre_games = [g for g in catalog if g["genre"] == target_genre]
for game in genre_games:
    print(f"   • {game['title']}")
if not genre_games:
    print(f"   No {target_genre} games found.")
print()

# Filter: Top rated (9.5+)
print("[I] Top Rated (9.5+):")
top_games = [g for g in catalog if g["rating"] >= 9.5]
for game in sorted(top_games, key=lambda x: x["rating"], reverse=True):
    print(f"   • {game['title']} ({game['rating']})")
print()

# ===== AGGREGATE DATA =====

print("=" * 60)
print("              [I] ANALYTICS")
print("=" * 60)
print()

# Calculate totals
total_value = sum(game["price"] for game in catalog)
avg_price = total_value / len(catalog)
avg_rating = sum(game["rating"] for game in catalog) / len(catalog)

print(f"💵 Total Catalog Value: ${total_value:.2f}")
print(f"[I] Average Price: ${avg_price:.2f}")
print(f"⭐ Average Rating: {avg_rating:.1f}/10")
print()

# Get all unique tags
all_tags = set()
for game in catalog:
    all_tags.update(game["tags"])

print(f"[I] All Tags ({len(all_tags)} unique):")
print(f"   {', '.join(sorted(all_tags))}")
print()

# Find the best game
best_game = max(catalog, key=lambda x: x["rating"])
print(f"[I] Highest Rated: {best_game['title']} ({best_game['rating']})")
print()

print("=" * 60)
print("[I] Quest 1.3 Complete! +40 XP")
print("=" * 60)
