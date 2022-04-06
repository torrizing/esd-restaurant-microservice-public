FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt stripe.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r amqp.reqs.txt -r stripe.reqs.txt
COPY ./place_an_order.py ./invokes.py ./amqp_setup.py ./
COPY ./templates/test.html ./templates/test.html
CMD [ "python", "./place_an_order.py" ]