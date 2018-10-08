FROM python:3.7 as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY products/requirements.txt /requirements.txt
RUN pip3 install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY ./products /app
WORKDIR /app
CMD ["python", "app.py"]
