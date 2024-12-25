# TrailService Microservice - part of the Trail Application

This project is a Python-based microservice that manages trail information for the **Trail Application**, a well-being trail application designed to encourage outdoor exploration and enhance personal well-being. The microservice provides full CRUD (Create, Read, Update, Delete) functionality for trails and interacts with an external **Authenticator API** for secure authentication.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [API Documentation](#api-documentation)

---

## Overview

The **TrailService** is a core component of the Trail App, a platform that motivates users to explore specific areas by providing well-documented trails. Users can view trail details, while administrators can manage trail data.

The product vision is:
> For people who wish to enjoy the outdoors, to enhance their wellbeing and to have a reason to explore a particular area, the Trail App is a full trail management application providing a reason to explore a given area.

This microservice is built with Python (Flask) and includes Swagger documentation for easy API interaction.

---

## Features

### For Administrators:
- Create new trails with detailed information
- Edit existing trail information
- View and verify the existence of trails
- Delete trails

### For Users:
- Retrieve detailed trail information to be displayed in an Android mobile application

### Additional Features:
- Integration with **Authenticator API** for secure authentication
- SQL Server database for trail data storage
- Swagger UI for API testing and documentation

---

## Technologies

- **Backend Framework:** Python, Flask
- **Database:** SQL Server
- **API Documentation:** Swagger (OpenAPI)
- **Authentication:** Authenticator API

---

## Setup and Installation

### Prerequisites:
- Python 3.x installed on your machine
- University of Plymouth VPN connection

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dennisnpc/COMP2001-CW2.git
   cd trailmicroservice

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

4. **Run**:
    ```bash
    python app.py

---

## API Documentation

The API endpoints for the TrailService are fully documented using Swagger. The endpoints include:

- **GET /trails**: Retrieve details of a list of trails.
- **GET /trails/{trail_id}**: Retrieve details of a specific trail.
- **POST /trails**: Create a new trail.
- **PUT /trails/{trail_id}**: Update details of an existing trail.
- **DELETE /trails/{trail_id}**: Remove a trail.

Detailed documentation is available at [Swagger UI](http://localhost:8000/api/v1/ui).
