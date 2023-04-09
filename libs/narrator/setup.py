import setuptools

setuptools.setup(
    name="narrator",
    version="0.1",
    packages=['narrator'],
    include_package_data=True,
    description='Global inventory system governing all items in term-world.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
