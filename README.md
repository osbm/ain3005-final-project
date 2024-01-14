
# AIN3005 - Advanced Python Programming - Final Project


The goal of this project is to implement a Library Automation System (LAS) using Flask as the web framework, MongoDB as the database, and Apache Kafka for messaging. The LAS will provide various services, including book lending, reservation, and search functionality.

Requirements:

- Flask Web Application: Implement a REST API to serve requirements you analyzed in the first homework for the Library Automation System.
- MongoDB Integration: Use MongoDB to store and manage data related to books, users, borrowing records, fines, and reservations.
- Apache Kafka Messaging: Integrate Apache Kafka for communication between different components of the LAS, ensuring reliable and scalable messaging.
- User Authentication and Authorization: Implement a user authentication system with roles (students, faculty members, staff, and graduates) to control access to LAS services. Implement JWT for secure user authentication and authorization. Each request to LAS services should be validated using JWT.


Notes:

- Include comprehensive documentation explaining the system architecture, database schema, and API endpoints.
- Clearly specify all dependencies and include a setup guide for easy replication of the environment.
- Provide a set of test cases to ensure the functionality of key features.



# Installation Guide

## Prerequisites

You need to install docker and docker-compose to run the application. You can find the installation guide for your operating system on the official docker website: https://docs.docker.com/get-docker/

## Running the application

To run the application, you need to clone the repository and run the following command in the root directory of the project:

```bash
docker compose up
```

This is it. This command will build the images and run the containers. You can access the application on http://localhost:8000

# Infrastructure

The application consists of 6 services:
- **mongo**: MongoDB database to store the data
- **mongodb-import-data**: This container is run once to import the data into the database using mongoimport. It is not needed after the data is imported.
- **kafka**: Apache Kafka messaging system to communicate between services
- **zookeeper**: This is needed for Kafka to work
- **flask-app**: Flask application that serves the API endpoints
- **kafta-consumer**: Kafka consumer that listens to the messages from the flask-app and streams them to log files then you can access it in the `kafka-consumer/output`  folder.

The mongo, kafka, and zookeeper services are taken from the official docker hub images. The flask-app and kafka-consumer images are built from the Dockerfiles in the `flask-app` and `kafka-consumer` folders respectively. The mongodb-import-data image is built from the Dockerfile in the `mongodb-import-data` folder.

# Database Schema

The database consists of 4 collections:

- **books**: This collection stores the information about the books. Following is the first document:

```json
{
    "isbn": "0596159900",
    "title": "Head First HTML and CSS",
    "year": 2012,
    "price": 26.78,
    "page": 768,
    "category": "IT",
    "coverPhoto": "images/head.first.html.and.css.png",
    "publisher": "O'Reilly",
    "author": "Elisabeth Robson, Eric Freeman",
    "status": "reserved",
    "current_occupant_username": "osman",
    "last_update_date": "2017-01-01",
    "deadline": "2024-01-26"
}
```

- **users**: This collection stores the information about the users. Following is the first document:

```json
{
    "name": "admin",
    "surname": "admin",
    "username": "admin",
    "password": "admin",
    "birthday": "01.01.2001",
    "email": "admin@admin.com",
    "user_type": "admin",
    "current_balance": 120000
}
```

- **fines**: This collection stores the information about the fines. Following is the first document:

```json
{
    "fine_date": "2019-01-01",
    "fine_id": 1,
    "username": "meg",
    "fine_amount": 100,
    "reason": "late return"
}
```

# Enjoy!

I also added some html and css to make the application look better. I hope you enjoy it!

