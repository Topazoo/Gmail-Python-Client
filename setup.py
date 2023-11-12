from setuptools import setup, find_packages

def get_requirements():
    with open('src/requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(
    name='gmail_python_client',
    version='0.0.4',
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=get_requirements(),
    author='Peter Swanson',
    author_email='pswanson@ucdavis.edu',
    description='Client for Sending Emails via GMail using OAuth2.0',
    license='LICENSE',
    url='https://github.com/Topazoo/Gmail-Python-Client',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
