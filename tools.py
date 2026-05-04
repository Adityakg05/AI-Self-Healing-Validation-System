"""
Tools for the AI-Self-Healing-Validation-System.

Tools that agents can use:
- fetch_logs: Retrieve application logs for analysis
- open_github_pr: Create GitHub Pull Request with fix
- run_tests: Simulate pytest on generated fix
"""

import ast
import os
from datetime import datetime
from typing import Optional

from github import Github, GithubException
from langchain_core.tools import tool


@tool
def fetch_logs(time_range: str = "1h", severity: str = "error") -> str:
    """Fetch logs from monitoring system."""
    from config import settings
    log_file = settings.log_file

    if not os.path.exists(log_file):
        return (
            "No logs found. The application may not have been started yet, "
            "or no errors have occurred. Please ensure the FastAPI app is running "
            "and has received requests."
        )

    try:
        with open(log_file, "r") as f:
            log_lines = f.readlines()

        if not log_lines:
            return "Log file is empty. No errors have been recorded yet."

        # Filter by severity
        if severity.lower() != "all":
            filtered_lines = [
                line for line in log_lines
                if severity.upper() in line or "CRITICAL" in line
            ]
        else:
            filtered_lines = log_lines

        # Parse time_range
        # In production, you'd parse timestamps and filter by actual time
        # For now, just return last N lines based on time_range
        line_limits = {
            "5m": 10,
            "15m": 30,
            "30m": 50,
            "1h": 100,
            "6h": 300,
            "1d": 500,
        }

        max_lines = line_limits.get(time_range, 100)
        recent_lines = filtered_lines[-max_lines:] if len(filtered_lines) > max_lines else filtered_lines

        if not recent_lines:
            return f"No logs found with severity '{severity}' in the last {time_range}."

        log_output = "".join(recent_lines)

        return f"""
=== Application Logs (Last {time_range}, Severity: {severity}) ===

{log_output}

=== End of Logs ===

Total lines returned: {len(recent_lines)}
"""

    except Exception as e:
        return f"Error reading logs: {str(e)}"


@tool
def run_tests(fix_code: str, original_code: str = "") -> dict:
    """Validate generated fix code."""
    errors = []

    # 1. Syntax check
    try:
        tree = ast.parse(fix_code)
    except SyntaxError as e:
        return {
            "passed": False,
            "message": "Fix code has syntax errors",
            "errors": [f"Syntax error at line {e.lineno}: {e.msg}"],
        }

    # 2. Preserve function signatures
    if original_code:
        try:
            orig_tree = ast.parse(original_code)
            original_funcs = {
                node.name
                for node in ast.walk(orig_tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            fixed_funcs = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            missing = original_funcs - fixed_funcs
            if missing:
                errors.append(
                    f"Functions removed from original code: {missing}. "
                    "All original functions must be preserved."
                )
                return {
                    "passed": False,
                    "message": f"Tests failed: {len(errors)} issue(s) found",
                    "errors": errors,
                }
        except SyntaxError:
            pass  # original broken - skip comparison

    # 3. No bare except clauses
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            errors.append(
                "Bare 'except:' found — use specific exception types "
                "(e.g. 'except KeyError:') to avoid masking unrelated errors."
            )

    if errors:
        return {
            "passed": False,
            "message": f"Tests failed: {len(errors)} issue(s) found",
            "errors": errors,
        }

    return {
        "passed": True,
        "message": "All tests passed! The fix is valid.",
        "errors": [],
    }


@tool
def open_github_pr(
    title: str,
    body: str,
    fix_code: str,
    file_path: str = "app.py",
    branch_name: Optional[str] = None
) -> str:
    """Create GitHub Pull Request with fix."""
    from config import settings
    github_token = settings.github_token
    github_repo = settings.github_repo

    # Fallback to simulation if GitHub not configured
    if not github_token or not github_repo:
        return _simulate_pr_creation(title, body, fix_code, file_path, branch_name)

    # GitHub PR creation
    try:
        from github import Auth as GithubAuth
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        auth = GithubAuth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(github_repo)

        # Generate branch name
        if not branch_name:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            branch_name = f"fix/sre-agent-{timestamp}"

        default_branch = repo.default_branch

        # Handle empty repository
        # An empty repo has no commits/branches yet. We must create an
        # initial commit before we can create branches or PRs.
        try:
            source = repo.get_branch(default_branch)
        except GithubException as e:
            if e.status == 404:
                # Repo empty - push initial commit
                repo.create_file(
                    path=file_path,
                    message="chore: initial commit by Self-Healing SRE Agent",
                    content=fix_code,
                    branch=default_branch,
                )
                return (
                    f"[SUCCESS] Repository was empty — created initial commit with fix on '{default_branch}'.\n\n"
                    f"Repo: https://github.com/{github_repo}\n\n"
                    f"Note: No PR was created because there was no base branch to compare against. "
                    f"The fix has been committed directly to '{default_branch}'."
                )
            raise  # Re-raise other 404s

        # Create fix branch
        repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=source.commit.sha,
        )

        # Commit fix file
        try:
            # File exists - update it
            existing = repo.get_contents(file_path, ref=default_branch)
            repo.update_file(
                path=file_path,
                message=f"fix: {title[:72]}",
                content=fix_code,
                sha=existing.sha,
                branch=branch_name,
            )
        except GithubException as e:
            if e.status == 404:
                # File doesn't exist - create it
                repo.create_file(
                    path=file_path,
                    message=f"fix: {title[:72]}",
                    content=fix_code,
                    branch=branch_name,
                )
            else:
                raise

        # Open Pull Request
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=default_branch,
        )

        return f"[SUCCESS] Pull Request created successfully!\n\nPR URL: {pr.html_url}\nPR Number: #{pr.number}"

    except GithubException as e:
        return f"[ERROR] GitHub API Error {e.status}: {e.data.get('message', str(e.data))}"
    except Exception as e:
        return f"[ERROR] Error creating PR: {str(e)}"


def _simulate_pr_creation(
    title: str,
    body: str,
    fix_code: str,
    file_path: str,
    branch_name: Optional[str]
) -> str:
    """Simulate PR creation for demo."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if not branch_name:
        branch_name = f"fix/sre-agent-{timestamp}"

    # Save fix to local file
    fix_file = f"generated_fix_{timestamp}.py"
    try:
        with open(fix_file, "w") as f:
            f.write(fix_code)
    except Exception:
        pass

    simulated_pr_url = "https://github.com/your-repo/pull/123"

    return f"""
[SIMULATED PR CREATION - Demo Mode]

[INFO] Pull Request would be created with:

Title: {title}
Branch: {branch_name}
File: {file_path}

Body:
{body}

Fix code has been saved to: {fix_file}

To enable real PR creation:
1. Set GITHUB_TOKEN in .env
2. Set GITHUB_REPO in .env (format: username/repo-name)

Simulated PR URL: {simulated_pr_url}
"""
