from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

setup(
    name='bmi_calculator',
    version='0.1.0',
    description='This package is to calculate BMI based on height and weight.',
    long_description=readme,
    author='Swaraj Bhagat',
    author_email='swarajbhagat11@gmail.com',
    url='https://github.com/swarajbhagat11/code-10_Nov_2021-Swaraj_Bhagat',
    packages=find_packages(exclude=('tests'))
)
