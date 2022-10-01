import setuptools

setuptools.setup(
    name="assignment creator",
    version="0.1",
    packages=['creator'],
    package_dir={'creator': 'src'},
    include_package_data=True,
    description='CLI utility designed to create assignment templates.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
