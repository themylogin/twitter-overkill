from setuptools import find_packages, setup

setup(
    name="twitter-overkill",
    version="0.0.0",
    author="themylogin",
    author_email="themylogin@gmail.com",
    packages=find_packages(exclude=["tests"]),
    scripts=[],
    test_suite="nose.collector",
    url="http://github.com/themylogin/twitter-overkill",
    description="Overengineered twitter posting solution",
    long_description=open("README.md").read(),
    install_requires=[
        "celery",
        "PyExecJS",
        "python-twitter",
        "pyyaml",
    ],
    setup_requires=[
        "nose>=1.0",
    ],
)
