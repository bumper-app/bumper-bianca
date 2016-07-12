import setuptools
from packagename.version import Version


setuptools.setup(name='py-bianca',
                 version=Version('0.0.1').number,
                 description='TBA',
                 long_description=open('README.md').read().strip(),
                 author='Mathieu Nayrolles',
                 author_email='mathieu.nayrolles@gmail.com',
                 url='https://github.com/bumper-app/bumper-bianca',
                 py_modules=['py-bianca'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='tba',
                 classifiers=['tba'])
