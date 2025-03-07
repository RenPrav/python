import difflib
from openai import AzureOpenAI

# Azure OpenAI Configuration
import os


API_KEY = os.environ.get('API_KEY')  # Replace hardcoded API key
SECRET_KEY = os.environ.get('SECRET_KEY')  # Replace hardcoded secret key

endpoint = os.environ.get('ENDPOINT')
deployment = "gpt-4o"

# Initialize Azure OpenAI Client using DefaultAzureCredential directly
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=SECRET_KEY,
    api_version="2024-10-21",
)

def analyze_code_changes(old_file, new_file, commit_id):
    """
    Compares the old and new file versions and returns AI-generated suggestions using Azure OpenAI.
    
    :param old_file: Path to the old version of the file.
    :param new_file: Path to the new version of the file.
    :param commit_id: The Git commit ID for reference.
    :return: AI-generated review suggestions as a string.
    """
    try:
        with open(old_file, 'r') as f1, open(new_file, 'r') as f2:
            old_code = f1.readlines()
            new_code = f2.readlines()

        # Generate a unified diff between old and new code
        diff = ''.join(difflib.unified_diff(old_code, new_code, lineterm=''))

        if not diff.strip():
            return "✅ No significant changes detected."

        # Build the prompt with the code diff and file names
        prompt = f"""Analyze the following code changes between {old_file} and {new_file} (Commit ID: {commit_id}) and provide concise feedback with file names:\n{diff}
            Format:
            ===============================
            AI Code Review Feedback
            ===============================

            - File: <filename>
              Issues: <issue type 1>, <issue type 2>, ...
              Suggestions: <brief suggestion 1>, <brief suggestion 2>, ...
              -------------------------------
            Example:
            - File: {new_file}
              Issues: Bug, Performance
              Suggestions: Fix syntax error on line 10, Optimize the Fibonacci calculation.
            -------------------------------

            Additionally, please evaluate whether the new commit is an improvement over the previous version and provide a precise summary.
            """

        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt}]
        )

        # Return AI-generated suggestions
        return response.choices[0].message.content

    except FileNotFoundError as e:
        return f"❌ Error: {str(e)}"

old_version = "OldFile.py"
new_version = "NewFile.py"
commit_id = "abc1234"  # Example commit ID

review_suggestions = analyze_code_changes(old_version, new_version, commit_id)

print(review_suggestions)
