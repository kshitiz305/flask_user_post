**Documentation**

Documenting our code is important for making it easy to understand and use. There are many tools and formats for documenting APIs, but one popular choice is Swagger/OpenAPI. In this section, we will use Flask-RESTPlus to generate Swagger documentation for our API.

Add the following code to the app.py file, at the top of the file:

In this code, we use Flask-RESTful to define our API endpoints and handle requests and responses. We also use Flask-SQLAlchemy to define our database models and interact with our database.

We define two database models, User and Post, which have a many-to-one relationship (one user can have many posts). We also define a many-to-many relationship between Post and User to handle the liking of posts.

We then define our API endpoints using Flask-RESTful's Resource class, and define the routes and HTTP methods that they respond to. We use the reqparse module to parse the request arguments and fields module to marshal the response data. Finally, we add our resources to the API using the api.add_resource() method.

To run this application, you'll need to install Flask, Flask-RESTful, and Flask-SQLAlchemy. You can do this using pip:


You can test the API using a tool like Postman or cURL. For example, to create a new user, you can send a POST request to `http://localhost:5000/users` with the following JSON data:

{
"username": "john",
"email": "john@example.com"
}



And to like a post, you can send a POST request to `http://localhost:5000/posts/1/like` with the following JSON data:

{
"user_id": 1
}

