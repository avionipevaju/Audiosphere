FROM python:2.7
WORKDIR /discogs_py
COPY ./requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./ ./
EXPOSE 8891
ENV PYTHONPATH /discogs_py
CMD python /discogs_py/discogs_py/engine/core.py