FROM mongo:latest

WORKDIR /app

# Copy data into container
COPY . .

# Import data into MongoDB
# Run the import command and exit
# RUN mongoimport --host mongodb-database --db las --collection users --type json --file users.json --jsonArray
CMD ["sh", "-c", "mongoimport --host mongodb-database --db las --collection books --type json --file books.json --jsonArray && mongoimport --host mongodb-database --db las --collection users --type json --file users.json --jsonArray && exit 0"]

