import json

# Load the Gentle JSON output
with open('aligned.json', 'r') as f:
    alignment = json.load(f)

# Parse the alignment data
ctm_lines = []
for word_info in alignment['words']:
    if 'start' in word_info and 'end' in word_info:
        start_time = word_info['start']
        duration = word_info['end'] - word_info['start']
        word = word_info['word']
        ctm_line = f"test_pcm 1 {start_time:.2f} {duration:.2f} {word} NA lex speaker_id"
        ctm_lines.append(ctm_line)

# Save to CTM file
with open('align.ctm', 'w') as f:
    f.write('\n'.join(ctm_lines))
