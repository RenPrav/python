import difflib
import git
import os
from openai import AzureOpenAI

repo_path = os.path.dirname(os.path.abspath(__file__))
feedback_file = "feedback.md"

SECRET_KEY = os.environ.get('AZURE_KEY')
endpoint = os.environ.get('END_POINT')
deployment = "gpt-4o"

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=SECRET_KEY,
    api_version="2024-10-21",
)

def get_previous_version(file_path):
    try:
        prev_content = git.Repo(repo_path).git.show(f"HEAD:{file_path}")
        return prev_content.splitlines()
    except Exception:
        return []

def get_new_version(file_path):
    try:
        with open(os.path.join(repo_path, file_path), "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []  

def analyze_code_changes(file_path, commit_id):
    old_code = get_previous_version(file_path)
    new_code = get_new_version(file_path)

    diff = ''.join(difflib.unified_diff(old_code, new_code, lineterm=''))

    if not diff.strip():
        return f"✅ No significant changes detected in {file_path}."

    prompt = f"""Analyze the following code changes in {file_path} (Commit ID: {commit_id}) and provide concise feedback:


    look for the following vulnerabilities :
    
    1.Security Issues
    Injection Attacks (SQLi, Command Injection, Code Injection)
    Cross-Site Attacks (XSS, CSRF, Clickjacking)
    Weak Authentication (Hardcoded credentials, weak JWTs, privilege escalation)
    Insecure Data Handling (Exposed APIs, insecure deserialization, debug info leaks)
    
    2. Memory & Performance Issues
    Buffer Overflows (Stack/Heap overflows, integer overflows)
    Resource Leaks (Memory, file descriptors, threads)
    Denial of Service (DoS) (Infinite loops, ReDoS, resource exhaustion)
    
    3. Logic & Best Practices
    Poor Exception Handling (except Exception: pass, swallowing errors)
    Race Conditions (TOCTOU, concurrent file access)
    Weak Cryptography (MD5, SHA1, hardcoded keys, weak randomness)
    
    4. Dependency & Configuration Issues
    Outdated & Vulnerable Dependencies (Unpatched CVEs, missing version pinning)
    Misconfigured Security Settings (Debug mode enabled, weak CORS, default credentials)
    
    5. Maintainability Issues
    Poor Coding Practices (Magic numbers, dead code, duplicate logic)
    Lack of Documentation (Missing docstrings, unclear function names)
    Inconsistent Formatting (Mixed indentation, non-standard naming)
    
    6.check for syntax errors 
    
    7.check for time complexity and space complexity.
    
    Also, evaluate if the changes improve the code quality and if any vulnerability were detected only then provide a summary otherwise respond " NO ISSUES ".
    KEEP IT SHORT 
    
    - File: {file_path}
        
    Code Diff:
    {diff}
    
    provide the details with the file name,commit id,issues and suggestion in a structured and short format.
    """

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def commit_feedback(feedback_text):
    try:
        repo = git.Repo(repo_path)
        current_branch = repo.active_branch.name

        feedback_path = os.path.join(repo_path, feedback_file)
        with open(feedback_path, "a", encoding="utf-8") as f:
            f.write(feedback_text + "\n\n-------------------------------------------------------------\n\n")

        repo.git.add(feedback_file)
        print("✅ Feedback committed.")

    except Exception as e:
        print(f"❌ Git Commit Error: {e}")

def main():
    repo = git.Repo(repo_path)
    staged_files = repo.git.diff("--cached", "--name-only").splitlines()

    if not staged_files:
        print("No files staged for commit.")
        exit(0)

    commit_id = repo.head.object.hexsha  

    feedback_summary = "\n".join(
        [analyze_code_changes(file, commit_id) for file in staged_files]
    )

    print("\n=== AI Code Review Feedback ===")
    print(feedback_summary)

    commit_feedback(feedback_summary)
    print("feedback is pushed back to the repository.")

if __name__ == "__main__":
    main()