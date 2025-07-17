import json
import pandas as pd
from collections import Counter

# Load the archive
def load_index(filename="archive_index.jsonl"):
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

df = load_index()

def find_wiki_content(df, concept, word_range=(1000, 15000), max_results=2):
    """Find good candidates for wiki content about a concept"""
    print("\n📝 WIKI CONTENT CANDIDATES")
    print("=" * 60)
    
    # Helper function to safely check if a concept is in tags
    def has_concept(tags, concept):
        if isinstance(tags, list):
            return concept in tags
        return False
    
    # Find files with the concept and within word range
    candidates = df[
        df['all_tags'].apply(lambda tags: has_concept(tags, concept)) &
        (df['wordcount'] >= word_range[0]) &
        (df['wordcount'] <= word_range[1])
    ].sort_values('wordcount', ascending=False)
    
    if len(candidates) == 0:
        print(f"No suitable wiki content found for {concept}")
        return
        
    print(f"\nFound {len(candidates)} potential wiki sources for {concept}:")
    for _, row in candidates.head(max_results).iterrows():
        print(f"\n📄 {row['filename']}")
        print(f"   Words: {row['wordcount']:,}")
        if isinstance(row['all_tags'], list):
            print(f"   Tags: {', '.join(row['all_tags'][:5])}")
        if 'first_500_chars' in row:
            print(f"   Preview: {row['first_500_chars'][:100]}...")

def explore_core_triad(df):
    """Explore the three core concepts: pattern recognition, field coherence, and sensory intelligence"""
    
    # Helper function to safely check if a concept is in tags
    def has_concept(tags, concept):
        if isinstance(tags, list):
            return concept in tags
        return False
    
    for concept in ['pattern_recognition', 'field_coherence', 'sensory_intelligence']:
        print(f"\n🎯 {concept.upper()}")
        print("-" * 40)
        
        # Find files with this concept
        concept_files = df[df['all_tags'].apply(lambda tags: has_concept(tags, concept))]
        
        if len(concept_files) == 0:
            print(f"No files found with {concept}")
            continue
            
        # Sort by word count
        concept_files = concept_files.sort_values('wordcount', ascending=False)
        
        # Show top files
        print(f"\nTop files discussing {concept}:")
        for _, row in concept_files.head(3).iterrows():
            print(f"\n📄 {row['filename']}")
            print(f"   Words: {row['wordcount']:,}")
            if isinstance(row['all_tags'], list):
                print(f"   Tags: {', '.join(row['all_tags'][:5])}")
            if 'first_500_chars' in row:
                print(f"   Preview: {row['first_500_chars'][:100]}...")
                
        # Find common co-occurring tags
        all_tags = []
        for tags in concept_files['all_tags']:
            if isinstance(tags, list):
                all_tags.extend(tags)
        
        if all_tags:
            print("\nCommonly co-occurring concepts:")
            for tag, count in Counter(all_tags).most_common(5):
                if tag != concept:
                    print(f"  • {tag}: {count} files")

def find_debugging_examples(df):
    """Find examples of debugging protocols in action"""
    print("\n🔧 DEBUGGING PROTOCOL EXAMPLES")
    print("=" * 60)
    
    # Helper function to safely check if a concept is in tags
    def has_concept(tags, concept):
        if isinstance(tags, list):
            return concept in tags
        return False
    
    debug_concepts = [
        'overwhelm_debugging',
        'decision_paralysis',
        'temporal_misalignment',
        'boundary_confusion',
        'pattern_overload',
        'sync_failure',
        'coherence_breakdown',
        'recursive_loops'
    ]
    
    for concept in debug_concepts:
        print(f"\n🔍 {concept.upper()}")
        print("-" * 40)
        
        # Find files with this concept
        files = df[df['all_tags'].apply(lambda tags: has_concept(tags, concept))]
        
        if len(files) == 0:
            print(f"No examples found for {concept}")
            continue
            
        # Sort by word count and show top examples
        files = files.sort_values('wordcount', ascending=False)
        
        print(f"\nTop examples ({len(files)} total files):")
        for _, row in files.head(3).iterrows():
            print(f"\n📄 {row['filename']}")
            print(f"   Words: {row['wordcount']:,}")
            if isinstance(row['all_tags'], list):
                print(f"   Tags: {', '.join(row['all_tags'][:5])}")
            if 'first_500_chars' in row:
                print(f"   Preview: {row['first_500_chars'][:100]}...")

def find_concept_intersections(df):
    """Find interesting concept intersections"""
    print("\n🔗 CONCEPT INTERSECTIONS")
    print("=" * 60)
    
    # Helper function to safely check if concepts are in tags
    def has_concepts(tags, concept1, concept2):
        if isinstance(tags, list):
            return concept1 in tags and concept2 in tags
        return False
    
    # Interesting concept pairs to explore
    concept_pairs = [
        ('pattern_recognition', 'field_coherence'),
        ('sensory_intelligence', 'boundary_coherence'),
        ('merge_separate', 'timing_misalignment'),
        ('pattern_overload', 'coherence_breakdown'),
        ('recursive_loops', 'boundary_confusion')
    ]
    
    for concept1, concept2 in concept_pairs:
        print(f"\n🔍 {concept1.upper()} + {concept2.upper()}")
        print("-" * 40)
        
        # Find files with both concepts
        intersection_files = df[df['all_tags'].apply(lambda tags: has_concepts(tags, concept1, concept2))]
        
        if len(intersection_files) == 0:
            print(f"No files found combining these concepts")
            continue
            
        # Sort by word count
        intersection_files = intersection_files.sort_values('wordcount', ascending=False)
        
        print(f"\nTop examples ({len(intersection_files)} total files):")
        for _, row in intersection_files.head(3).iterrows():
            print(f"\n📄 {row['filename']}")
            print(f"   Words: {row['wordcount']:,}")
            if isinstance(row['all_tags'], list):
                print(f"   Tags: {', '.join(row['all_tags'][:5])}")
            if 'first_500_chars' in row:
                print(f"   Preview: {row['first_500_chars'][:100]}...")

def extract_definitions(df):
    """Find files that likely contain good definitions"""
    # Look for files with "definition", "what is", "explained", etc. in summary
    definition_keywords = ['definition', 'what is', 'explained', 'means', 'refers to', 'is when']
    
    definition_files = df[
        df['summary'].str.lower().str.contains('|'.join(definition_keywords), na=False) &
        (df['wordcount'] >= 200) &
        (df['wordcount'] <= 5000)
    ]
    
    print(f"\n📚 DEFINITION-RICH FILES")
    print("=" * 60)
    print(f"Found {len(definition_files)} files with definitional content")
    
    for i, (idx, row) in enumerate(definition_files.head(5).iterrows()):
        filename = row['filename'].split('\\')[-1]
        print(f"\n{i+1}. {filename} ({row['wordcount']} words)")
        print(f"   🏷️ Tags: {', '.join(row['all_tags'][:3])}")
        print(f"   📝 {row['summary'][:120]}...")

# Run the analysis
print("🔍 MINING DOS ARCHIVE FOR WIKI CONTENT")
print("=" * 60)

# Explore core concepts
explore_core_triad(df)

# Find debugging examples
find_debugging_examples(df)

# Find concept intersections
find_concept_intersections(df)

# Find definition-rich content
extract_definitions(df)

# Find wiki-ready content for key concepts
print(f"\n" + "="*60)
print("📝 WIKI CONTENT CANDIDATES")
print("="*60)

wiki_concepts = ['merge_separate', 'timing_misalignment', 'pattern_recognition', 'bunny_os']
for concept in wiki_concepts:
    find_wiki_content(df, concept, word_range=(1000, 15000), max_results=2)

print(f"\n🎯 NEXT STEPS:")
print("1. Pick a concept from above")
print("2. Read the best examples") 
print("3. Extract key insights for your wiki pages")
print("4. Use the file paths to access the full content")