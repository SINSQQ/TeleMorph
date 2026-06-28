"""
Setup script for TeleMorph.

Install:
    pip install -e .

Or with extras:
    pip install -e .[telethon,pyrogram,kurigram,opentele]
"""

from setuptools import find_packages, setup


def read_long_description() -> str:
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="telemorph",
    version="1.0.0",
    description=(
        "Unified Telegram session conversion library — wraps TGConvertor "
        "and opentele2 into a single, easy-to-use API."
    ),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="TeleMorph Team",
    author_email="team@telemorph.dev",
    url="https://github.com/telemorph/telemorph",
    license="MIT",
    packages=find_packages(exclude=["examples", "examples.*", "tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=[
        "asyncio",
        "aiosqlite>=0.18.0",
    ],
    extras_require={
        "telethon": ["telethon>=1.34.0"],
        "pyrogram": ["pyrogram>=2.0.106"],
        "kurigram": ["kurigram>=2.0.4"],
        "opentele": ["opentele>=1.27.0"],
        "all": [
            "telethon>=1.34.0",
            "pyrogram>=2.0.106",
            "kurigram>=2.0.4",
            "opentele>=1.27.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    keywords="telegram telethon pyrogram kurigram tdata session converter opentele",
    entry_points={
        "console_scripts": [
            "telemorph=telemorph.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)