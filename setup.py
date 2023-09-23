from setuptools import find_packages, setup

setup(
    name="Pygame_Engine",
    version="0.0.1",
    description="A package to create GUIs in pygame, featuring labels, buttons, etc.",
    packages=find_packages(),
    url="https://github.com/Golfmensch99/Pygame_Engine.git",
    author="Marcel Menzel",
    license="MIT",
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=["pygame >= 2.0.0"],
    python_requires=">=3.11"
)