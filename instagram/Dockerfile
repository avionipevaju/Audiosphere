FROM python:2.7
WORKDIR /insta_feed
COPY ./requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./ ./
EXPOSE 8892
ENV PYTHONPATH /insta_feed
CMD python /insta_feed/insta_feed/routing/core.py