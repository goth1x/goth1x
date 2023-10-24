from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_ymax',
    version='0.0.5',
    description='Organize folder with file types',
    author='Maksym Y',
    author_email='minilond@gmail.com',
    url='https://github.com/goth1x/goth1x.git',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean=clean_folder_ymax.clean:start']}
)
