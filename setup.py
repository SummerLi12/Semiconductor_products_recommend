from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="semiconductor supplies-recommender",
    version="0.1",
    author="JinduoLi",
    packages=find_packages(),
    install_requires = requirements,
)