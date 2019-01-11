FROM python:2.7
WORKDIR /weather
COPY /requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./ ./
EXPOSE 8889
ENV PYTHONPATH /weather
CMD python /weather/yahoo_weather/core/core.py