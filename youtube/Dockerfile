FROM python:2.7
WORKDIR /youtube_search
COPY ./requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./ ./
EXPOSE 8890
ENV PYTHONPATH /youtube_search
CMD python /youtube_search/youtube_search/engine/core.py