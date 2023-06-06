import setuptools

setuptools.setup(
    name="gitit",
    version="0.1",
    packages=['gitit'],
    include_package_data=True,
    description='Limited module for writing (not cloning) raw files from GitHub.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
