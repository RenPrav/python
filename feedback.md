**File Path**: pre-commit.py  
**Commit ID**: 11f35fe  

The commit introduces a **security vulnerability** by using `exec()` in the `__eq__` method of the `Evil` class. This can execute arbitrary code, making the application prone to attacks. Avoid using `exec()` unless absolutely necessary and ensure strict validation if required.  



-------------------------------------------------------------

