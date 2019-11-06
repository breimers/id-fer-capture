from setuptools import setup, find_packages

setup(
    name='fer_capture',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'keras',
        'numpy',
        'opencv-python',
        'python-magic',
    ],
    extras_require = {
    'gpu':  ['tensorflow-gpu'],
    'cpu': ['tensorflow']
    },
    entry_points='''
        [console_scripts]
        fer_capture=fer_capture.main:cli
    ''',
)
