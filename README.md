# Setting Up the Project

### Clone the Repository:

```bash
git clone https://github.com/YazanSneneh/games_store.git
cd game_store
```
### Setting up manually
#### Create & run virtualenv
```bash
pip install virtualenv   # if virtualenv not installed on your machine
virtualenv -p python env
. env/bin/activate  # Linux/Mac
. env\Scripts\activate     # Windows
```
#### create a Database to store data

#### create `.env` file:
- refer to **.env.example** how to create your .env variables.
- additionally: the response email will contain the secrets to create JWT.

**optionally use docker**
Run the application using docker (Make sure you have Docker and docker compose on your machine):

```bash
docker-compose up -d --build
```

- **Go to Postman to or continue manually**

#### install dependencies
`pip install -r requirements.txt`

#### migrations:
```bash
./mange.py makemigrations
./mange.py migrate
```
**Note: if you encounter issue with migrations explicitly migrate store and core apps**
```bash
./mange.py makemigrations core store
./mange.py migrate
```

#### create customer:
` ./manage.py create_customer`

####  import games:
` ./manage.py import_games`

## Use Pytest to run unit test
To test everything is okay and working as expected Make sure your virtual environment is activated.

**Run Command in terminal:**
``` bash
pytest -v
```

### Using Postman to test the API
# Postman Collection

You can test the API using the Postman collection and environment files included in this project.
- Collection file: [`postman/GameStore.postman_collection.json`](postman/GameStore.postman_collection.json)
- Environment file: [`postman/GameStore.postman_environment.json`](postman/GameStore.postman_environment.json)

### Usage:
1. Open Postman.
2. Import the collection and environment files.
3. Select the imported environment from the top right.
4. You’re good to go!
**Note: if you want to add Authorization key manually in API you need to prefix it with Bearer unless you use Authorization tab(my collection) Postman might prefix it automatically before sending request**

**Note: Make sure the backend is running before sending requests.**

## Manually create endpoints
#### Authentication
POST /auth/login/
Description: Authenticate user and return JWT token
Request Body:
``` json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

### Store
**GET /games/**

Headers:
```json
Authorization: Bearer <auth_token>
```
Request Body:
``` json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**GET /games/**

Headers:
```json
Authorization: Bearer <auth_token>
```
Query Parameters:
``` json
?page=1&page_size=5
```

Response Example:
```json
{
  "count": 300,
  "total_pages": 60,
  "current_page": 3,
  "results": [
    {
      "id": 11,
      "title": "Sword of Valor",
      "description": "A legendary sword with magical powers",
      "price": 155.0,
      "location": "JO",
      "created_at": "2025-04-18T20:24:58.577587Z",
      "updated_at": "2025-04-18T20:24:58.577600Z"
    }
    // ...other games
  ]
}

```

**GET games/{id}/**
Headers:
```json
Authorization: Bearer <auth_token>
```
Response Example:

```json
{
  "id": 11,
  "title": "Sword of Valor",
  "description": "A legendary sword with magical powers",
  "price": 155.0,
  "location": "JO",
  "created_at": "2025-04-18T20:24:58.577587Z",
  "updated_at": "2025-04-18T20:24:58.577600Z"
}
```
**POST /purchase/**

Headers:
```json
Authorization: Bearer <auth_token>
Content-Type: application/json
```

Request body:
```json
{
  "game_id": 3
}
```

Response Example:
```json
{
  "message": "Purchase successful",
  "order": {
    "id": 1,
    "game": {
      "id": 3,
      "title": "Potion of Healing",
      "description": "Restores health completely over 5 seconds",
      "price": 20.0,
      "location": "JO",
      "created_at": "2025-04-18T20:24:58.537010Z",
      "updated_at": "2025-04-18T20:24:58.537027Z"
    },
    "total_price": "20.00",
    "purchase_date": "2025-04-18T20:25:47.775636Z"
  }
}

```

**GET /orders/**

Headers:
```json
Authorization: Bearer <auth_token>
```
Response:
``` json
[
    {
        "id": 1,
        "game": {
            "id": 3,
            "title": "Potion of Healing",
            "price": 20.0
        },
        "total_price": "20.00",
        "purchase_date": "2025-04-18T20:25:47.775636Z"
    }
    // ...other orders
]
```