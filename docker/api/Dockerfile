FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY api/requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY ./api/src /app
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD ["api.py"]
