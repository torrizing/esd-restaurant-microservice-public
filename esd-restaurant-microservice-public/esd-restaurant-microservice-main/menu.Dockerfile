FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./menu.py ./db_creds.py ./
CMD [ "python", "./menu.py" ]
