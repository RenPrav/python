**File Path:** pre-commit.py  
**Commit ID:** 62e0d75  

The addition of the `Evil` class introduces a significant security vulnerability. The use of the `exec` function with a hardcoded command (`exec("print('Hacked!'); import os;")`) poses a risk of arbitrary code execution. This is dangerous, violates best practices, and compromises security. Avoid using `exec` unless absolutely necessary and ensure user inputs or hardcoded strings are sanitized.

-------------------------------------------------------------

