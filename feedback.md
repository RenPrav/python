**File:** pre-commit.py  
**Commit ID:** bacc871  

Detected Issue:  
- **Security Vulnerability:** The `__eq__` method in the `Evil` class uses `exec`, which can execute arbitrary code, making the code prone to remote code execution (RCE) attacks. Avoid using `exec` unless absolutely necessary and ensure inputs are sanitized.  



-------------------------------------------------------------

**File Path:** pre-commit.py  
**Commit ID:** a21867b  

**Issue Detected:**  
The `Evil` class introduces a security vulnerability due to the use of `exec()` with potentially malicious behavior (`print('Hacked!'); import os;`). This poses a critical risk of arbitrary code execution and should be removed or replaced with safe alternatives.

-------------------------------------------------------------

