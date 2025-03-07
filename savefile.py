import git
import os

# Define your local Git repository path
repo_path = r"C:\Users\sowmi\OneDrive\Desktop\ABB_hackathon"

# Define the files you want to track
feedback_files = ["feedback.txt"]

try:
    # Open the local Git repository
    repo = git.Repo(repo_path)

    # Ensure the repository is not in a detached HEAD state
    if repo.head.is_detached:
        print("Error: Git is in a detached HEAD state. Please check your repository.")
        exit(1)

    # Get the current branch name
    current_branch = repo.active_branch.name

    # Pull the latest changes from the remote repository (Optional: Can be removed if working offline)
    repo.git.pull("origin", current_branch)

    # Check if the files exist before adding
    files_to_add = [f for f in feedback_files if os.path.exists(os.path.join(repo_path, f))]

    if not files_to_add:
        print("Error: None of the feedback files exist in the repository folder.")
        exit(1)

    # Add feedback files to Git
    repo.index.add(files_to_add)

    # Commit the changes locally
    repo.index.commit("Automated commit: Updated AI-generated feedback files")

    print("Feedback files committed locally.")

except git.exc.GitCommandError as git_error:
    print(f"Git command error: {git_error}")
except Exception as e:
    print(f"Error: {e}")
