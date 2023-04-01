import setuptools

setuptools.setup(
    name="powergrid",
    version="0.1",
    packages=['powergrid'],
    package_dir={'powergrid': 'src'},
    include_package_data=True,
    description='Global resource pool for term-world resources',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
