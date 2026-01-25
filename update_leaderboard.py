import json
import sys
import os

# 1. Get data from the GitHub Action payload
data = json.loads(os.getenv('STUDENT_DATA'))
student_name = data['student']
new_score = float(data['score'])

leaderboard_file = 'README.md'

# 2. Read existing content
with open(leaderboard_file, 'r') as f:
    lines = f.readlines()

# 3. Simple Logic: Parse the table and update or add the student
scores = {}
header = "# 🏆 Class Leaderboard\n\n| Rank | Student | Score |\n| :--- | :--- | :--- |\n"

# Assume table starts after line 3
for line in lines[3:]:
    if '|' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            scores[parts[2]] = float(parts[3])

# Update with the new score
scores[student_name] = new_score

# 4. Sort and rewrite
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

with open(leaderboard_file, 'w') as f:
    f.write(header)
    for i, (name, score) in enumerate(sorted_scores, 1):
        f.write(f"| {i} | {name} | {score} |\n")
