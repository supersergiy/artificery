import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="artificery",
    version="0.0.2.7",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="A tool for building pyrorch nets from spec files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supersergiy/artificery",
    include_package_data=True,
    package_data={'': ['*.py']},
    install_requires=[
      'scalenet',
      'torch',
      'torchvision'
    ],
    packages=setuptools.find_packages(),
)
