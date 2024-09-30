from setuptools import find_packages, setup

PACKAGE_NAME = "utils"

# Read version
with open(f"src/{PACKAGE_NAME}/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("\"'")
            break
    else:
        raise RuntimeError(
            f"Unable to find __version__ in src/{PACKAGE_NAME}/__init__.py"
        )

# Read requirements
with open("requirements/main.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    author="Leonard Schuler",
    description="Time series utils to ease usage in notebooks.",
    url="https://github.com/LeonardSchuler/time-series-forecasting",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
