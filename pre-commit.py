import difflib
import git
import os
from google import genai

repo_path = os.path.dirname(os.path.abspath(__file__))
feedback_file = "feedback.md"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

def analyze_code_changes(file_path, commit_id, repo):
    old_code = get_previous_version(file_path)
    new_code = get_new_version(file_path)
    repo.git.reset("HEAD", file_path)
    diff = repo.git.diff()
    repo.git.add(file_path)
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
    
    Only respond with any recognised vulnerabilities. ONLY ADD NECESSSARY VULNERABILITIES.
    
    Also, evaluate if the changes improve the code quality and if any vulnerability were detected only then provide a summary otherwise respond " NO ISSUES ".
    KEEP IT SHORT 
    
    - File: {file_path}
        
    Code Diff:
    {diff}
    
    provide the details with the file name,commit id,issues and suggestion in a structured and short format.
    """
    
    prompt = f"""
    Given the diff of a file {file_path} and the commit ID
    Check if the commit is introducing any security vulnerabilities, poor code quality, syntax errors, maintainability issues, Logic & Best Practices, etc
    
    # Instructions
    - Provice concise response. ONLY Respond if there is an issue detected
    - If no issues are detected, respond with No Issues.
    - Always start with file path and commit ID, should mention the {file_path} and {commit_id} and then your concise response.
    - Donot exceed more thatn 100 words
    
    ```diff
    {diff}
    ```
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"text": prompt}]
    )
    return response.candidates[0].content.parts[0].text
    

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
        [analyze_code_changes(file, commit_id, repo) for file in staged_files]
    )

    print("\n=== AI Code Review Feedback ===")
    print(feedback_summary)

    commit_feedback(feedback_summary)
    print("feedback is pushed back to the repository.")


if __name__ == "__main__":
    main()
