import nox
from nox_poetry import session

nox.options.sessions = ["static", "tests"]


@session(python=["3.8", "3.9", "3.10"])
def with_coverage(session):
    session.install(".")
    session.run("coverage", "run", "-m", "pytest", "tests", "-vvs", "-n", "auto")
    session.run("coverage", "report", "-m", "--fail-under", "50")


@session(python=["3.8", "3.9", "3.10"])
def unit_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-vvs", "-n", "auto")


@session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.notify("unit_tests")


@session(python=["3.8", "3.9", "3.10"])
def flake8(session):
    session.run("flake8")


@session(python=["3.8", "3.9", "3.10"])
def isort(session):
    session.run("isort", "pytest_jtr")


@session(python=["3.8", "3.9", "3.10"])
def bandit(session):
    session.run("bandit", "--configfile", "bandit.yml", "--recursive", "pytest_jtr")


@session(python=["3.8", "3.9", "3.10"])
def safety(session):
    session.run("safety", "check", "--ignore=51457")


@session(python=["3.8", "3.9", "3.10"])
def black(session):
    session.run("black", "pytest_jtr")


@session(python=["3.8", "3.9", "3.10"])
def mypy(session):
    session.run("mypy", "-p", "pytest_jtr")


@session(python=["3.8", "3.9", "3.10"])
def static(session):
    session.notify("isort")
    session.notify("flake8")
    session.notify("bandit")
    session.notify("black")
    session.notify("mypy")
