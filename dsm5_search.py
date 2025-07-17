import json
import pandas as pd
import re

# Load the archive
def load_index(filename="archive_index.jsonl"):
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

df = load_index()

def search_dsm_content(df):
    """Search for DSM-5 and related psychiatric content"""
    
    # Keywords related to DSM-5 and psychiatric categorization
    dsm_keywords = [
        'dsm', 'dsm-5', 'dsm5', 'diagnostic', 'patholog', 'psychiatric', 
        'mental health', 'disorder', 'diagnosis', 'clinical', 'therapy',
        'therapist', 'psychiatrist', 'medication', 'treatment'
    ]
    
    # Neurodivergent/alternative framework keywords
    neuro_keywords = [
        'neurodivergent', 'neurodiversity', 'autism', 'adhd', 'pda',
        'pathological demand avoidance', 'stimming', 'masking', 'meltdown',
        'sensory processing', 'executive function'
    ]
    
    all_keywords = dsm_keywords + neuro_keywords
    
    # Search in summaries and content
    pattern = '|'.join([kw.lower() for kw in all_keywords])
    
    # Find files that mention these terms
    dsm_mask = (
        df['summary'].str.lower().str.contains(pattern, na=False, regex=True) |
        df['first_500_chars'].str.lower().str.contains(pattern, na=False, regex=True) |
        df['last_500_chars'].str.lower().str.contains(pattern, na=False, regex=True)
    )
    
    dsm_files = df[dsm_mask].copy()
    
    # Score by relevance (how many keywords appear)
    def count_keywords(text):
        if pd.isna(text):
            return 0
        text_lower = text.lower()
        return sum(1 for kw in all_keywords if kw.lower() in text_lower)
    
    dsm_files['keyword_count'] = dsm_files['summary'].apply(count_keywords)
    dsm_files = dsm_files.sort_values(['keyword_count', 'wordcount'], ascending=[False, False])
    
    return dsm_files, all_keywords

def analyze_dsm_content(dsm_files, keywords):
    """Analyze the DSM-related content"""
    
    print("🧠 DSM-5 & PSYCHIATRIC CONTENT ANALYSIS")
    print("=" * 60)
    print(f"Found {len(dsm_files)} files with psychiatric/neurodivergent content")
    
    if len(dsm_files) == 0:
        print("No files found with DSM-5 related keywords")
        return
    
    # Show stats
    total_words = dsm_files['wordcount'].sum()
    print(f"Total words in psychiatric content: {total_words:,}")
    print(f"Average relevance score: {dsm_files['keyword_count'].mean():.1f}")
    
    print(f"\n📊 TOP 10 MOST RELEVANT FILES:")
    print("-" * 60)
    
    for i, (idx, row) in enumerate(dsm_files.head(10).iterrows()):
        filename = row['filename'].split('\\')[-1]
        print(f"\n{i+1}. {filename}")
        print(f"   📊 {row['wordcount']:,} words | Relevance: {row['keyword_count']} keywords")
        print(f"   🏷️ Tags: {', '.join(row['all_tags'][:4])}")
        print(f"   📝 Preview: {row['summary'][:120]}...")
        
        # Show which keywords appear in this file
        keywords_found = []
        text_lower = (str(row['summary']) + " " + str(row['first_500_chars'])).lower()
        for kw in keywords:
            if kw.lower() in text_lower:
                keywords_found.append(kw)
        
        if keywords_found:
            print(f"   🔍 Keywords found: {', '.join(keywords_found[:5])}")
    
    # Look for specific high-value content
    print(f"\n🎯 SPECIFIC DSM-5 MENTIONS:")
    print("-" * 60)
    
    specific_dsm = dsm_files[
        dsm_files['summary'].str.lower().str.contains('dsm', na=False) |
        dsm_files['first_500_chars'].str.lower().str.contains('dsm', na=False)
    ]
    
    if len(specific_dsm) > 0:
        for i, (idx, row) in enumerate(specific_dsm.head(5).iterrows()):
            filename = row['filename'].split('\\')[-1]
            print(f"\n{i+1}. {filename} ({row['wordcount']:,} words)")
            print(f"   Preview: {row['summary'][:150]}...")
    else:
        print("No explicit DSM-5 mentions found")
    
    # Look for framework critiques
    print(f"\n🔍 FRAMEWORK VS TRADITIONAL APPROACHES:")
    print("-" * 60)
    
    critique_files = dsm_files[
        (dsm_files['keyword_count'] >= 3) &  # Multiple relevant keywords
        (dsm_files['wordcount'] >= 1000) &   # Substantial content
        (dsm_files['wordcount'] <= 50000)    # Not massive compilation files
    ]
    
    for i, (idx, row) in enumerate(critique_files.head(5).iterrows()):
        filename = row['filename'].split('\\')[-1]
        print(f"\n{i+1}. {filename}")
        print(f"   📊 {row['wordcount']:,} words | {len(row['all_tags'])} DOS tags")
        print(f"   🏷️ Framework tags: {', '.join(row['all_tags'][:3])}")
        print(f"   📝 {row['summary'][:120]}...")
        print(f"   📂 Path: {row['filename']}")

# Run the analysis
df = load_index()
dsm_files, keywords = search_dsm_content(df)
analyze_dsm_content(dsm_files, keywords)

print(f"\n🎯 NEXT STEPS:")
print(f"1. Review the most relevant files above")
print(f"2. Look for critiques of pathologizing approaches")
print(f"3. Find your alternative framework explanations")
print(f"4. Extract content for potential wiki pages on:")
print(f"   • 'Beyond Pathology: Pattern-Based Understanding'")
print(f"   • 'Neurodivergence as Specialized Configuration'") 
print(f"   • 'I=C/M vs DSM-5 Categorization'")
print(f"   • 'From Diagnosis to Debugging'")