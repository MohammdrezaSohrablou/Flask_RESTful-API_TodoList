# Flask_RESTful-API_TodoList
A simple Flask project for managing tasks using SQL Server and JWT.

Features
  Uses SQL Server as the database (CRUD)
  Authentication/Authorization using JWT
  Advanced Exception/Error Handling
  RESTful API design with Flask

Requirements packages 
  Flask
  flask-jwt-extended
  pyodbc
  werkzeug

Endpoints
  Register a new user
    Request
      POST /register HTTP/1.1
      Host: localhost:5000
      Content-Type: application/json
      
      {
        "username": "mamareza",
        "password": "123456789",
        "email": "mamareza@example.com",
        "phone": "09120000000"
      }
    Response (201 Created)
    
      {
        "msg": "User registered successfully.",
        "user_id": 1
      }
  
  Login and receive JWT
    Request
      POST /login HTTP/1.1
      Host: localhost:5000
      Content-Type: application/json
      
      {
        "username": "mamareza",
        "password": "123456789"
      }
    Response (200 OK)
    
      {
        "access_token": "<YOUR_JWT_TOKEN>"
      }
  
  Create a new task
    Request
      POST /tasks HTTP/1.1
      Host: localhost:5000
      Content-Type: application/json
      Authorization: Bearer <YOUR_JWT_TOKEN>
      
      {
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs"
      }
    Response (201 Created)
    
      {
        "message": "Task created successfully"
      }
      
  Get all tasks
    Request
    
      GET /tasks HTTP/1.1
      Host: localhost:5000
      Authorization: Bearer <YOUR_JWT_TOKEN>
    Response (200 OK)
    
      { "id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs" },
      { "id": 2, "title": "Homeworks", "description": "Math, Chemistry, Physics" }
  
  Get task by ID
    Request
    
      GET /tasks/{id} HTTP/1.1
      Host: localhost:5000
      Authorization: Bearer <YOUR_JWT_TOKEN>
  
    Response (200 OK)
      
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs"
      }
      
  Update task by ID
    Request
  
      PUT /tasks/{id} HTTP/1.1
      Host: localhost:5000
      Content-Type: application/json
      Authorization: Bearer <YOUR_JWT_TOKEN>
      
      {
        "title": "Updated title",
        "description": "Updated description"
      }
  
    Response (200 OK)
    
      {
        "message": "Task updated successfully."
      }
        
  Delete task by ID
    Request
    
      DELETE /tasks/1 HTTP/1.1
      Host: localhost:5000
      Authorization: Bearer <YOUR_JWT_TOKEN>
  
    Response (200 OK)
    
      {
      "message": "Task deleted successfully."
      }
