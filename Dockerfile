FROM python:3.9-buster

WORKDIR /app
# Double Check comments / Fixed for Demo
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#RUN touch k3s-context.yaml

COPY . .

#CMD [ "python3", "/app/main.py"]
CMD ["python3","-u","/app/main.py"]


# docker buildx build --platform linux/amd64,linux/arm64 --push -t hughbrien/komo_rbac_ns_updater:0.0.1 .