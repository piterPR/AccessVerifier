## Structure of repository
.github -> pipelines for pylint checker
app -> 


# App
To run app locally, choose one of two ways (using venv or docker)

Using venv: 
```
python3 -m venv venv
source venv/bin/activate
uvicorn app.main:app --reload
```
Using dockerfile:
```
podman build -t acces_verifier . && \
podman run --name acces_verifier -p 8000:8000 \
-v /path/to/your/local/app:/usr/src/app/app:Z \
-v /path/to/requirements.txt:/usr/src/app/requirements.txt:Z \
acces_verifier```
```

Test and verify endpoint using curl

```
curl --location 'localhost:8000/verify' \
--header 'Content-Type: text/plain' \
--data 'x-forwarded-for: 3.248.180.68
User-Agent: CustomClient/1.0
Host: example.com
X-Custom-Header: TestHeader'
```

