#! /usr/bin/env python
"""Build cython extensions.

isort:skip_file
"""
import multiprocessing
import os
from pathlib import Path
from typing import List

from setuptools import Distribution, Extension  # type: ignore
from Cython.Build import cythonize  # type: ignore
from Cython.Distutils.build_ext import new_build_ext as cython_build_ext  # type: ignore

SOURCE_DIR = Path("src")
BUILD_DIR = Path("cython_build")


def get_extension_modules() -> List[Extension]:
    """Collect all .py files and construct Setuptools Extensions"""
    extension_modules: List[Extension] = []

    source_paths = list(SOURCE_DIR.rglob("*.pyx"))
    for pxd_file in SOURCE_DIR.rglob("*.pxd"):
        py_file = pxd_file.with_suffix(".py")
        if py_file.exists():
            source_paths.append(py_file)

    for source_path in source_paths:
        sources = [str(source_path)]
        # Convert path to module name
        module_path = str(source_path.relative_to(SOURCE_DIR).with_suffix("")).replace(
            os.sep, "."
        )
        extension_module = Extension(
            name=module_path,
            sources=sources,
            define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        )

        extension_modules.append(extension_module)

    return extension_modules


def cythonize_helper(extension_modules: List[Extension], debug=True) -> List[Extension]:
    """Cythonize all Python extensions"""

    return cythonize(
        module_list=extension_modules,
        # Don't build in source tree (this leaves behind .c files)
        build_dir=str(BUILD_DIR),
        # Don't generate an .html output file. Would contain source.
        annotate=False,
        # Parallelize our build
        nthreads=multiprocessing.cpu_count() * 2,
        # Tell Cython we're using Python 3. Becomes default in Cython 3
        compiler_directives={"language_level": "3", "linetrace": debug},
        # (Optional) Always rebuild, even if files untouched
        force=not debug,
    )


def build(setup_kwargs=None, debug=False):
    # Collect and cythonize all files
    extension_modules = cythonize_helper(get_extension_modules(), debug=debug)

    # Use Setuptools to collect files
    distribution = Distribution(
        {
            "name": "subsequences",
            "package_dir": {"": str(SOURCE_DIR)},
            "ext_modules": extension_modules,
            "cmdclass": {
                "build_ext": cython_build_ext,
            },
        }
    )

    build_ext_cmd = distribution.get_command_obj("build_ext")
    build_ext_cmd.ensure_finalized()
    # Build inplace so that poetry knows where to pick up files during build
    # process
    build_ext_cmd.inplace = 1
    if debug:
        # Needed for coverage of cython modules
        build_ext_cmd.define = [("CYTHON_TRACE", 1)]
    # Actually build the extensions
    build_ext_cmd.run_command("build_ext")

    return setup_kwargs


if __name__ == "__main__":
    build()
