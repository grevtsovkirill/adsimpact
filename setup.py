from setuptools import setup

with open("requirements.txt") as f:
    requirements = [line for line in f if not line.startswith("#")]
    
setup(
    name='adsimpact',
    version="0.1",
    author="Kirill Grevtsov",
    author_email="grevtsovkirill@gmail.com",
    description="build a model for predicting the quantities of sold products",
    packages=["adsimpact"],
    entry_points={
        "console_scripts": ["adsimpact = adsimpact.__main__:main"]},
    install_requires=requirements,
)
