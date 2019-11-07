from setuptools import setup, find_packages

setup(
    name='fer_capture',
    version='0.1.1',
    license='MIT',
    description='Give the function an image and it will return a dictionary of detected faces and emotion predictions.',
    author='Bradley Reimers',
    author_email = 'Bradley@IntrospectData.com',
    url='https://github.com/IntrospectData/id-fer-capture',
    download_url='https://github.com/IntrospectData/id-fer-capture/archive/v0.1.1.tar.gz',
    keywords = ['facial', 'detection', 'emotion', 'recognition'],
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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Data Science :: Utility',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
  ],
)
