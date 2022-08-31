import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="great_circle_calculator",
    version="1.3.0",
    author="Sean Grogan",
    author_email="sean.grogan@gmail.com",
    description="A collection of functions to calculate attributes of the great circle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seangrogan/great_circle_calculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Utilities"
    ],
)
