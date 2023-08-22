# Flask App with User Registration, Search, and Sorting
This repository contains a Flask app that allows users to register using the POST method and search for listings using the GET method. Users can search by title, amenities, price, and location, and the search results can be sorted by price. The app also implements JWT token-based authentication for user login and registration. PostgreSQL is used for user management, and Elasticsearch is used for efficient search queries. Both databases are containerized using Docker. The required Python libraries are listed in the `requirements.txt` file.


## Features
  - User Registration and Login using JWT Tokens
  - User data stored in PostgreSQL
  - Listing data stored in Elasticsearch for efficient searching
  - Search listings by title, amenities, price, and location
  - Sort search results by price

## Prerequisites
  - Docker
  - Python
  - Flask
  - PostgreSQL / PGAdmin
  - Elasticsearch / Kibana




## Setup

#### 1. Clone this repository:

   ```bash
   git clone https://github.com/FahimHaider19/W3Engineers-Flask-Task.git
   cd W3Engineers-Flask-Task
   ```

#### 2. Database Setup using Docker Compose

#### PostgreSQL Setup

- Create a new file named `docker-compose-postgres.yml`.

- Copy and paste the following content into the `docker-compose-postgres.yml` file:

   ```yaml
   version: "3.8"
   services:
     db:
       image: postgres
       container_name: postgres
       restart: always
       ports:
         - "5432:5432"
       environment:
         POSTGRES_USER: user-name
         POSTGRES_PASSWORD: strong-password
       volumes:
         - local_pgdata:/var/lib/postgresql/data
     pgadmin:
       image: dpage/pgadmin4
       container_name: pgadmin4_container
       restart: always
       ports:
         - "8888:80"
       environment:
         PGADMIN_DEFAULT_EMAIL: user-name@domain-name.com
         PGADMIN_DEFAULT_PASSWORD: strong-password
       volumes:
         - pgadmin-data:/var/lib/pgadmin

   volumes:
     local_pgdata:
     pgadmin-data:
   ```

- Open a terminal window and navigate to the folder where you placed the `docker-compose-postgres.yml` file.

- Run the following command to start the PostgreSQL and pgAdmin containers:
```
docker-compose -f docker-compose-postgres.yml up -d
```
- PostgreSQL will be available on port `5432`, and pgAdmin will be available on port `8888`.


#### Elasticsearch and Kibana Setup
   - Create a new file named docker-compose-elasticsearch.yml.

   - Copy and paste the following content into the `docker-compose-elasticsearch.yml` file:

   ```yaml
   version: "3.7"
   services:
   elasticsearch:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
      container_name: elasticsearch
      restart: always
      environment:
         - xpack.security.enabled=false
         - discovery.type=single-node
         - ES_JAVA_OPTS=-Xmx2g -Xms2g
      ulimits:
         memlock:
         soft: -1
         hard: -1
         nofile:
         soft: 65536
         hard: 65536
      cap_add:
         - IPC_LOCK
      ports:
         - 9200:9200
   kibana:
      container_name: kibana
      image: docker.elastic.co/kibana/kibana:8.9.0
      restart: always
      environment:
         - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      ports:
         - 5601:5601
      depends_on:
         - elasticsearch
   ```

   - Open a terminal window and navigate to the folder where you placed the docker-compose-elasticsearch.yml file.

   - Run the following command to start the Elasticsearch and Kibana containers:

```
docker-compose -f docker-compose-elasticsearch.yml up -d
```
   - Elasticsearch will be available on port 9200, and Kibana will be available on port 5601.

   - Make sure you have Docker and Docker Compose installed before running the above commands. These instructions assume that you are in the same directory as the Docker Compose files when running the commands. Once the containers are up and running, you can proceed with setting up your Flask app to interact with the PostgreSQL and Elasticsearch databases.


## Elasticsearch Seed

This document provides example data and queries to seed Elasticsearch with property listings and perform searches.

## Seed Data - Bulk Insert

Run the following `POST` request to bulk insert property listings:

```json
put properties


post /properties/_bulk
{ "index": {} }
{ "title": "Luxury Apartment", "amenities": ["pool", "gym", "wifi"], "price": 4500, "location": "New York, NY" }
{ "index": {} }
{ "title": "Cozy Studio", "amenities": ["wifi"], "price": 800, "location": "New York, NY" }
{ "index": {} }
{ "title": "Spacious Loft", "amenities": ["gym", "wifi"], "price": 3200, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Urban Condo", "amenities": ["pool"], "price": 2800, "location": "Queens, NY" }
{ "index": {} }
{ "title": "Downtown Retreat", "amenities": ["pool", "gym"], "price": 3800, "location": "New York, NY" }
{ "index": {} }
{ "title": "Modern Penthouse", "amenities": ["pool", "wifi"], "price": 5000, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Charming Duplex", "amenities": ["gym"], "price": 2200, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Cosmopolitan Living", "amenities": ["pool", "wifi"], "price": 4200, "location": "Queens, NY" }
{ "index": {} }
{ "title": "Rooftop Oasis", "amenities": ["pool", "gym", "wifi"], "price": 4700, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Sleek Studio", "amenities": ["wifi"], "price": 950, "location": "Bronx, NY" }
{ "index": {} }
{ "title": "Elegant Condo", "amenities": ["pool", "wifi"], "price": 3800, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Artist's Loft", "amenities": ["gym"], "price": 2600, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Central Park View", "amenities": ["pool", "wifi"], "price": 4900, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Quaint Hideaway", "amenities": ["wifi"], "price": 700, "location": "Staten Island, NY" }
{ "index": {} }
{ "title": "Luxury Condo", "amenities": ["pool", "gym", "wifi"], "price": 4800, "location": "Queens, NY" }
{ "index": {} }
{ "title": "Chic Apartment", "amenities": ["wifi"], "price": 1200, "location": "Bronx, NY" }
{ "index": {} }
{ "title": "Downtown View", "amenities": ["gym", "wifi"], "price": 3500, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "City Escape", "amenities": ["pool"], "price": 2900, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Modern Studio", "amenities": ["wifi"], "price": 1100, "location": "Bronx, NY" }
{ "index": {} }
{ "title": "Penthouse Retreat", "amenities": ["pool", "wifi"], "price": 5300, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Artsy Apartment", "amenities": ["gym"], "price": 2400, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Riverside Living", "amenities": ["wifi"], "price": 1300, "location": "Queens, NY" }
{ "index": {} }
{ "title": "Sky High Condo", "amenities": ["pool", "gym", "wifi"], "price": 5100, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Coastal Getaway", "amenities": ["wifi"], "price": 900, "location": "Staten Island, NY" }
{ "index": {} }
{ "title": "Urban Retreat", "amenities": ["gym"], "price": 2700, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Cityscape View", "amenities": ["pool", "wifi"], "price": 4600, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Studio Haven", "amenities": ["wifi"], "price": 1000, "location": "Bronx, NY" }
{ "index": {} }
{ "title": "Luxury Loft", "amenities": ["gym"], "price": 3300, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "City Lights Condo", "amenities": ["pool", "wifi"], "price": 4700, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Serene Hideout", "amenities": ["wifi"], "price": 750, "location": "Staten Island, NY" }
{ "index": {} }
{ "title": "Modern Urban Living", "amenities": ["pool", "gym", "wifi"], "price": 4900, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Metropolitan Studio", "amenities": ["wifi"], "price": 1150, "location": "Bronx, NY" }
{ "index": {} }
{ "title": "Industrial Loft", "amenities": ["gym"], "price": 2500, "location": "Brooklyn, NY" }
{ "index": {} }
{ "title": "Central Oasis", "amenities": ["pool", "wifi"], "price": 4400, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Rural Escape", "amenities": ["wifi"], "price": 650, "location": "Staten Island, NY" }
{ "index": {} }
{ "title": "Modern Chic Condo", "amenities": ["gym"], "price": 3000, "location": "Queens, NY" }
{ "index": {} }
{ "title": "Downtown Haven", "amenities": ["pool", "wifi"], "price": 4200, "location": "Manhattan, NY" }
{ "index": {} }
{ "title": "Seaside Retreat", "amenities": ["wifi"], "price": 850, "location": "Staten Island, NY" }
{ "index": {} }
{ "title": "Modern Luxury", "amenities": ["pool", "gym"], "price": 4700, "location": "Brooklyn, NY" }
```

#### 3. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```
   

## Usage

#### 1. Access the app through your browser or API client at http://localhost:5000.

#### 2. **User Registration and Login**:
   - Register a new user using the `POST` method to `/register` with username and password in the request body.
   - Obtain a JWT token by logging in using the `POST` method to `/login` with the same credentials.

#### 3. **Search Listings**:
   - Use the `GET` method to `/search` for listing search.
   - Include query parameters for search criteria:
     - `title`: Search by title
     - `amenities`: Search by amenities
     - `price`: Search by price range
     - `location`: Search by location
     - `sort`: Sort by price (use asc or desc)

## API Endpoints

- `POST /register`: Register a new user with username and password.
- `POST /login`: Obtain a JWT token by logging in with username and password.
- `GET /search`: Search listings with various query parameters and sorting.
