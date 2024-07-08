from setuptools import setup, find_packages
import os

package_name = 'f1_tenth_utils'


# 리소스 디렉토리의 모든 파일을 포함하는 함수
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


ui_files = package_files(os.path.join('resource', 'ui'))
icon_files = package_files(os.path.join('resource', 'icons'))

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (f'share/{package_name}/resource/ui', ui_files),
        (f'share/{package_name}/resource/icons', icon_files),
    ],
    install_requires=['setuptools', 'PyQt5'],
    zip_safe=True,
    maintainer='Juyoung Kim',
    maintainer_email='ymail3@naver.com',
    description='F1 Tenth Utilities',
    license='License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'f1_tenth_utils = f1_tenth_utils.main:main'
        ],
    },
)
