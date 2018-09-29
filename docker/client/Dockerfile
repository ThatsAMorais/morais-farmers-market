FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY client/requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY ./client/src /app
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD ["the-farmers-market.py", "api"]
