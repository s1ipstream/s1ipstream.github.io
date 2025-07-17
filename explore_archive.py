import json
import pandas as pd
import numpy as np
from collections import Counter

def load_index(filename="archive_index.jsonl"):
    """Load the archive index"""
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

def show_stats(df):
    """Show basic statistics about the archive"""
    print("📊 DOS ARCHIVE STATISTICS")
    print("=" * 50)
    print(f"Total files indexed: {len(df):,}")
    print(f"Total words: {df['wordcount'].sum():,}")
    print(f"Average words per file: {df['wordcount'].mean():.0f}")
    
    print("\n📏 File size distribution:")
    print(f"  • Shortest: {df['wordcount'].min()} words")
    print(f"  • Longest: {df['wordcount'].max():,} words") 
    print(f"  • Median: {df['wordcount'].median():.0f} words")

def analyze_tags(df):
    """Analyze tag distribution and co-occurrence"""
    print("\n🏷️ TAG ANALYSIS")
    print("=" * 50)

    # Convert string representations of lists to actual lists and handle NaN
    def parse_tags(x):
        if isinstance(x, list):
            return x
        if pd.isnull(x):
            return []
        try:
            return eval(x) if isinstance(x, str) else []
        except:
            return []

    # Convert all tag columns to proper lists
    tag_columns = ['all_tags', 'theme_tags', 'pattern_tags', 'debug_tags', 'app_tags']
    for col in tag_columns:
        if col in df.columns:
            df[col] = df[col].apply(parse_tags)
    
    # Now we can safely get files with tags
    files_with_tags = df[df['all_tags'].apply(len) > 0]
    
    if len(files_with_tags) == 0:
        print("No files found with tags!")
        return

    print(f"\nFiles with tags: {len(files_with_tags)} ({len(files_with_tags)/len(df)*100:.1f}%)")
    
    # Get all unique tags
    all_tags = set()
    for tags in files_with_tags['all_tags']:
        all_tags.update(tags)
    
    print(f"Total unique tags: {len(all_tags)}")
    
    # Tag frequency
    tag_counts = {}
    for tags in files_with_tags['all_tags']:
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
    print("\nMost common tags:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {tag}: {count} files")

    # Analyze by category
    print("\n📊 Tags by Category:")
    for col, title in [
        ('theme_tags', 'Themes'),
        ('pattern_tags', 'Patterns'),
        ('debug_tags', 'Debug Protocols'),
        ('app_tags', 'Applications')
    ]:
        if col in df.columns:
            category_tags = []
            for tags in df[col]:
                if isinstance(tags, list):
                    category_tags.extend(tags)
            
            if category_tags:
                print(f"\n{title}:")
                counter = Counter(category_tags)
                for tag, count in counter.most_common():
                    print(f"  • {tag}: {count} files")
            else:
                print(f"\n{title}: No tags found")

def search_files(df, themes=None, patterns=None, debug_tags=None, min_words=None, max_results=10):
    """Search files based on tags and word count"""
    print("\n🔍 SEARCH RESULTS:", end=" ")
    
    # Start with all files
    results = df.copy()
    
    # Filter by themes
    if themes:
        theme_mask = results['theme_tags'].apply(lambda x: any(tag in x for tag in themes) if isinstance(x, list) else False)
        results = results[theme_mask]
    
    # Filter by patterns
    if patterns:
        pattern_mask = results['pattern_tags'].apply(lambda x: any(tag in x for tag in patterns) if isinstance(x, list) else False)
        results = results[pattern_mask]
    
    # Filter by debug tags
    if debug_tags:
        debug_mask = results['debug_tags'].apply(lambda x: any(tag in x for tag in debug_tags) if isinstance(x, list) else False)
        results = results[debug_mask]
    
    # Filter by minimum word count
    if min_words:
        results = results[results['wordcount'] >= min_words]
    
    print(f"{len(results)} files found")
    print("=" * 50)
    
    if len(results) == 0:
        return
    
    # Sort by word count if available, otherwise by filename
    if 'wordcount' in results.columns:
        results = results.sort_values('wordcount', ascending=False)
    
    # Display top results
    for i, (_, row) in enumerate(results.head(max_results).iterrows(), 1):
        print(f"\n📄 {i}. {row['filename']}")
        if 'wordcount' in row:
            print(f"   Words: {row['wordcount']}")
        if 'theme_tags' in row and isinstance(row['theme_tags'], list):
            print(f"   Tags: {', '.join(row['theme_tags'][:5])}")
        if 'first_500_chars' in row:
            print(f"   Preview: {row['first_500_chars'][:100]}...")

def show_richest_files(df, top_n=10):
    """Show files with the most tags"""
    df['tag_count'] = df['all_tags'].apply(len)
    richest = df.nlargest(top_n, 'tag_count')
    
    print(f"\n🌟 RICHEST FILES (most tags):")
    print("=" * 50)
    
    for i, (idx, row) in enumerate(richest.iterrows()):
        print(f"\n{i+1}. {row['filename']} ({row['tag_count']} tags)")
        print(f"   Words: {row['wordcount']:,}")
        print(f"   Tags: {', '.join(row['all_tags'])}")
        print(f"   Preview: {row['summary'][:100]}...")

# Load and analyze the archive
print("🚀 Loading DOS Archive...")
df = load_index()

# Show basic stats
show_stats(df)

# Analyze tags
analyze_tags(df)

# Show richest files
show_richest_files(df, 5)

# Example searches
print("\n" + "="*60)
print("🔍 EXAMPLE SEARCHES")
print("="*60)

print("\n1. Files about merge/separate and timing:")
search_files(df, 
            patterns=['merge_separate', 'timing_misalignment'], 
            max_results=3)

print("\n2. Files about consciousness debugging:")
search_files(df, 
            themes=['consciousness_debugging'], 
            debug_tags=['overwhelm_debugging'], 
            max_results=3)

print("\n3. Substantial files about pattern recognition:")
search_files(df, 
            themes=['pattern_recognition'], 
            min_words=1000, 
            max_results=3)

print("\n" + "="*60)
print("🎯 INTERACTIVE SEARCH FUNCTIONS READY!")
print("="*60)
print("\nYou can now use:")
print("  • search_files(df, themes=['theme_name'])")
print("  • search_files(df, patterns=['pattern_name'])")  
print("  • search_files(df, debug_tags=['debug_name'])")
print("  • search_files(df, min_words=500)")
print("\nExample:")
print("  search_files(df, themes=['boundary_architecture'], patterns=['recursive_collapse'])")