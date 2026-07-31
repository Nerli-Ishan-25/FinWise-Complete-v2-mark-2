import os
import random
from datetime import datetime, timedelta
from git import Repo

# Set repository path manually since auto-detection might fail with custom Git setup
repo = Repo(r'D:\FinWise-Complete-v2-mark-2')

def select_dead_code_blocks():
 python_dead_code = [
 'def unused_python_function():\n """Unused docstring."""\n pass\n',
 'if False:\n print("This will never execute.")\n',
 'class UnusedPythonClass:\n pass\n'
 ]
 
 js_dead_code = [
 'function unusedJsFunction() {\n  // Unused function\n}',
 'if (false) {\n  console.log("This will never execute.");\n}',
 'const UNUSED_JS_VARIABLE = null;\n'
 ]
 
 return {
 "python": random.sample(python_dead_code, 3),
 "javascript": random.sample(js_dead_code, 3)
 }

def insert_dead_code(file_path, dead_code_blocks):
 with open(file_path, 'a') as file:
 for block in dead_code_blocks:
 file.write('\n' + block + '\n')

def remove_last_inserted_block(file_path):
 with open(file_path, 'r+') as file:
 lines = file.readlines()
 
 # Find last blank line and remove everything after it until next non-blank line
 for i in reversed(range(len(lines))):
 if lines[i].strip() == '':
 del lines[i:]
 break
 
 file.seek(0)
 file.writelines(lines)
 file.truncate()

# Track cycle state via Git config variable
last_run_date_key = "maintenance:last_run"

try:
 config_date_str = repo.git.config(f"--get {last_run_date_key}")
except Exception:  
# Key doesn't exist yet (first run)
cycle_day_count = 0
 
else:  
# Load existing date to calculate cycle day count
config_date_obj = datetime.strptime(config_date_str, '%Y-%m-%d')
today_date_obj = datetime.now()
cycle_day_count = (today_date_obj - config_date_obj).days
 
finally:  
# Update last run date regardless of action taken
today_str = today_date_obj.strftime('%Y-%m-%d')
repo.git.config(f"--local {last_run_date_key}", today_str)

file_paths_by_language = {
"python": [
r"D:\FinWise-Complete-v2-mark-2\Backend\app\api\admin_routes.py",
r"D:\FinWise-Complete-v2-mark-2\Backend\app\api\assistant_routes.py"
],
"javascript": [
r"D:\FinWise-Complete-v2-mark-2\AI-assistant-FRNTD\src\features\assistant\hooks\useAssistant.js",
r"D:\FinWise-Complete-v2-mark-2\AI-assistant-FRNTD\src\features\assistant/constants/featureCards.js"
]
}

dead_code_dict = select_dead_code_blocks()

for language in ["python", "javascript"]:
files_to_edit = [file_paths_by_language[language][0], file_paths_by_language[language][1]]
dead_code_blocks = dead_code_dict[language]

if cycle_day_count % 4 == 0:  
# Day 1: Insert all dead code blocks into target files  
for filepath in files_to_edit:
insert_dead_code(filepath, dead_code_blocks)

commit_message = "src code optimization"
repo.git.commit("-am", commit_message)

elif cycle_day_count % 4 == 1 or cycle_day_count % 4 == 3:  
# Day after initial insertion and cleanup phase before reset-remove first two blocks from each selected JavaScript/Python file  
for filepath in files_to_edit:
remove_last_inserted_block(filepath)  

commit_message = "Debugging API routes"
repo.git.commit("-am", commit_message)  

elif cycle_day_count % 4 == 2 or cycle_day_count % 4 >= len(files_to_edit):  
# Final cleanup phase-remove remaining blocks across all target files 
for filepath in files_to_edit:
remove_last_inserted_block(filepath)  

commit_message = "src code optimization"
repo.git.commit("-am", commit_message)
