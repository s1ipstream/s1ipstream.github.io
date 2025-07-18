// Knowledge Base Analyzer for n8n
module.exports = {
    async extractContentByTag(items, tag) {
        const fs = require('fs');
        const path = require('path');
        
        // Load the archive index
        const archiveData = [];
        const indexFile = path.join(__dirname, 'archive_index.jsonl');
        const lines = fs.readFileSync(indexFile, 'utf8').split('\n');
        lines.forEach(line => {
            if (line.trim()) {
                archiveData.push(JSON.parse(line));
            }
        });

        // Filter content by tag
        const relevantContent = archiveData.filter(entry => 
            entry.all_tags && entry.all_tags.includes(tag)
        );

        // Format content for webpage insertion
        const formattedContent = relevantContent.map(entry => ({
            filename: entry.filename,
            content: entry.content,
            summary: entry.summary,
            tags: entry.all_tags,
            wordcount: entry.wordcount
        }));

        return {
            tag,
            matches: formattedContent.length,
            content: formattedContent
        };
    },

    async generateRelatedConcepts(items, primaryTag) {
        const fs = require('fs');
        const path = require('path');
        
        // Load schema to get all possible tags
        const schema = JSON.parse(fs.readFileSync(path.join(__dirname, 'schema.yaml'), 'utf8'));
        const allTags = [
            ...schema.core_themes,
            ...schema.pattern_operators,
            ...schema.debugging_protocols,
            ...schema.applications
        ];

        // Load archive index
        const archiveData = [];
        const indexFile = path.join(__dirname, 'archive_index.jsonl');
        const lines = fs.readFileSync(indexFile, 'utf8').split('\n');
        lines.forEach(line => {
            if (line.trim()) {
                archiveData.push(JSON.parse(line));
            }
        });

        // Find co-occurring tags
        const coOccurringTags = new Map();
        archiveData.forEach(entry => {
            if (entry.all_tags && entry.all_tags.includes(primaryTag)) {
                entry.all_tags.forEach(tag => {
                    if (tag !== primaryTag) {
                        coOccurringTags.set(tag, (coOccurringTags.get(tag) || 0) + 1);
                    }
                });
            }
        });

        // Sort by frequency
        const relatedConcepts = Array.from(coOccurringTags.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([tag, count]) => ({
                tag,
                count,
                category: Object.keys(schema).find(cat => 
                    schema[cat].includes(tag)
                )
            }));

        return {
            primaryTag,
            relatedConcepts
        };
    }
}; 