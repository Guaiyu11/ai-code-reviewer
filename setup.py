from setuptools import setup, find_packages
setup(
    name="ai-code-reviewer",
    version="1.0.0",
    description="A curated collection of Python CLI productivity tools for developers",
    author="yyu995",
    url="https://github.com/Guaiyu11/ai-code-reviewer",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["requests", "beautifulsoup4"],
)
