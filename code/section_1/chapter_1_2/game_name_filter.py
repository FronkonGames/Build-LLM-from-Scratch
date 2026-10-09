# Quest 1.2: Filter "Good" and "Bad" Game Names
# Practice with control flow, conditions, and loops

# ===== GAME NAME CONFIGURATION =====

game_name = "Stardew Valley"
name_length = len(game_name)   # in characters
has_numbers = False
is_catchy = True
has_alliteration = game_name.split()[0][0].lower() == game_name.split()[-1][0].lower() if len(game_name.split()) > 1 else False

# ===== ANALYSIS SIMULATION =====

print("=" * 50)
print("     [I] AI NAME QUALITY CONTROL")
print("=" * 50)
print()
print(f"Analyzing: '{game_name}'")
print("-" * 50)

# Simulate analysis passes with a loop
for pass_num in range(1, 4):
    print(f"   Pass {pass_num}/3: ", end="")
    
    if pass_num == 1:
        print(f"Checking length ({name_length} chars)...")
    elif pass_num == 2:
        print(f"Evaluating catchiness...")
    else:
        print(f"Assessing memorability...")

print("-" * 50)
print()

# ===== VERDICT LOGIC =====

# Multiple conditions using and/or
is_too_long = name_length > 30
is_too_short = name_length < 5
has_special_chars = any(c in game_name for c in "!@#$%")
is_memorable = name_length <= 20 and is_catchy

print("[I] Analysis Results:")
print(f"   Length:           {'[W] Too long' if is_too_long else '[W] Too short' if is_too_short else '[I] Good'}")
print(f"   Catchy:           {'[I] Yes' if is_catchy else '[!] No'}")
print(f"   Alliteration:     {'[I] Yes' if has_alliteration else '[!] No'}")
print(f"   Has Numbers:      {'[W] Yes' if has_numbers else '[I] No'}")
print()

# Main verdict using if/elif/else chain
print("[I] VERDICT: ", end="")

if is_too_long:
    print("[!] TOO LONG")
    print("   Gamers won't remember this name!")
    verdict_score = 3
elif has_numbers:
    print("[W] HAS NUMBERS")
    print("   Might be confused with a sequel.")
    verdict_score = 5
elif is_memorable and has_alliteration:
    print("[I] CATCHY GEM!")
    print("   Short, memorable, and fun to say!")
    verdict_score = 10
elif is_memorable:
    print("[I] SOLID NAME")
    print("   Good length and catchiness.")
    verdict_score = 8
else:
    print("[I] NEEDS WORK")
    print("   Try something shorter or more distinctive.")
    verdict_score = 6

print()

# ===== SCORE VISUALIZATION =====

print(f"[I] Name Score: {verdict_score}/10")
print(f"   [{'*' * verdict_score}{'o' * (10 - verdict_score)}]")
print()

# ===== BATCH ANALYSIS EXAMPLE =====

print("=" * 50)
print("     [I] BATCH ANALYSIS MODE")
print("=" * 50)

# A list of game names to analyze
game_names = [
    "Stardew Valley",
    "Dark Souls III",
    "Celeste",
    "Hollow Knight",
    "The Legend of Zelda"
]

min_length = 8   # Minimum threshold
max_length = 30  # Maximum threshold

print(f"\nFiltering names between {min_length}-{max_length} characters:\n")

passed = 0
failed = 0

for name in game_names:
    name_len = len(name)
    
    if min_length <= name_len <= max_length:
        print(f"   [I] '{name}' ({name_len} chars)")
        passed += 1
    else:
        reason = "Too short!" if name_len < min_length else "Too long!"
        print(f"   [!] '{name}' ({name_len} chars) - {reason}")
        failed += 1

print()
print(f"Results: {passed} passed, {failed} failed")
print(f"Pass rate: {(passed / len(game_names)) * 100:.0f}%")
print()
print("=" * 50)
print("[I] Quest 1.2 Complete! +30 XP")
print("=" * 50)
