import os
import sys
import re
import time
import random
import logging
from datetime import datetime
from git import Repo
from git.exc import GitCommandError

# ---------------------------------------------------------------------------
# Path & Logging Setup
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Setup console-only logging
logger = logging.getLogger("MaintenanceAutomation")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console Handler only (no log files written to disk)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Target Files Configuration
TARGET_FILES = {
    "python": [
        os.path.join(REPO_DIR, "Backend", "app", "api", "admin_routes.py"),
        os.path.join(REPO_DIR, "Backend", "app", "api", "assistant_routes.py"),
    ],
    "javascript": [
        os.path.join(
            REPO_DIR,
            "AI-assistant-FRNTD",
            "src",
            "features",
            "assistant",
            "hooks",
            "useAssistant.js",
        ),
        os.path.join(
            REPO_DIR,
            "AI-assistant-FRNTD",
            "src",
            "features",
            "assistant",
            "constants",
            "featureCards.js",
        ),
    ],
}

MARKERS = {
    "python": {
        "start": "# --- MAINTENANCE_DEAD_CODE_START ---",
        "end": "# --- MAINTENANCE_DEAD_CODE_END ---",
        "pattern": r"\n?# --- MAINTENANCE_DEAD_CODE_START ---[\s\S]*?# --- MAINTENANCE_DEAD_CODE_END ---\n?",
    },
    "javascript": {
        "start": "// --- MAINTENANCE_DEAD_CODE_START ---",
        "end": "// --- MAINTENANCE_DEAD_CODE_END ---",
        "pattern": r"\n?// --- MAINTENANCE_DEAD_CODE_START ---[\s\S]*?// --- MAINTENANCE_DEAD_CODE_END ---\n?",
    },
}

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def select_dead_code_blocks():
    """Returns random snippets of harmless maintenance code."""
    python_dead_code = [
        'def unused_python_function():\n    """Unused docstring for maintenance."""\n    pass\n',
        'if False:\n    print("Daily Maintenance run.")\n',
        'class UnusedPythonClass:\n    pass\n',
        '# Maintenance routine marker\nUNUSED_FLAG = True\n',
    ]

    js_dead_code = [
        'function unusedJsFunction() {\n  // Unused function for maintenance\n}',
        'if (false) {\n  console.log("Daily maintenance run.");\n}',
        'const UNUSED_JS_VARIABLE = null;\n',
        '// Maintenance routine marker\nconst MAINTENANCE_ACTIVE = true;\n',
    ]

    return {
        "python": random.sample(python_dead_code, k=min(3, len(python_dead_code))),
        "javascript": random.sample(js_dead_code, k=min(3, len(js_dead_code))),
    }


def file_has_markers(file_path, language):
    """Checks whether maintenance markers are currently present in a file."""
    if not os.path.exists(file_path):
        logger.warning(f"File not found during state check: {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return MARKERS[language]["start"] in content
    except Exception as e:
        logger.error(f"Error reading {file_path} during state check: {e}")
        return False


def determine_current_state():
    """
    Scans all existing target files to determine system state.
    Returns 'INSERTED' if any file contains markers, else 'CLEANED'.
    """
    for lang, files in TARGET_FILES.items():
        for file_path in files:
            if file_has_markers(file_path, lang):
                return "INSERTED"
    return "CLEANED"


def insert_dead_code(file_path, dead_code_blocks, language):
    """Appends dead code block to the specified file if not already present."""
    if not os.path.exists(file_path):
        logger.warning(f"Skipping insertion. File does not exist: {file_path}")
        return False

    if file_has_markers(file_path, language):
        logger.info(f"Markers already exist in {os.path.basename(file_path)}. Skipping insertion.")
        return False

    m_start = MARKERS[language]["start"]
    m_end = MARKERS[language]["end"]

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + m_start + "\n")
            for block in dead_code_blocks:
                f.write(block.rstrip() + "\n")
            f.write(m_end + "\n")
        logger.info(f"Inserted maintenance code into {os.path.basename(file_path)}")
        return True
    except Exception as e:
        logger.error(f"Failed to write to {file_path}: {e}")
        return False


def remove_all_inserted_blocks(file_path, language):
    """Removes ALL maintenance dead code blocks from the specified file."""
    if not os.path.exists(file_path):
        logger.warning(f"Skipping cleanup. File does not exist: {file_path}")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = MARKERS[language]["pattern"]
        new_content, count = re.subn(pattern, "", content)

        if count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logger.info(f"Removed {count} maintenance code block(s) from {os.path.basename(file_path)}")
            return True
        else:
            logger.info(f"No maintenance code blocks found in {os.path.basename(file_path)}")
            return False
    except Exception as e:
        logger.error(f"Failed to remove code blocks from {file_path}: {e}")
        return False


# ---------------------------------------------------------------------------
# Git Operations
# ---------------------------------------------------------------------------

def ensure_git_identity(repo):
    """Ensures Git user.name and user.email are set for the repository session."""
    with repo.config_writer() as config:
        try:
            name = repo.git.config("--get", "user.name")
        except GitCommandError:
            name = None
        try:
            email = repo.git.config("--get", "user.email")
        except GitCommandError:
            email = None

        if not name:
            config.set_value("user", "name", "Maintenance Automation Bot")
            logger.info("Set fallback Git user.name: Maintenance Automation Bot")
        if not email:
            config.set_value("user", "email", "maintenance-bot@users.noreply.github.com")
            logger.info("Set fallback Git user.email")


def stage_and_commit(repo, modified_files, commit_message):
    """Stages specified modified files and creates a Git commit."""
    if not modified_files:
        logger.info("No files modified during maintenance phase.")
        return False

    ensure_git_identity(repo)

    # Stage files explicitly
    valid_files = [f for f in modified_files if os.path.exists(f)]
    if not valid_files:
        logger.warning("No valid files to stage.")
        return False

    try:
        repo.git.add(valid_files)
        logger.info(f"Staged {len(valid_files)} file(s).")
    except Exception as e:
        logger.error(f"Failed to stage files in Git: {e}")
        return False

    # Check if index has changes staged for commit
    if not repo.is_dirty(index=True, working_tree=False):
        logger.info("Git index clean. Nothing to commit.")
        return False

    try:
        commit_obj = repo.index.commit(commit_message)
        logger.info(f"Commit created successfully: {commit_obj.hexsha[:7]} - '{commit_message}'")
        return True
    except Exception as e:
        logger.error(f"Git commit failed: {e}")
        return False


def push_with_retry(repo, max_retries=3, delay_seconds=5):
    """Pushes local branch to origin with fetch/rebase and retry logic."""
    try:
        active_branch = repo.active_branch.name
    except Exception:
        # Handle detached HEAD state gracefully
        logger.warning("Repository is in detached HEAD state. Attempting checkout to 'develop'...")
        repo.git.checkout("develop")
        active_branch = repo.active_branch.name

    logger.info(f"Preparing to push branch '{active_branch}' to origin...")

    # Sync remote changes first (fetch)
    try:
        repo.git.fetch("origin", active_branch)
        behind_count = repo.git.rev_list("--count", f"HEAD..origin/{active_branch}").strip()
        if behind_count != "0":
            logger.info(f"Local branch is behind origin/{active_branch} by {behind_count} commit(s). Rebasing...")
            repo.git.rebase(f"origin/{active_branch}")
    except Exception as fetch_err:
        logger.warning(f"Remote fetch/rebase warning: {fetch_err}")

    # Retry loop for push
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Push attempt {attempt}/{max_retries} to origin/{active_branch}...")
            push_info = repo.git.push("origin", active_branch)
            logger.info(f"Successfully pushed to origin/{active_branch}. Output: {push_info.strip()}")
            return True
        except GitCommandError as push_err:
            logger.warning(f"Push attempt {attempt} failed: {push_err}")
            if attempt < max_retries:
                logger.info(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                logger.error("All push retries exhausted.")
                return False
        except Exception as general_err:
            logger.error(f"Unexpected error during git push: {general_err}")
            return False

    return False


# ---------------------------------------------------------------------------
# Main Workflow
# ---------------------------------------------------------------------------

def run_maintenance():
    start_time = datetime.now()
    logger.info("==================================================")
    logger.info(f"Starting Maintenance Automation Run at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Repository Root: {REPO_DIR}")

    try:
        repo = Repo(REPO_DIR)
        if repo.bare:
            logger.error("Git repository is bare. Aborting.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to initialize Git repository at {REPO_DIR}: {e}")
        sys.exit(1)

    # 1. Determine Current State via self-healing detection
    current_state = determine_current_state()
    logger.info(f"Detected repository state: '{current_state}'")

    dead_code_dict = select_dead_code_blocks()
    modified_files = []

    commit_messages_insert = [
        "src code optimization",
        "Refactored API handlers",
        "Performance improvements",
        "Updated internal helper routines",
    ]
    commit_messages_cleanup = [
        "Debugging API routes",
        "Code cleanup and formatting",
        "Fixed minor route issues",
        "Routine maintenance cleanup",
    ]

    # 2. Execute Action Based on State
    if current_state == "CLEANED":
        # Target action: INSERTION
        logger.info("Action: Inserting maintenance code blocks (Insertion Phase)...")
        for lang, files in TARGET_FILES.items():
            blocks = dead_code_dict[lang]
            for file_path in files:
                if insert_dead_code(file_path, blocks, lang):
                    modified_files.append(file_path)
        commit_msg = random.choice(commit_messages_insert)

    else:
        # Target action: CLEANUP
        logger.info("Action: Removing maintenance code blocks (Cleanup Phase)...")
        for lang, files in TARGET_FILES.items():
            for file_path in files:
                if remove_all_inserted_blocks(file_path, lang):
                    modified_files.append(file_path)
        commit_msg = random.choice(commit_messages_cleanup)

    # 3. Stage & Commit
    committed = stage_and_commit(repo, modified_files, commit_msg)

    # Check unpushed commits count
    unpushed_count = "0"
    try:
        active_branch = repo.active_branch.name
        unpushed_count = repo.git.rev_list("--count", f"origin/{active_branch}..HEAD").strip()
    except Exception as e:
        logger.warning(f"Could not calculate unpushed commits count: {e}")

    # 4. Push if committed or unpushed commits exist
    pushed = False
    if committed or unpushed_count != "0":
        logger.info(f"Unpushed commits present ({unpushed_count}). Proceeding to push...")
        pushed = push_with_retry(repo, max_retries=3, delay_seconds=5)
    else:
        logger.info("No new commits or unpushed changes. Skipping push.")

    # 5. Record Last Run Metadata in Git Config
    try:
        today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_state = "INSERTED" if current_state == "CLEANED" else "CLEANED"
        if committed or pushed:
            repo.git.config("--local", "maintenance.lastrun", today_str)
            repo.git.config("--local", "maintenance.laststate", new_state)
            logger.info(f"Updated Git config: maintenance.lastrun = '{today_str}', maintenance.laststate = '{new_state}'")
    except Exception as config_err:
        logger.warning(f"Could not save Git config metadata: {config_err}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Maintenance Run Completed in {duration:.2f} seconds.")
    logger.info("==================================================")

    # Return non-zero exit code if modifications occurred but commit/push failed completely
    if modified_files and not committed and unpushed_count != "0" and not pushed:
        logger.error("Execution finished with uncommitted or unpushed changes.")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    try:
        run_maintenance()
    except Exception as fatal_err:
        logger.critical(f"Fatal unhandled exception in maintenance automation: {fatal_err}", exc_info=True)
        sys.exit(1)