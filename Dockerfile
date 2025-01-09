FROM python:3.13-slim


#sec context
RUN groupadd --gid 1001 access_verifier && \
    useradd --uid 1001 --gid 1001 --create-home access_verifier


WORKDIR /usr/src
COPY app/ /usr/src/app/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
RUN chown -R access_verifier:access_verifier /usr/src
USER access_verifier

ENTRYPOINT [ "uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "8000" ]