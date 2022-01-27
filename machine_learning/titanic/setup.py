from glob import glob

from os.path import basename
from os.path import splitext

from setuptools import find_packages, setup


setup(
    name="titanic",
    version="0.0.1",
    description="Titanic Sample",
    python_requires=">=3.9",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    author="datafy",
    zip_safe=False,
    keywords="data pipelines, data engineering, machine learning",
    extras_require={},
)
