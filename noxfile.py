import nox
from nox_poetry import session


nox.options.sessions = ["static", "tests"]


@session(python=["3.9"])
def with_coverage(session):
    session.install(".")
    session.run(
        'coverage', 'run', '-m',
        'pytest', 'tests', '-vvs', '-n', 'auto'
    )
    session.run('coverage', 'report', '-m', '--fail-under', '50')


@session(python=["3.9"])
def unit_tests(session):
    session.install(".")
    session.run('pytest', 'tests', '-vvs', '-n', 'auto')


@session(python=["3.9"])
def tests(session):
    session.notify("unit_tests")


@session(python=["3.9"])
def flake8(session):
    session.run('flake8')


@session(python=["3.9"])
def isort(session):
    session.run('isort', 'pytest_jtr')


@session(python=["3.9"])
def bandit(session):
    session.run(
        'bandit', '--configfile', 'bandit.yml', '--recursive', 'pytest_jtr'
    )


@session(python=["3.9"])
def safety(session):
    session.run('safety', 'check')


@session(python=["3.9"])
def black(session):
    session.run('black', 'pytest_jtr')


@session(python=["3.9"])
def mypy(session):
    session.run('mypy', '-p', 'pytest_jtr')


@session(python=["3.9"])
def static(session):
    session.notify("isort")
    session.notify("flake8")
    session.notify("bandit")
    session.notify("safety")
    session.notify("black")
    session.notify("mypy")
