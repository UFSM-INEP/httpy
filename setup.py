from setuptools import setup

setup(
    name='httpy',
    version='1.0',
    url='https://github.com/UFSM-INEP/httpy',
    author='Marcos Visentini',
    author_email='marcosvisentini@gmail.com',
    license='MIT',
    py_modules=['httpy'],
    install_requires=['requests'],
    extras_require={
        'dev': ['pytest']
    },
    python_requires='>=3.8',
)
