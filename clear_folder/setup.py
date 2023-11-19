from setuptools import setup, find_namespace_packages

setup(
    name='clear_folder',
    version='0.0.1',
    description='Very useful code',
    url='https://github.com/AnnaAmKh/module_7_hw/tree/master/clear_folder',
    author='Anna Amelina',
    author_email='author@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clear_folder=clear_folder.clear:main']}
)
