const fs = require('fs');
const path = require('path');

// Define pages to process
const pages = [
    {
        name: 'merge-separate',
        tag: 'merge_separate',
        path: 'concepts/merge-separate.html'
    },
    {
        name: '123-cycle',
        tag: 'tension_release_distribution',
        path: 'concepts/123-cycle.html'
    },
    {
        name: 'identity-equation',
        tag: 'identity_knot',
        path: 'concepts/identity-equation.html'
    },
    {
        name: 'beyond-pathology',
        tag: 'neurodivergent_frameworks',
        path: 'beyond-pathology/index.html'
    }
];

// Load and parse archive index
console.log('Loading archive index...');
const archiveData = fs.readFileSync('archive_index.jsonl', 'utf8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line));

console.log(`Loaded ${archiveData.length} entries from archive`);

// Process each page
for (const page of pages) {
    console.log(`\nProcessing ${page.name}...`);
    
    // Filter content by tag
    console.log(`Finding content with tag: ${page.tag}`);
    const content = archiveData.filter(entry => 
        entry.all_tags && entry.all_tags.includes(page.tag)
    );
    
    // Find related concepts
    console.log('Finding related concepts...');
    const coOccurringTags = new Map();
    archiveData.forEach(entry => {
        if (entry.all_tags && entry.all_tags.includes(page.tag)) {
            entry.all_tags.forEach(tag => {
                if (tag !== page.tag) {
                    coOccurringTags.set(tag, (coOccurringTags.get(tag) || 0) + 1);
                }
            });
        }
    });

    const related = Array.from(coOccurringTags.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([tag, count]) => ({
            tag,
            count
        }));

    // Format content
    console.log('Formatting content...');
    const formattedContent = content.map(item => `
        <section class="content-section">
            <h3>${item.filename}</h3>
            <div class="summary">${item.summary}</div>
            <div class="tags">${item.all_tags.join(', ')}</div>
            <div class="content">${item.content}</div>
        </section>
    `).join('\n');

    const formattedRelated = related.map(concept => `
        <li class="related-concept">
            <a href="/concepts/${concept.tag}.html">${concept.tag.replace('_', ' ')}</a>
            <span class="count">(${concept.count} connections)</span>
        </li>
    `).join('\n');

    // Update HTML file
    console.log(`Updating ${page.path}...`);
    let html = fs.readFileSync(page.path, 'utf8');
    html = html.replace('<!-- CONTENT -->', formattedContent);
    html = html.replace('<!-- RELATED_CONCEPTS -->', formattedRelated);
    fs.writeFileSync(page.path, html);

    console.log(`✓ Updated ${page.path} with ${content.length} content sections and ${related.length} related concepts`);
}

console.log('\nContent population complete!') 