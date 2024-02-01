import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aurora-cli',
    version='2.1.1',
    author='Vitaliy Zarubin',
    author_email='keygenqt@gmail.com',
    description='An application that simplifies the life of an application developer for the Aurora OS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/keygenqt/aurora-cli",
    packages=setuptools.find_packages(exclude=['*tests.*', '*tests']),
    include_package_data=True,
    py_modules=['colors'],
    install_requires=[
        'click>=8.1.7',
        'requests>=2.31.0',
        'alive-progress>=3.1.5',
        'pyYaml>=6.0.1',
        'paramiko>=3.4.0',
        'cffi>=1.16.0',
        'GitPython>=3.1.41',
        'shiv>=1.0.4',
    ],
    python_requires='>=3.8.2',
    entry_points={
        'console_scripts': [
            'aurora-cli = aurora_cli.__main__:main',
        ],
    },
)
