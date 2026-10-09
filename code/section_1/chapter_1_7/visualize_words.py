# Quest 1.7: Visualize Word Frequencies
# Practice with NumPy, Matplotlib, and tqdm

# NOTE: Run 'uv pip install numpy matplotlib tqdm' first!

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from tqdm import tqdm
import time


def analyze_text(texts: list[str], show_progress: bool = True) -> dict:
    """
    Analyze word frequencies in a list of texts.
    
    Args:
        texts: List of text strings to analyze.
        show_progress: Whether to show progress bar.
    
    Returns:
        Dictionary with frequencies, stats, and top words.
    """
    all_words = []
    text_lengths = []
    
    # Process each text
    iterator = tqdm(texts, desc="Processing texts") if show_progress else texts
    
    for text in iterator:
        # Simple tokenization: lowercase and split on spaces
        words = text.lower().split()
        # Remove punctuation from words
        words = [word.strip(".,!?;:'\"()[]") for word in words]
        # Filter out empty strings
        words = [w for w in words if w]
        
        all_words.extend(words)
        text_lengths.append(len(words))
        
        if show_progress:
            time.sleep(0.05)  # Small delay to see progress
    
    # Count frequencies
    word_counts = Counter(all_words)
    
    # Calculate statistics using NumPy
    lengths_array = np.array(text_lengths)
    
    return {
        "total_words": len(all_words),
        "unique_words": len(word_counts),
        "frequencies": dict(word_counts),
        "top_words": word_counts.most_common(20),
        "stats": {
            "mean_length": float(np.mean(lengths_array)),
            "median_length": float(np.median(lengths_array)),
            "std_length": float(np.std(lengths_array)),
            "min_length": int(np.min(lengths_array)),
            "max_length": int(np.max(lengths_array))
        },
        "text_lengths": text_lengths
    }


def plot_word_frequencies(analysis: dict, top_n: int = 15, color: str = "steelblue") -> None:
    """
    Create a bar chart of the most common words.
    
    Args:
        analysis: Dictionary from analyze_text().
        top_n: Number of top words to display.
        color: Bar color.
    """
    # Get top N words
    top_words = analysis["top_words"][:top_n]
    words, counts = zip(*top_words) if top_words else ([], [])
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create horizontal bar chart (easier to read labels)
    bars = plt.barh(range(len(words)), counts, color=color, edgecolor='black', alpha=0.8)
    
    # Customize
    plt.yticks(range(len(words)), words)
    plt.xlabel("Frequency", fontsize=12)
    plt.title(f"Top {top_n} Most Common Words", fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()  # Highest at top
    
    # Add value labels
    for bar, count in zip(bars, counts):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                 str(count), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.show()


def plot_length_distribution(analysis: dict) -> None:
    """
    Create a histogram of text lengths.
    
    Args:
        analysis: Dictionary from analyze_text().
    """
    lengths = analysis["text_lengths"]
    stats = analysis["stats"]
    
    plt.figure(figsize=(10, 6))
    
    # Create histogram
    n, bins, patches = plt.hist(lengths, bins=20, color='skyblue', 
                                edgecolor='black', alpha=0.7)
    
    # Add mean line
    mean = stats["mean_length"]
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, 
                label=f'Mean: {mean:.1f}')
    
    # Add median line
    median = stats["median_length"]
    plt.axvline(median, color='green', linestyle='dashed', linewidth=2,
                label=f'Median: {median:.1f}')
    
    plt.xlabel("Words per Text", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Distribution of Text Lengths", fontsize=14, fontweight='bold')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


def plot_vocabulary_coverage(analysis: dict) -> None:
    """
    Plot cumulative vocabulary coverage.
    
    Args:
        analysis: Dictionary from analyze_text().
    """
    # Sort words by frequency
    sorted_counts = sorted(analysis["frequencies"].values(), reverse=True)
    total = sum(sorted_counts)
    
    # Calculate cumulative coverage
    cumulative = np.cumsum(sorted_counts) / total * 100
    
    plt.figure(figsize=(10, 6))
    
    # Plot coverage curve
    plt.plot(range(1, len(cumulative) + 1), cumulative, 
             linewidth=2, color='purple')
    
    # Find coverage milestones
    for coverage in [50, 80, 90]:
        idx = np.searchsorted(cumulative, coverage)
        plt.axhline(coverage, color='gray', linestyle=':', alpha=0.5)
        plt.axvline(idx, color='gray', linestyle=':', alpha=0.5)
        plt.annotate(f'{coverage}% = {idx} words', 
                     xy=(idx, coverage), xytext=(idx + 10, coverage - 5),
                     fontsize=9, color='darkblue')
    
    plt.xlabel("Number of Words (by frequency)", fontsize=12)
    plt.ylabel("Cumulative Coverage (%)", fontsize=12)
    plt.title("Vocabulary Coverage Analysis", fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


# ===== SAMPLE DATA =====

SAMPLE_GAME_NAMES = [
    "Echoes of the Hollow Crown",
    "Sunridge Farm Stories",
    "Velocity Prime X",
    "Ward 17: Still Breathing",
    "Skyglass Metropolis",
    "Brushstroke Odyssey",
    "Zero Hour: Fireteam",
    "Chromatica Puzzle Box",
    "Forgotten Spires Chronicles",
    "Sync Rush Live",
    "Grimvault Ascendant",
    "Lanternfish Lake",
    "Bulwark Command",
    "Shockdrop Arena",
    "Arcana Deck Duelist",
    "Shadowfall: The Last Stand",
    "Eclipse Rift: Trials",
    "Pulse Arena: Prologue",
    "Blink of Fate: Legacy",
    "Quantum Nexus: Origin",
    "Chronos Path: Genesis",
    "Echoes of the Void: Revelation",
    "Starlight Rift: Origins",
    "Nebula Nexus: Legacy",
    "Galactic Rift Stories",
]


# ===== DEMONSTRATION =====

if __name__ == "__main__":
    print("=" * 60)
    print("         [I] WORD FREQUENCY VISUALIZER")
    print("=" * 60)
    print()
    
    # Analyze the sample game names
    print("Analyzing game names...\n")
    analysis = analyze_text(SAMPLE_GAME_NAMES)
    
    # Display statistics
    print("\n[I] Analysis Results:")
    print(f"   Total Words: {analysis['total_words']}")
    print(f"   Unique Words: {analysis['unique_words']}")
    print(f"   Vocabulary Richness: {analysis['unique_words']/analysis['total_words']:.2%}")
    print()
    
    print("[I] Text Length Statistics:")
    stats = analysis["stats"]
    print(f"   Mean: {stats['mean_length']:.1f} words")
    print(f"   Median: {stats['median_length']:.1f} words")
    print(f"   Std Dev: {stats['std_length']:.1f}")
    print(f"   Range: {stats['min_length']} - {stats['max_length']} words")
    print()
    
    print("[I] Top 10 Words:")
    for word, count in analysis["top_words"][:10]:
        bar = "█" * (count * 2)
        print(f"   {word:15} {bar} ({count})")
    print()
    
    # Generate visualizations
    print("Generating visualizations...")
    print("(Close each chart window to see the next one)")
    print()
    
    # Show charts one at a time
    print("[I] Chart 1: Word Frequencies")
    plot_word_frequencies(analysis, top_n=15, color='coral')
    
    print("[I] Chart 2: Text Length Distribution")
    plot_length_distribution(analysis)
    
    print("[I] Chart 3: Vocabulary Coverage")
    plot_vocabulary_coverage(analysis)
    
    print()
    print("=" * 60)
    print("[I] Quest 1.7 Complete! +80 XP")
    print("=" * 60)
