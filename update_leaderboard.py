import os
import json
import datetime

# Configuration
SCORES_FILE = "scores.json"
README_FILE = "README.md"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def update_readme(scores):
    # Sort scores: Highest score first. 
    # If scores match, most recent timestamp (last updated) is secondary sort? 
    # Usually we just sort by score descending.
    sorted_students = sorted(scores.items(), key=lambda item: float(item[1]['score']), reverse=True)
    
    markdown_content = "# 🏆 MEE450 Project : Single Discrete Agent Leaderboard\n\n"
    markdown_content += "| Rank | Student | Score | Last Updated |\n"
    markdown_content += "| :--- | :--- | :--- | :--- |\n"
    
    rank = 1
    for student, data in sorted_students:
        score = f"{float(data['score']):.2f}"
        timestamp = data.get('timestamp', 'N/A')
        markdown_content += f"| {rank} | **{student}** | {score} | {timestamp} |\n"
        rank += 1
        
    markdown_content += "\n\n*Updated automatically by GitHub Actions.*"
    
    with open(README_FILE, 'w') as f:
        f.write(markdown_content)

def main():
    # 1. Get Payload from Environment Variable
    payload_str = os.environ.get('PAYLOAD_JSON')
    if not payload_str:
        print("Error: No PAYLOAD_JSON environment variable found.")
        exit(1)
        
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

    username = payload.get('username') or payload.get('student') # Handle both naming conventions
    score = payload.get('score')

    if not username or score is None:
        print(f"Error: Invalid payload data. Username: {username}, Score: {score}")
        exit(1)

    print(f"Processing score for {username}: {score}")

    # 2. Update Data
    scores = load_scores()
    
    # Update logic: Always overwrite with latest, or only if higher?
    # Usually for a test leaderboard, we overwrite so students can see regressions.
    scores[username] = {
        "score": score,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 3. Save and Regenerate
    save_scores(scores)
    update_readme(scores)
    print("Leaderboard updated successfully.")

if __name__ == "__main__":
    main()
