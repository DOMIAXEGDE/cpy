from setuptools import setup, find_packages

setup(
    name="Amalec",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "keyboard",
        "matplotlib",
        "numpy",
        "pygame",
        "Pillow",
        "plotly",
        "psutil",
        "pyautogui",
        "PyQt5",
        "qiskit",
        "requests",
        "schemdraw",
        "schedule",
    ],
    entry_points={
        'console_scripts': [
            'quantum_arithmetic=C:main',
        ],
    },
    author="Mr. Dominic Alexander Cooper",
    author_email="dacgde.cooper@gmail.com",
    description="A Python application for generating quantum circuits and performing arithmetic geometry using state shapes, and much more.",
    license="MIT",
    keywords="quantum circuits arithmetic geometry image generation cosmology language generation",
    url="https://github.com/domiaxegde/cpy",
)
