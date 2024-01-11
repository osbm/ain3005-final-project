FROM mongo:latest

COPY data.json /data.json

# Import data into MongoDB
# Run the import command and exit
CMD ["sh", "-c", "mongoimport --host mongodb-database --db test --collection restaurants --type json --file data.json --jsonArray && exit 0"]



