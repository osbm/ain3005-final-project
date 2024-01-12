FROM mongo:latest

WORKDIR /app

# Copy data into container
COPY . .

# Import data into MongoDB
# Run the import command and exit

CMD ["sh", "-c", "./mongoimport-run.sh && exit 0"]

