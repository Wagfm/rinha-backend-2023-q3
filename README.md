# Python - Flask API

This server does **~40k** inserts of **~46.5k** in the stress test from the event "Rinha de backend 2023 q3". The
project is not suitable for production deployment, since it's a competition focused code.

# Instructions

To start the server, run:

```shell
git clone git@github.com:Wagfm/rinha-backend-2023-q3.git
cd rinha-backend-2023-q3
docker compose up

```

This will start a Flask based HTTP server in http://localhost:9999, as the event required. The stress test results are
located in the "results" folder, more specifically in the "results/index.html" file.

To run the stress test:

```shell
git clone git@github.com:zanfranceschi/rinha-de-backend-2023-q3.git
cd rinha-de-backend-2023-q3
cd teste/gatling
sh install-gatling
cd ../../stress-test
vim run-test.sh
asdf local java openjdk-17 # set jdk version to 17 in your machine with the right manager
# change location for the downloaded gatling/bin folder in run-test.sh file
./run-test.sh
```

---

> :warning: This was made **AFTER** the event ended and must **NOT** be compared to the real competitors performance. It
> was made just as a learning experience for topics like Docker, HTTP Servers, Web Applications and SQL Databases.
