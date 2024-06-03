from nox_poetry import session

py_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@session(python=py_versions)
def with_coverage(session):
    session.install(".")
    session.run("coverage", "run", "-m", "pytest", "tests", "-vvs", "-n", "auto")
    session.run("coverage", "report", "-m", "--fail-under", "50")


@session(python=py_versions)
def unit_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-vvs", "-n", "auto")
