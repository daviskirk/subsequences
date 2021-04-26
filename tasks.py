#! /usr/bin/env python
import shlex
import subprocess
import sys
from pathlib import Path

import click


@click.group()
def cli():
    """Dev tasks."""


@cli.command()
@click.option("--debug/--release", required=True)
def build(debug):
    """Format code using isort and black."""
    s = "Cythonizing source code"
    s += " in debug/test mode" if debug else "in release mode"
    click.secho(s, fg="cyan")
    from build import build

    build(debug=debug)
    click.secho("Success!", fg="green")


@cli.command()
def clean():
    """Format code using isort and black."""
    click.secho(
        "Removing cythonized and compiled files and build directories", fg="cyan"
    )
    import shutil

    from build import BUILD_DIR

    root = Path(__file__).parent
    for glob in ["*.c", "*.so", "*.pyd"]:
        for path in root.rglob(glob):
            path.unlink()
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    click.secho("Success!", fg="green")


@cli.command()
def format():
    """Format code using isort and black."""
    _run("isort .")
    _run("black .")


@cli.command()
def lint():
    """Run isort, black, flake8 and mypy checks."""
    _run("isort --check-only --diff .")
    _run("black --check --diff .")
    _run("flake8 .")
    _run("mypy src")


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("pytest_args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def test(ctx, pytest_args):
    """Run tests."""
    ctx.invoke(build, debug=True)
    _run(["coverage", "run", "-m", "pytest"] + list(pytest_args))
    _run("coverage html")
    _run("coverage report")


@cli.command()
@click.pass_context
def all(ctx):
    """Run format, lint and tests."""
    ctx.invoke(format)
    ctx.invoke(lint)
    ctx.invoke(test)


def _run(args, **kwargs):
    if isinstance(args, str):
        args = shlex.split(args)
    click.secho(shlex.join(args), fg="cyan")
    process = subprocess.run(args, **kwargs)
    if process.returncode != 0:
        sys.exit(process.returncode)
    return process


if __name__ == "__main__":
    cli()
