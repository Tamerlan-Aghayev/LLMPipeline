from setuptools import setup, find_packages

setup(
    name="llm_pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.0.26,<8.1",
        "sentence-transformers>=2.2.2,<3.0",
        "openai>=1.0.0,<2.0",
        "pyyaml>=5.4.1,<6.0",
        "torch>=1.9.0,<2.0",
    ],
    python_requires='>=3.7',
)