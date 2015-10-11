from distutils.core import setup


setup(
    name='trojan',
    version='0.1',
    description='Small helper library to bootstrap remote python',
    author='Anton Patrushev',
    author_email='apatrushev@gmail.com',
    url='https://github.com/apatrushev/python-trojan',
    license='MIT License',
    packages=[
        'trojan',
        'trojan.stages'
    ]
)
