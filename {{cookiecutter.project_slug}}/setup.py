#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'futures',
    'requests',
    'flask',
    'Flask>=0.10.1',
    'flask-cors',
    'PyYaml',

]

celery_requirements = [
    'celery[redis]',
    'celery',
]

test_requirements = [
    "pytest",
    "coverage",
    "pytest-sugar",
    "pytest-cov",
    "pytest-ordering",
    "requests-mock"
]

setup(
    name='{{ cookiecutter.project_slug }}',
    version='{{cookiecutter.version}}',
    description="{{ cookiecutter.project_slug }}",
    long_description=readme,
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    url='{{cookiecutter.git}}',
    packages=[
        '{{ cookiecutter.project_slug }}',
        '{{ cookiecutter.project_slug }}.api',
        '{{ cookiecutter.project_slug }}.api.handlers',
        '{{ cookiecutter.project_slug }}.jobs',
    ],
    package_dir={'{{ cookiecutter.project_slug }}':
                 '{{ cookiecutter.project_slug }}'},
    include_package_data=True,
    install_requires=requirements + celery_requirements,
    license="Apache License version 2",
    zip_safe=False,
    keywords=['{{ cookiecutter.project_slug }}'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
