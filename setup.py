from setuptools import setup

setup(
    name='sekrets',
    version='0.1',
    py_modules=['sekrets'],
    install_requires=[
        'Click>=4.0',
        'python-gnupg>=0.3.7',
        'requests>=2.7.0',
    ],
    entry_points='''
        [console_scripts]
        sekrets=sekrets:cli
    ''',
)
