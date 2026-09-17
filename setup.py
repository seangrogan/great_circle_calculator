import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="great_circle_calculator",
    version="2.0.0",
    author="Sean Grogan",
    author_email="sean.grogan@gmail.com",
    description="A collection of functions to calculate attributes of the great circle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seangrogan/great_circle_calculator",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Utilities"
    ],
)
