#  ***[python_flask_selenium_stock_price_api](https://github.com/adrianopaduam/python_flask_selenium_stock_price_api)***
A flask-driven restful API for stock market information scrapping


## Technologies used
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Selenium](https://selenium-python.readthedocs.io/)** - A simple API to write functional/acceptance tests using Selenium WebDriver
* **[Docker](https://www.docker.com/)** - The fastest way to containerize applications
* **[Gunicorn](https://gunicorn.org/)** - 'Green Unicorn' is a Python WSGI HTTP Server for UNIX
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Local Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd python_flask_selenium_stock_price_api
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ python -m venv venv
        $ ./venvScripts/activate
        ```

* #### Environment Variables
    Create a .env file on the root folder and add the same information appointed on .env-example file (You can twak it as much as you like)

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

* #### Running API Locally
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ python manage.py
    ```
    You can now call the API by using
    ```
    http://localhost:8000/stocks?region=Argentina
    ```


## Docker Installation / Usage
Another option is to install docker using these instructions [here](https://www.docker.com/products/docker-desktop) and build the API as a container.

* #### Environment Variables
    Create a .env file on the root folder and add the same information appointed on .env-example file (You can twak it as much as you like)

* #### Building Docker Container
    On your terminal, generate the container using the command:
    ```
    docker build -t python_flask_selenium_stock_price_api
    ```

* #### Running API as Docker Container
    Start the container using the following
    ```
    docker run -p 8000:8000 python_flask_selenium_stock_price_api:latest
    ```
    You can now call the API by using
    ```
    http://localhost:8000/stocks?region=Argentina
    ```
