# coding: utf8
from setuptools import setup, find_packages


def parse_requirements(file: str) -> list:
    """
    Parse requirements.txt file pip packages
    Args:
        file (str): requirement.txt file path

    Returns:
        list
    """
    with open(file, encoding='utf8') as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


def setup_package():
    """
    Packages setup functions with all required parameters
    Returns:
        Null
    """

    package_name = 'kueski_mle_task'

    # Required packages
    requires = parse_requirements("requirements.txt")

    setup(
            name=package_name,
            version='0.0.1',
            packages=find_packages(),
            install_requires=requires
    )


if __name__ == '__main__':
    setup_package()