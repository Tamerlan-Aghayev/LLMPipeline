from setuptools import setup, find_packages

setup(
    name="llm_pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python==9.0.0",
        "google-generativeai==0.7.2",
        "python-dotenv==1.0.1",
        "sentence-transformers==3.0.1",
        "torch==2.4.0",
        "streamlit==1.25.0",
    ],
    python_requires='>=3.7',
)