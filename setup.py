from setuptools import setup, find_packages

setup(
    name='hunter',
    version='1.61',
    description="hunter allows you to check if the mail is used on different sites...",
    author='whoamikiddie',
    author_email='',
    url='http://github.com/whoamikiddie/hunter',
    packages=find_packages(),
    install_requires=[
        'termcolor',
        'bs4',
        'httpx',
        'trio',
        'tqdm',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'hunter = hunter.core:main'
        ]
    }
) 