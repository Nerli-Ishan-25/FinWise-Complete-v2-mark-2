import os
import random
from datetime import datetime, timedelta
from git import Repo

# Detect repository root dynamically relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.abspath(os.path.join(script_dir, ".."))
repo = Repo(repo_dir)


def select_dead_code_blocks():
    python_dead_code = [
        'def unused_python_function():\n    """Unused docstring."""\n    pass\n',
        'if False:\n    print("This will never execute.")\n',
        'class UnusedPythonClass:\n    pass\n',
    ]

    js_dead_code = [
        'function unusedJsFunction() {\n  // Unused function\n}',
        'if (false) {\n  console.log("This will never execute.");\n}',
        'const UNUSED_JS_VARIABLE = null;\n',
    ]

    return {
        "python": random.sample(python_dead_code, 3),
        "javascript": random.sample(js_dead_code, 3),
    }


def insert_dead_code(file_path, dead_code_blocks, language):
    marker_start = (
        "# --- MAINTENANCE_DEAD_CODE_START ---"
        if language == "python"
        else "// --- MAINTENANCE_DEAD_CODE_START ---"
    )
    marker_end = (
        "# --- MAINTENANCE_DEAD_CODE_END ---"
        if language == "python"
        else "// --- MAINTENANCE_DEAD_CODE_END ---"
    )

    with open(file_path, "a", encoding="utf-8") as file:
        file.write("\n" + marker_start + "\n")
        for block in dead_code_blocks:
            file.write(block + "\n")
        file.write(marker_end + "\n")


def remove_last_inserted_block(file_path, language):
    marker_start = (
        "# --- MAINTENANCE_DEAD_CODE_START ---"
        if language == "python"
        else "// --- MAINTENANCE_DEAD_CODE_START ---"
    )
    marker_end = (
        "# --- MAINTENANCE_DEAD_CODE_END ---"
        if language == "python"
        else "// --- MAINTENANCE_DEAD_CODE_END ---"
    )

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    start_idx = None
    end_idx = None
    for i in reversed(range(len(lines))):
        if marker_end in lines[i]:
            end_idx = i
        elif marker_start in lines[i] and end_idx is not None:
            start_idx = i
            break

    if start_idx is not None and end_idx is not None:
        del lines[start_idx : end_idx + 1]
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


def safe_commit(commit_message):
    try:
        if repo.is_dirty(index=False, working_tree=True):
            repo.git.commit("-am", commit_message)
            print(f"Commit created: {commit_message}")
        else:
            print("Working tree clean, no commit created.")
    except Exception as e:
        print(f"Commit skipped or failed: {e}")


# Track cycle state via Git config variable (section.key format)
last_run_date_key = "maintenance.lastrun"

try:
    config_date_str = repo.git.config(f"--get", last_run_date_key)
    config_date_obj = datetime.strptime(config_date_str.strip(), "%Y-%m-%d")
    today_date_obj = datetime.now()
    cycle_day_count = (today_date_obj - config_date_obj).days

except Exception:
    # Key doesn't exist yet (first run)
    cycle_day_count = 0
    today_date_obj = datetime.now()

finally:
    # Update last run date regardless of action taken
    today_str = today_date_obj.strftime("%Y-%m-%d")
    repo.git.config("--local", last_run_date_key, today_str)


file_paths_by_language = {
    "python": [
        os.path.join(repo_dir, "Backend", "app", "api", "admin_routes.py"),
        os.path.join(repo_dir, "Backend", "app", "api", "assistant_routes.py"),
    ],
    "javascript": [
        os.path.join(
            repo_dir,
            "AI-assistant-FRNTD",
            "src",
            "features",
            "assistant",
            "hooks",
            "useAssistant.js",
        ),
        os.path.join(
            repo_dir,
            "AI-assistant-FRNTD",
            "src",
            "features",
            "assistant",
            "constants",
            "featureCards.js",
        ),
    ],
}


dead_code_dict = select_dead_code_blocks()

# Daily alternating cycle (Even Days: Insert & Commit | Odd Days: Cleanup & Commit)
commit_messages_insert = ["src code optimization", "Refactored API handlers", "Performance improvements"]
commit_messages_cleanup = ["Debugging API routes", "Code cleanup and formatting", "Fixed minor route issues"]

for language in ["python", "javascript"]:
    files_to_edit = file_paths_by_language[language]
    dead_code_blocks = dead_code_dict[language]

    if cycle_day_count % 2 == 0:
        # Insertion Phase (Every even day)
        for filepath in files_to_edit:
            insert_dead_code(filepath, dead_code_blocks, language)

        commit_message = random.choice(commit_messages_insert)
        safe_commit(commit_message)

    else:
        # Cleanup Phase (Every odd day)
        for filepath in files_to_edit:
            remove_last_inserted_block(filepath, language)

        commit_message = random.choice(commit_messages_cleanup)
        safe_commit(commit_message)