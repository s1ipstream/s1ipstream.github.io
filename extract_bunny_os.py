import pandas as pd
import json
from pathlib import Path

def has_tag(tags, tag):
    """Helper function to safely check if a tag exists"""
    if isinstance(tags, list):
        return tag in tags
    return False

# Load the index
print("🐰 Loading BunnyOS content...")
df = pd.read_json('archive_index.jsonl', lines=True)

# Find files tagged with bunny_os
bunny_files = df[df['all_tags'].apply(lambda tags: has_tag(tags, 'bunny_os'))]

if len(bunny_files) == 0:
    print("No files found with bunny_os tag")
    exit()

print(f"\n📚 Found {len(bunny_files)} files about BunnyOS:")
for _, row in bunny_files.iterrows():
    print(f"\n📄 {row['filename']}")
    print(f"   Words: {row['wordcount']:,}")
    if isinstance(row['all_tags'], list):
        print(f"   Tags: {', '.join(row['all_tags'][:5])}")
    if 'first_500_chars' in row:
        print(f"   Preview: {row['first_500_chars'][:100]}...")