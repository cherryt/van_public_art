# Van Public Art

This is a project which utilizes the data catalogue of artwork found in public areas in the city of Vancouver. Artwork can be displayed by artists or neighbourhood, and can be filtered by keywords.

## Running the Project

Create and activate the virtual environment

```bash
$ virtualenv venv
$ source venv/script/activate
```

Install Python dependencies

```bash
$ pip install -r requirements.txt
```

Navigate to '/static' and install JavaScript dependencies

```bash
cd van_public_art/static
npm install
```

Environment variables for database connection should be set in the .env file. Once this is done, navigate back to the root and run the project 


```bash
$ python run.py
```

## Running Tests

Install testing dependencies and run tests
```bash
$ pip install -r test-requirements.txt

$ pytest
```