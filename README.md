`**GitSense: AI-Powered Code Review Assistant**`   ![image](https://github.com/user-attachments/assets/7dd8186e-ab12-4d49-ba25-196c87176363)

**Overview**

This pre-commit hook automatically analyzes staged files before they are committed. It checks for security vulnerabilities, performance issues, and logical inconsistencies using AI-powered analysis.

**Workflow**

Check for Staged Files – If no files are staged, the hook exits.

Retrieve Commit ID – Captures the commit ID for reference.

Analyze Staged Files – Compares the previous and new versions using Git.

Compute Code Diff – Identifies significant changes.

Trigger AI Feedback – If notable changes exist, Azure OpenAI reviews the code.

Issue Detection – Detects security, performance, and logic issues.

Generate Report – Summarizes findings in feedback.txt.

Stage & Commit Feedback – Adds feedback to the commit.

Complete Pre-Commit Hook – Ensures code quality before finalizing the commit.
