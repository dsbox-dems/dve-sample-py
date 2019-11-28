from setuptools import setup, find_packages

setup(
    name='dqn-spaceinvadres-pytorch',
    version='1.0.0',
    packages=find_packages('dqn'),
    package_dir={'': 'dqn'},
    url='https://gitlab.com/ub-dems/ds-labs/lab-ds-mb101/pub-samples/dqn_spaceinvadres_pytorch',
    license='',
    author='gp21021',
    author_email='dsbox.dems@gmail.com',
    install_requires=[
        'mypy-lang',
        'py',
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
        'torch',
        'PyOpenCL'
    ],
    tests_requires=[
        'colorama',
        'pbr',
        'mock',
        'polling',
        'pluggy',
        'pytest',
        'atomicwrites',
        'attrs',
        'more-itertools',
        'six',
	'gym'
    ],
    description='dqn spaceinvadres pytorch'
)

