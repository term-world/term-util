import setuptools

setuptools.setup(
    name="inventory",
    version="0.2",
    packages=['inventory'],
    package_dir={'inventory': 'src'},
    include_package_data=True,
    description='Global inventory system governing all items in term-world.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
