# URL SHORTENER


This repository contains a URL shortening API developed using the **FastAPI** framework in Python. The API allows users to shorten long URLs and generate shorter aliases. It serves as a proof-of-concept for building RESTful APIs with FastAPI.

The key features are:

- **URL shortening functionality** - Long URLs can be shortened to shorter aliases which are easier to remember and share.

- **Persistent storage** - The URL mappings are persisted in a SQLite database to retain the shortened URLs even after the API restarts.

- **Configurability** - The database connection string and other settings can be configured through config files.

To use the API, simply send a POST request to the /url endpoint with the long URL in the request body. The API will respond with a JSON containing the shortened alias. The shortened URLs can then be accessed through the /{alias} endpoint.

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Bootstrap(Still under development)
