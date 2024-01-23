FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11-bullseye

RUN apt-get update && apt-get install ffmpeg -y