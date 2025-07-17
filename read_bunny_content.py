from pathlib import Path

def read_and_format_content(filepath):
    """Read content and prepare for wiki formatting"""
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')
        
        print(f"📄 CONTENT FROM: {filepath}")
        print("=" * 60)
        print(f"📊 Length: {len(content)} characters")
        print(f"📝 Word count: {len(content.split())}")
        print("\n📖 FULL CONTENT:")
        print("-" * 60)
        print(content)
        print("-" * 60)
        
        return content
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

# Main Bunny OS file
main_file = r".\source_materials\converted_txt\google_drive\Decisions\ChatGPT\Bunny OS.txt"
print("🐰 EXTRACTING MAIN BUNNY OS CONTENT")
main_content = read_and_format_content(main_file)

print("\n" + "="*60)
print("🎯 WIKI PAGE STRUCTURE SUGGESTIONS")
print("="*60)

if main_content:
    # Analyze the content structure
    lines = main_content.split('\n')
    potential_headers = [line for line in lines if line.strip() and (
        line.startswith('#') or 
        line.isupper() or 
        len(line.split()) < 8 and line.strip().endswith(':')
    )]
    
    print("\n📋 Potential section headers found:")
    for header in potential_headers[:10]:  # Show first 10
        print(f"   • {header.strip()}")
    
    # Look for key concepts
    key_terms = ['PDA', 'neurodivergent', 'pattern', 'overwhelm', 'boundary', 'timing', 'debug']
    found_terms = []
    content_lower = main_content.lower()
    
    for term in key_terms:
        if term.lower() in content_lower:
            found_terms.append(term)
    
    print(f"\n🔍 Key DOS concepts found: {', '.join(found_terms)}")

print(f"\n🛠️ NEXT STEPS:")
print(f"1. Review the content above")
print(f"2. Identify the main sections/concepts")  
print(f"3. I'll help you structure it into a proper wiki page")
print(f"4. We'll create the HTML file for your DOS debugging manual")