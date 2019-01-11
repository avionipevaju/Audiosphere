FROM python:2.7
WORKDIR /moody
COPY /requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./ ./
EXPOSE 8887
ENV PYTHONPATH /moody
CMD python /moody/moody_py/engine/core.py