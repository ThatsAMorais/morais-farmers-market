FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY client/requirements.txt /requirements.txt
RUN pip3 install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY ./client /app
WORKDIR /app
CMD ["python", "the-farmers-market.py"]
