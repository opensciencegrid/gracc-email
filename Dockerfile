FROM opensciencegrid/software-base:23-el9-release
RUN dnf update -y
RUN dnf install -y python3-gfal2 gfal2-plugin-gridftp
COPY src/* /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "report.py"]