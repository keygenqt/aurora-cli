import setuptools

long_description = """
![picture](https://github.com/keygenqt/aurora-cli/blob/main/data/images/banner/banner_1000.png?raw=true)

[![picture](https://github.com/keygenqt/aurora-cli/blob/main/data/common/btn_more.png?raw=true)](https://keygenqt.github.io/aurora-cli/)

### License

```
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
"""

setuptools.setup(
    name='aurora-cli',
    version='3.0.8.0',
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
        'beautifulsoup4>=4.12.3',
        'weasyprint>=61.1',
        'pillow>=10.2.0',
        'diskcache>=5.6.3',
    ],
    python_requires='>=3.8.10',
    entry_points={
        'console_scripts': [
            'aurora-cli = aurora_cli.__main__:main',
        ],
    },
)
