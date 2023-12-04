from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in interest_calculation/__init__.py
from interest_calculation import __version__ as version

setup(
	name="interest_calculation",
	version=version,
	description="Interest Calculation",
	author="Abhishek Chougule",
	author_email="chouguleabhis@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
