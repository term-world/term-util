import setuptools

setuptools.setup(
    name="worldlib",
    version="0.1",
    packages=['worldlib'],
    package_dir={'worldlib': 'src'},
    include_package_data=True,
    description='Shorthand import for all world-specific libraries for term-world narrative objects.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
