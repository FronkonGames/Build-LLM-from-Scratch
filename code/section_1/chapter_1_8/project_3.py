import json
import re
from collections import Counter
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


class TextAnalyzer:
    """Analyze and visualize text data like game names."""
    
    # Common words to skip
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "this", "that",
        "these", "those", "it", "its", "you", "your", "we", "our", "they",
        "their", "he", "she", "him", "her", "as", "from", "into", "through"
    }
    
    def __init__(self, name: str = "Text Analysis"):
        self.name = name
        self.documents: list[str] = []
        self.word_counts: Counter = Counter()
        self.doc_lengths: list[int] = []
        self.unique_words: set = set()
        self._analyzed = False
    
    def add_document(self, text: str) -> None:
        """Add a document for analysis."""
        self.documents.append(text)
        self._analyzed = False
    
    def add_documents(self, texts: list[str]) -> None:
        """Add multiple documents."""
        self.documents.extend(texts)
        self._analyzed = False
    
    def _tokenize(self, text: str, remove_stopwords: bool = True) -> list[str]:
        """Convert text to lowercase word tokens."""
        # Remove punctuation and convert to lowercase
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        if remove_stopwords:
            words = [w for w in words if w not in self.STOPWORDS]
        
        return words
    
    def analyze(self, remove_stopwords: bool = True) -> dict:
        """Perform full analysis on all documents."""
        if not self.documents:
            return {"error": "No documents to analyze"}
        
        print(f"\n[I] Analyzing {len(self.documents)} documents...")
        
        self.word_counts = Counter()
        self.doc_lengths = []
        all_words = []
        
        for doc in tqdm(self.documents, desc="Processing"):
            words = self._tokenize(doc, remove_stopwords)
            all_words.extend(words)
            self.doc_lengths.append(len(words))
            self.word_counts.update(words)
        
        self.unique_words = set(all_words)
        self._analyzed = True
        
        return self.get_statistics()
    
    def get_statistics(self) -> dict:
        """Get comprehensive statistics about the analyzed text."""
        if not self._analyzed:
            return {"error": "Please run analyze() first"}
        
        lengths = np.array(self.doc_lengths)
        
        return {
            "total_documents": len(self.documents),
            "total_words": sum(self.doc_lengths),
            "unique_words": len(self.unique_words),
            "vocabulary_richness": len(self.unique_words) / sum(self.doc_lengths) if self.doc_lengths else 0,
            "document_length_stats": {
                "mean": float(np.mean(lengths)),
                "median": float(np.median(lengths)),
                "std": float(np.std(lengths)),
                "min": int(np.min(lengths)),
                "max": int(np.max(lengths))
            },
            "top_10_words": self.word_counts.most_common(10)
        }
    
    def display_statistics(self) -> None:
        """Display formatted statistics."""
        stats = self.get_statistics()
        
        if "error" in stats:
            print(f"[!] {stats['error']}")
            return
        
        print(f"\n[I] {self.name} - Statistics")
        print("=" * 50)
        print(f"Documents:        {stats['total_documents']:,}")
        print(f"Total Words:      {stats['total_words']:,}")
        print(f"Unique Words:     {stats['unique_words']:,}")
        print(f"Vocab Richness:   {stats['vocabulary_richness']:.4f}")
        
        print("\n[I] Document Length Statistics:")
        ls = stats['document_length_stats']
        print(f"   Mean:   {ls['mean']:.1f} words")
        print(f"   Median: {ls['median']:.1f} words")
        print(f"   Std:    {ls['std']:.1f}")
        print(f"   Range:  {ls['min']} - {ls['max']} words")
        
        print("\n[I] Top 10 Words:")
        for word, count in stats['top_10_words']:
            bar = "█" * (count * 20 // stats['top_10_words'][0][1])
            print(f"   {word:15} {bar} {count:,}")
    
    def plot_word_frequencies(self, top_n: int = 20, save_path: Optional[str] = None) -> None:
        """Create bar chart of most common words."""
        if not self._analyzed:
            print("[!] Please run analyze() first")
            return
        
        words, counts = zip(*self.word_counts.most_common(top_n))
        
        plt.figure(figsize=(12, 6))
        colors = plt.cm.viridis(np.linspace(0, 0.8, top_n))
        plt.barh(range(len(words)), counts, color=colors)
        plt.yticks(range(len(words)), words)
        plt.xlabel("Frequency")
        plt.title(f"Top {top_n} Most Common Words")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"[I] Saved to {save_path}")
        plt.show()
    
    def plot_length_distribution(self, bins: int = 30, save_path: Optional[str] = None) -> None:
        """Create histogram of document lengths."""
        if not self._analyzed:
            print("[!] Please run analyze() first")
            return
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.doc_lengths, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
        
        mean_len = np.mean(self.doc_lengths)
        plt.axvline(mean_len, color='red', linestyle='dashed', label=f'Mean: {mean_len:.1f}')
        
        plt.xlabel("Document Length (words)")
        plt.ylabel("Frequency")
        plt.title("Distribution of Document Lengths")
        plt.legend()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"[I] Saved to {save_path}")
        plt.show()
    
    def plot_vocabulary_coverage(self, save_path: Optional[str] = None) -> None:
        """Show cumulative word coverage."""
        if not self._analyzed:
            print("[!] Please run analyze() first")
            return
        
        # Sort words by frequency
        sorted_counts = sorted(self.word_counts.values(), reverse=True)
        cumulative = np.cumsum(sorted_counts) / sum(sorted_counts) * 100
        
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(cumulative) + 1), cumulative, linewidth=2)
        
        # Find 80% and 90% coverage points
        idx_80 = np.searchsorted(cumulative, 80)
        idx_90 = np.searchsorted(cumulative, 90)
        
        plt.axhline(80, color='orange', linestyle='--', alpha=0.7)
        plt.axvline(idx_80, color='orange', linestyle='--', alpha=0.7, 
                   label=f'80% coverage: {idx_80} words')
        
        plt.axhline(90, color='red', linestyle='--', alpha=0.7)
        plt.axvline(idx_90, color='red', linestyle='--', alpha=0.7,
                   label=f'90% coverage: {idx_90} words')
        
        plt.xlabel("Number of Words (sorted by frequency)")
        plt.ylabel("Cumulative Coverage (%)")
        plt.title("Vocabulary Coverage Analysis")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"[I] Saved to {save_path}")
        plt.show()
    
    def generate_report(self, output_dir: str = "analysis_output") -> None:
        """Generate a complete analysis report with all visualizations."""
        if not self._analyzed:
            self.analyze()
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n[I] Generating report in {output_dir}/...")
        
        # Save statistics as JSON
        stats = self.get_statistics()
        (output_path / "statistics.json").write_text(json.dumps(stats, indent=2))
        print("   [I] statistics.json")
        
        # Generate visualizations
        self.plot_word_frequencies(save_path=str(output_path / "word_frequencies.png"))
        self.plot_length_distribution(save_path=str(output_path / "length_distribution.png"))
        self.plot_vocabulary_coverage(save_path=str(output_path / "vocabulary_coverage.png"))
        
        print(f"\n[I] Report complete! Check {output_dir}/ for results.")


# Demo with sample game names
if __name__ == "__main__":
    # Sample game names
    game_names = [
        "An epic action RPG where you explore vast dungeons and defeat powerful dragons. Collect legendary weapons and armor to become the ultimate hero.",
        "A peaceful farming simulator where you build your dream farm, raise animals, and make friends with the townspeople. Relax and enjoy country life.",
        "Fast-paced racing game with realistic physics and stunning graphics. Compete against players worldwide in thrilling multiplayer races.",
        "A survival horror game set in an abandoned hospital. Solve puzzles, avoid terrifying monsters, and uncover the dark secrets of the past.",
        "Build and manage your own city in this strategic simulation game. Balance resources, keep citizens happy, and grow your metropolis.",
        "A story-driven adventure game with beautiful hand-drawn art. Make meaningful choices that affect the narrative and character relationships.",
        "Intense first-person shooter with tactical gameplay. Work with your squad to complete missions and dominate the battlefield.",
        "A cozy puzzle game with hundreds of challenging levels. Match colors, solve brain teasers, and unlock new worlds.",
        "Open-world exploration game where you discover ancient ruins and forgotten civilizations. Document your findings and become a legendary explorer.",
        "Rhythm game featuring popular songs and custom beatmaps. Perfect your timing and climb the global leaderboards."
    ]
    
    # Create analyzer and run analysis
    analyzer = TextAnalyzer("Game Name Analysis")
    analyzer.add_documents(game_names)
    analyzer.analyze()
    
    # Display results
    analyzer.display_statistics()
    
    # Generate visualizations (comment out if you just want to test)
    # analyzer.plot_word_frequencies()
    # analyzer.plot_length_distribution()
    # analyzer.plot_vocabulary_coverage()
    
    # Or generate complete report
    # analyzer.generate_report("game_analysis")
