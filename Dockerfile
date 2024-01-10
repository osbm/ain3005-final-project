FROM mongo:4.4.26


RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY . /app
WORKDIR /app


# mongoimport the data.json file into the mongo container

CMD mongoimport --host mongodb --db test --collection restaurants --type json --file data.json --jsonArray




RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

