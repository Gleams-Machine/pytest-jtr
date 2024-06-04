from nox_poetry import session

py_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@session(python=py_versions)
def unit_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-vvs", "-n", "auto")
