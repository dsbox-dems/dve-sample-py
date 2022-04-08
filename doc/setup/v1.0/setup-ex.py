from setuptools import setup, find_packages

setup(
    name="dve-sample-py",
    version="1.0.0",
    packages=find_packages("dve"),
    package_dir={"": "dve"},
    url="https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py",
    license="",
    author="gp21021",
    author_email="dsbox.dems@gmail.com",
    install_requires=["py", "numpy", "scipy", "rootpath"],
    tests_require=["colorama", "mock", "pytest", "attrs", "more-itertools", "six"],
    description="dve sample py",
)
