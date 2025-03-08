**File Path**: pre-commit.py  
**Commit ID**: 11f35fe  

The commit introduces a **security vulnerability** by using `exec()` in the `__eq__` method of the `Evil` class. This can execute arbitrary code, making the application prone to attacks. Avoid using `exec()` unless absolutely necessary and ensure strict validation if required.  



-------------------------------------------------------------

**File Path:** pre-commit.py  
**Commit ID:** 695028f  

Detected Issue: The `Evil.__eq__` method uses `exec` with hardcoded malicious code (`exec("print('Hacked!'); import os;")`), which introduces a severe security vulnerability by allowing arbitrary code execution. Methods like `exec` should be avoided due to their risk of abuse. Remove or refactor for security and best practices.

-------------------------------------------------------------

