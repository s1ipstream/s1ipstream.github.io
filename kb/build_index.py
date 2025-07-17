import os
import json
import yaml
from glob import glob
from pathlib import Path
import re

def load_schema():
    """Load the pattern schema"""
    try:
        with open("schema.yaml", "r") as f:
            schema = yaml.safe_load(f)
            print("✓ Schema loaded successfully")
            return schema
    except FileNotFoundError:
        print("❌ ERROR: schema.yaml not found in current directory")
        print("Current directory:", os.getcwd())
        print("Files in current directory:", os.listdir("."))
        return None
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Invalid YAML in schema.yaml: {e}")
        return None

def clean_text(text):
    """Clean text for processing"""
    # Just remove excessive whitespace but preserve newlines
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def auto_tag(text, tag_list):
    """Auto-tag content based on keyword matching"""
    tags = []
    lower_text = text.lower()
    
    for tag in tag_list:
        # Check for exact tag match (with underscores as spaces)
        tag_phrase = tag.replace("_", " ")
        if tag_phrase in lower_text:
            tags.append(tag)
            continue
            
        # Check for individual words in the tag
        tag_words = tag.split("_")
        if len(tag_words) > 1:
            # If all words in the tag appear in text
            if all(word in lower_text for word in tag_words):
                tags.append(tag)
    
    return tags

def simple_summarize(text, max_length=200):
    """Simple extractive summarization - take first few sentences"""
    sentences = text.split('. ')
    summary = ""
    for sentence in sentences:
        if len(summary + sentence) < max_length:
            summary += sentence + ". "
        else:
            break
    return summary.strip()

def process_file(filepath, schema):
    """Process a single file and extract metadata"""
    try:
        print(f"Processing {filepath}...")
        # Try different encodings
        content = ""
        encoding_tried = []
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                print(f"  Trying {encoding} encoding...")
                content = Path(filepath).read_text(encoding=encoding)
                print(f"  Successfully read with {encoding}")
                break
            except UnicodeDecodeError:
                encoding_tried.append(encoding)
                print(f"  Failed with {encoding}")
                continue
        
        if not content:
            return {"file": filepath, "reason": f"encoding failed with: {', '.join(encoding_tried)}"}
            
        # Clean content
        print(f"  Content length before cleaning: {len(content)}")
        content = clean_text(content)
        print(f"  Content length after cleaning: {len(content)}")
        
        # Skip if too short
        if len(content) < 50:
            return {"file": filepath, "reason": f"content too short ({len(content)} chars)"}
            
        # Extract metadata
        first_500 = content[:500]
        last_500 = content[-500:] if len(content) > 500 else content
        summary = simple_summarize(content)
        
        # Auto-tag
        all_tags = (schema.get("core_themes", []) + 
                   schema.get("pattern_operators", []) + 
                   schema.get("debugging_protocols", []) + 
                   schema.get("applications", []))
        
        detected_tags = auto_tag(content, all_tags)
        
        # Categorize tags
        theme_tags = auto_tag(content, schema.get("core_themes", []))
        pattern_tags = auto_tag(content, schema.get("pattern_operators", []))
        debug_tags = auto_tag(content, schema.get("debugging_protocols", []))
        app_tags = auto_tag(content, schema.get("applications", []))
        
        entry = {
            "filename": str(filepath),
            "wordcount": len(content.split()),
            "char_count": len(content),
            "first_500_chars": first_500,
            "last_500_chars": last_500,
            "summary": summary,
            "theme_tags": theme_tags,
            "pattern_tags": pattern_tags,
            "debug_tags": debug_tags,
            "app_tags": app_tags,
            "all_tags": detected_tags
        }
        
        return entry
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def build_index(root_dir=".", output_file="archive_index.jsonl"):
    """Build the complete file index"""
    
    print("🚀 Starting DOS Archive Indexing...")
    print(f"Working directory: {os.getcwd()}")
    
    # Create skipped files log
    skipped_log = []
    
    # Load schema
    schema = load_schema()
    if not schema:
        print("❌ Cannot proceed without schema.yaml")
        return None
    
    print(f"📋 Schema loaded:")
    print(f"  • Themes: {len(schema.get('core_themes', []))}")
    print(f"  • Patterns: {len(schema.get('pattern_operators', []))}")
    print(f"  • Debug protocols: {len(schema.get('debugging_protocols', []))}")
    print(f"  • Applications: {len(schema.get('applications', []))}")
    
    # Find all text files
    file_patterns = ["**/*.txt", "**/*.md", "**/*.docx", "**/*.doc"]
    all_files = []
    
    print(f"\n🔍 Searching for files in: {root_dir}")
    for pattern in file_patterns:
        files = glob(os.path.join(root_dir, pattern), recursive=True)
        all_files.extend(files)
        print(f"  • Found {len(files)} {pattern} files")
    
    print(f"\n📁 Total files found: {len(all_files)}")
    
    if len(all_files) == 0:
        print("❌ No files found to process!")
        print("Make sure your files are in the correct directory.")
        return None
    
    # Process files
    index = []
    processed = 0
    skipped = 0
    
    print(f"\n⚙️ Processing files...")
    for filepath in all_files:
        print(f"\nAttempting to process: {filepath}")
        # Skip hidden files and system files
        if "/.git/" in filepath or os.path.basename(filepath).startswith('.'):
            skipped_log.append({"file": filepath, "reason": "hidden/system file"})
            print(f"Skipping hidden/system file: {filepath}")
            skipped += 1
            continue
            
        entry = process_file(filepath, schema)
        if entry:
            print(f"Successfully processed: {filepath}")  # Debug
            index.append(entry)
            processed += 1
        else:
            skipped_log.append({"file": filepath, "reason": "processing failed"})
            print(f"Failed to process: {filepath}")  # Debug
            skipped += 1
            
        if processed % 100 == 0 and processed > 0:
            print(f"  ✓ Processed {processed} files...")
    
    # Write skipped files log
    with open("skipped_files.json", "w") as f:
        json.dump(skipped_log, f, indent=2)
    print(f"  📝 Skipped files log saved to: skipped_files.json")
    
    if len(index) == 0:
        print("❌ No files were successfully processed!")
        return None
    
    # Write index
    print(f"\n💾 Saving index to {output_file}...")
    with open(output_file, "w") as f:
        for entry in index:
            f.write(json.dumps(entry) + "\n")
    
    print(f"\n🎉 Index complete!")
    print(f"  ✓ Successfully processed: {len(index)} files")
    print(f"  ⚠️ Skipped: {skipped} files")
    print(f"  📄 Output saved to: {output_file}")
    
    # Quick stats
    total_tags = sum(len(entry["all_tags"]) for entry in index)
    total_words = sum(entry["wordcount"] for entry in index)
    print(f"  🏷️ Total tags detected: {total_tags}")
    print(f"  📝 Total words indexed: {total_words:,}")
    
    return index

if __name__ == "__main__":
    # Set the root directory where your files are
    # Change this to the path containing your 7000 files
    ROOT_DIR = "."  # Current directory - change if your files are elsewhere
    
    print("DOS Archive Indexer")
    print("=" * 50)
    
    index = build_index(ROOT_DIR)
    
    if index:
        print("\n✅ Indexing completed successfully!")
        print("You can now run the explorer script to search your files.")
    else:
        print("\n❌ Indexing failed. Please check the errors above.")