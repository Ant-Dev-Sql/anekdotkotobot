FROM python:3.13
WORKDIR /pythonprojects/anekdotbombot
COPY requirements.txt ./
COPY anekdotkidbot.py ./
COPY test_for_docker.py ./
COPY adult_anekdot.json ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install mc -y
RUN apt-get install unixodbc-dev -y

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
# RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get clean && apt-get update

# RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
# RUN curl -sSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# RUN apt-get install msodbcsql17 -y
CMD ["python", "anekdotkidbot.py"]