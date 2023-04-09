import setuptools

setuptools.setup(
    name="marketplace",
    version="0.1",
    packages=['marketplace']
    include_package_data=True,
    description='Global marketplace for items in term-world.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
