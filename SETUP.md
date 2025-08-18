# Setup and Deployment

## Libraries and Services Required

- [Flask](https://flask.palletsprojects.com)
- [Jinja2](https://jinja.palletsprojects.com/templates/)
- [PicoCSS](https://picocss.com/)


---

## Setting up a Development Environment

To develop locally, you need to setup a **Python virtual environment (venv)** to keep your Python configuration isolated from the rest of your system.

### VS Code Extensions

To support setting up and developing with the Flask server, add the following extensions to VS Code:

- **Python** (from Microsoft)
- **Better Jinja** (from Samuel Colvin)

You should also have the following (just to n=make life better):

- **Code Spell Checker** (because speeling is hard!)
- **Error Lens** (places error messages inline, next to code)


### Create the Virtual Environment

1. In your terminal, navigate to the project root folder

2. **Create** the virtual environment with:

    ```
    python -m venv venv
    ```

2. **Activate** the virtual environment

    *Note: If using __VS Code__'s terminal, VS Code will offer to use / activate the virtual environment for you - select __Yes__, and then relaunch the terminal. If you do this, there is no need for the following command.*

    Windows PowerShell:

    ```
    .\venv\Scripts\activate
    ```

    Linux:

    ```
    source venv/bin/activate
    ```

3. **Install** all required Python libraries:

    ```
    pip install -r requirements.txt
    ```

### Using a Previously Created Virtual Environment

If you are returning to your project, you do not need to recreate your virtual environment, just activate and update it.

*Note: If using __VS Code__ as mentioned above, VS Code will __automatically__ activate the environment as time you open its Terminal, and you don't need to do anything.*


### Launching the Server Locally

The Flask project is configured as a module called **app** (with main code in **\_\_init__.py**), which allows the the server to be run very easily with:

```
flask run --debug
```

The server should start and will present a URL link, usually 127.0.0.1:5000


