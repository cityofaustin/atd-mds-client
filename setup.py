import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atd-mds-client",
    version="0.0.4",
    author="City of Austin",
    author_email="transportation.data@austintexas.gov",
    description="A Python utility to interact data endpoints compliant with the Mobility Data Specification, as designed by the Open Mobility Foundation",
    install_requires=[
      'requests',
      'pytz',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofaustin/atd-mds-client/tree/atd-mds-client",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ),
)
