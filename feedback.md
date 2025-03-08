**File:** pre-commit.py  
**Commit ID:** bacc871  

Detected Issue:  
- **Security Vulnerability:** The `__eq__` method in the `Evil` class uses `exec`, which can execute arbitrary code, making the code prone to remote code execution (RCE) attacks. Avoid using `exec` unless absolutely necessary and ensure inputs are sanitized.  



-------------------------------------------------------------

