from distutils.core import setup


setup(
    name='trojan',
    version='0.2',
    description='Small helper library to bootstrap remote python',
    author='Anton Patrushev',
    author_email='apatrushev@gmail.com',
    url='https://github.com/apatrushev/python-trojan',
    license='MIT License',
    packages=[
        'trojan',
        'trojan.stages'
    ],
    install_requires=[
        'click'
    ],
    extras_require={
        'paramiko':  [
            'paramiko'
        ]
    }
)
