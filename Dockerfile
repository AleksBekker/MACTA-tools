ARG PYTHON_VERSION

# Specify image dynamically
FROM python:$PYTHON_VERSION

# HAS to be below the `FROM`
ARG EXTRAS

ADD . /package
RUN python -m pip install "/package$EXTRAS"

# Run macta-tools
ENTRYPOINT ["macta-tools"]
