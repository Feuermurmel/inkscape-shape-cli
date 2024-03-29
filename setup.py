import setuptools


setuptools.setup(
    name='inkscape-shape-cli',
    version='1.0.0',
    packages=setuptools.find_packages(),
    package_data={'': ['*.txt']},
    entry_points=dict(
        console_scripts=[
            'inkscape2dxf = inkscapeshapecli.inkscape2dxf:script_main']),
    install_requires=['lxml'])
