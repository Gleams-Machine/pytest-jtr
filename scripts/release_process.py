import subprocess
from rich.console import Console

console = Console()


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").casefold()
    return reply == "y"


def _run_tests():
    console.rule("[bold blue]Executing tests via nox")
    with console.status("[bold green] Test execution in progress..."):
        cmd = ["nox", "-s", "tests"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            console.print("[bold red] :broken_heart: Tests have failed. Please investigate")
            console.print(result.stdout)
            console.print(result.stderr)
            exit(result.returncode)
        else:
            console.print("[bold green] :green_heart: Tests have passed. Moving on...")


def _run_static_checks():
    console.rule("[bold blue]Executing static code analysis checks")
    with console.status("[bold green] Static code checks in progress..."):
        cmd = ["nox", "-s", "static"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            console.print(result.returncode)
            console.print("[bold red] :broken_heart: Checks have failed. Please investigate")
            console.print(result.stdout)
            console.print(result.stderr)
            exit(result.returncode)
        else:
            console.print("[bold green] :green_heart: Checks have passed. Moving on...")


def _run_release_process(release_type: str):
    console.rule("[bold blue]Preparing a patch release")

    cmd = ["poetry", "version"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    console.print(f"Package current version: {result.stdout}")

    cmd = ["poetry", "version", release_type]
    console.print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    console.print(f"Package updated version: {result.stdout}")

    cmd = ["poetry", "build"]
    console.print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    console.print(f"Package updated version: {result.stdout}")
    if result.returncode:
        exit(result.returncode)

    if confirm_prompt("Do you want to upload to TestPyPI?"):
        cmd = ["poetry", "publish", "-r", "test-pypi"]
        console.print(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        console.print(result)
        console.print(result.stdout)
        console.print(result.stderr)


def upload_release():
    if confirm_prompt("Do you want to upload to PyPI?"):
        cmd = ["poetry", "publish"]
        console.print(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        console.print(result)
        console.print(result.stdout)
        console.print(result.stderr)


def prep_dev():
    _run_tests()
    _run_static_checks()
    _run_release_process(release_type="prerelease")


def prep_patch():
    _run_tests()
    _run_static_checks()
    _run_release_process(release_type="patch")


def prep_minor():
    _run_tests()
    _run_static_checks()
    _run_release_process(release_type="minor")


def prep_major():
    _run_tests()
    _run_static_checks()
    _run_release_process(release_type="major")
