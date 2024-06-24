### Hexlet tests and linter status:
[![Actions Status](https://github.com/lt3-me/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lt3-me/python-project-52/actions)
[![Github Actions Status](https://github.com/lt3-me/python-project-52/workflows/Python%20CI/badge.svg)](https://github.com/lt3-me/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/1271fd58ac4d36fbd901/maintainability)](https://codeclimate.com/github/lt3-me/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1271fd58ac4d36fbd901/test_coverage)](https://codeclimate.com/github/lt3-me/python-project-52/test_coverage)

# Task Manager

https://task-manager-ubxr.onrender.com/

## Overview

This is a task management web app built with Python and Django. It allows users to create tasks, assign them, and track their statuses. If you want to access a demo version of this app hosted on [Render](https://render.com/), please visit [this page](https://task-manager-ubxr.onrender.com/).

### Features

- **Task Management**: Create, assign performers, update statuses.
- **Labels**: Categorize tasks with multiple labels.
- **Filtering**: Easily find tasks by status, performer, or label.
- **User Authentication**: Secure access with registration and login.

### Technology Stack

- **Backend**: [Python](https://python.org), [Django](https://djangoproject.com), [PostgreSQL](https://postgresql.org)
- **Frontend**: [Bootstrap 5](https://getbootstrap.com/)
- **Deployment**: [Gunicorn](https://gunicorn.org/)
- **Tools**: [Poetry](https://python-poetry.org/), [Rollbar](https://rollbar.com/) for error monitoring

### Available Actions

- **Registration**: Begin by registering on the application using the [registration form](https://task-manager-ubxr.onrender.com/users/create/).
- **Authentication**: After registration, log in [here](https://task-manager-ubxr.onrender.com/login/) to access the list of tasks and create new ones.
- **Users**: You can view all registered users on the [users page](https://task-manager-ubxr.onrender.com/users/). You can edit your own information or delete your profile if you're authorized. Deleting another user or a user associated with any tasks is restricted.
- **Statuses**: Once logged in, you can manage task statuses — adding, updating, or deleting them. Statuses linked to any tasks cannot be deleted.
- **Tasks**: After logging in, you can view, add, and update tasks. Only the creator of a task can delete it. Tasks can be filtered by statuses, users, and labels on the tasks page.
- **Labels**: When logged in, you have control over task labels—adding, updating, or deleting them. Labels linked to any tasks cannot be deleted.

## Installation

Follow these steps to install the application using Poetry:

### Prerequisites

Ensure you have the following installed on your system:

- [Python](https://www.python.org/downloads/) (version 3.10 or later)
- [Poetry](https://python-poetry.org/docs/#installation) (a dependency management tool for Python)
- [PostgreSQL](https://www.postgresql.org/download/) *(optional)*

>*Alternatively, you can use SQLite database by setting `DATABASE_URL = sqlite:///db.sqlite3` in .env file.*

### Steps

1. **Clone the Repository**

Open your terminal and run the following command to clone the repository:

```bash
>>$ git clone https://github.com/lt3-me/python-project-52
```

2. **Navigate to the Project Directory**

Change into the project directory:

```bash
>>$ cd python-project-52
```

3. **Install Dependencies**

Run the following command to install all necessary dependencies using Poetry:

```bash
>>$ poetry install
```

Or using Makefile:

```bash
>>$ make build
```

4. **Get Rollbar Token (optional)**

[Sign up](https://rollbar.com/signup/) on Rollbar and create a new project.

To track errors you simply need to add an access your Project Access Token for post_server_item to your .env (you can find it in project settings).

5. **Create .env File**

Create .env file in the root folder and add following variables:

```bash
DATABASE_URL = 'postgresql://...' # url of your database
# (if you don't want to use PostgreSQL, just use 'sqlite:///db.sqlite3')
SECRET_KEY= '...' # your secret key
LANGUAGE= 'en' # project locale (optional)
ROLLBAR_TOKEN = '...' # rollbar token for errors tracking (optional)
```

## Running the Application

You can start the application with the appropriate command using Gunicorn WSGI:

```bash
>>$ make start
```

Alternatively, you can start the app using standard Django development server:

```bash
>>$ make dev
```
