from setuptools import setup, find_packages
setup(
    name="voice-analyzer",
    version="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["voice-analyzer=voice_analyzer.cli:cli"]},
    install_requires=["faster-whisper", "python-telegram-bot", "requests", "click"],
)
