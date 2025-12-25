---
title: Building Robust Components With Fastapi And Pydantic
published: true
date: 2024-10-12 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/a99e34532241
---

# Building Robust Components with FastAPI and Pydantic

Learn how to build robust FastAPI components using Pydantic for data validation, improving API integrity, readability, and error handling. 

* * *

### Building Robust Components with FastAPI and Pydantic

![](https://cdn-images-1.medium.com/max/800/1*LfpvjEdRRu0UKmrH8RgosA.png)

### Leveraging Well-Defined Objects for Efficient Data Validation

Objects serve as the entry and exit points for [components](https://dev.to/kfir-g/enhancing-software-architecture-through-comprehensive-testing-in-backend-development-4bn2), acting as fundamental gateways for data flow. To create robust, maintainable components, it’s essential to define clear, well-structured fields within these objects. This ensures data integrity and reliable interactions among different system parts. Personally, I prefer using Python along with the FastAPI framework for developing modern, high-performance APIs. For data validation, Pydantic is my library of choice, seamlessly integrating with FastAPI to elegantly enforce field constraints and maintain consistency throughout the system.
    
    
    from fastapi import FastAPI, HTTPException  
    from pydantic import BaseModel, EmailStr, Field, ValidationError, conint  
      
    # FastAPI instance  
    app = FastAPI()  
      
    # Pydantic model for request body validation  
    class User(BaseModel):  
        name: str = Field(..., min_length=3, max_length=50, description="Name must be between 3 and 50 characters")  
        age: conint(gt=0, le=120) = Field(..., description="Age must be between 1 and 120")  # Constrained integer type  
        email: EmailStr = Field(..., description="Must be a valid email address")  
      
    # API route to handle user data submission  
    @app.post("/create-user/")  
    async def create_user(user: User):  
        try:  
            # If validation passes, this will run  
            return {"message": f"User {user.name} created successfully!"}  
        except ValidationError as e:  
            # Catch and return validation errors  
            raise HTTPException(status_code=400, detail=e.errors())  
      
    # Sample invalid data  
    invalid_data = {"name": "A", "age": -5, "email": "invalid_email"}  
      
    # Simulate calling the route with invalid data  
    @app.get("/test-invalid-data/")  
    async def test_invalid_data():  
        try:  
            user = User(**invalid_data)  # Validation will fail here  
        except ValidationError as e:  
            return {"error": e.errors()}  
      
    # Run the server using: uvicorn <filename>:app --reload

In this example, we demonstrate how FastAPI and Pydantic work together to efficiently handle data validation. Using Pydantic’s `BaseModel`, we define validation rules for incoming request data. For instance, we utilize `EmailStr` to automatically validate email formats, simplifying the process without needing custom regex. Similarly, we use `conint` (a constrained integer type) to ensure age falls within a specific range, from 1 to 120. This approach enhances readability and safety.

In the example code, a `User` model is defined with fields such as `name`, `age`, and `email`, each having its validation criteria. When a user submits data through the `/create-user/` route, FastAPI automatically validates the input against these rules. If valid, the user is created successfully; if not, FastAPI raises a `400 Bad Request` with detailed error messages. This significantly reduces the risk of processing incorrect or malicious data, making FastAPI a powerful choice for secure API development.

### Custom Field/Model Validation with Pydantic

Pydantic v2 introduces model-level validation, allowing you to validate multiple fields in relation to each other using the @model_validator decorator. This validation runs after field validation and is particularly useful for ensuring that certain conditions between fields are met. For instance, you might want to confirm that a start_date occurs before an end_date in an event model:
    
    
    from pydantic import BaseModel, model_validator  
    from datetime import date  
      
    class Event(BaseModel):  
        name: str  
        start_date: date  
        end_date: date  
      
        @model_validator(mode='after')  
        def check_dates(cls, values):  
            start, end = values.get('start_date'), values.get('end_date')  
            if start and end and start >= end:  
                raise ValueError('start_date must be before end_date')  
            return values

In this example, the `@model_validator` checks that start_date is earlier than end_date. If this condition is not met, Pydantic raises a validation error. This model-level validation is beneficial for ensuring that the relationships between multiple fields are accurately enforced.

### Custom Serialization in Pydantic

Pydantic allows for custom serialization of model fields by overriding the `dict()` or `json()` methods. This is useful when you want to modify the output format or exclude certain fields during serialization. You can also use the `@property` decorator to add computed fields that are included in serialization but not part of the model's raw data.

Here’s an example of custom serialization that modifies how a full name is returned while excluding the `password` field from the serialized output:
    
    
    from pydantic import BaseModel  
      
    class User(BaseModel):  
        first_name: str  
        last_name: str  
        password: str  
      
        # Custom serialization to return the full name  
        @property  
        def full_name(self):  
            return f"{self.first_name} {self.last_name}"  
      
        # Overriding dict() to exclude the password  
        def dict(self, **kwargs):  
            result = super().dict(**kwargs)  
            result['full_name'] = self.full_name  # Add computed field  
            result.pop('password', None)  # Remove password from serialization  
            return result  
      
    # Example usage  
    user = User(first_name="John", last_name="Doe", password="secret123")  
    print(user.dict())

In this example, `full_name` is a computed property, and we override the `dict()` method to ensure `password` is excluded from the output. Custom serialization like this offers fine-grained control over how model data is exposed in APIs or responses.

### FastAPI and Pydantic Integration

Pydantic integrates seamlessly with FastAPI, providing automatic data validation for request payloads, query parameters, and path parameters. When you define a Pydantic model in a FastAPI endpoint, FastAPI automatically handles parsing and validating the incoming data against the model’s rules. If the data is invalid, FastAPI returns a detailed 422 Unprocessable Entity response with clear error messages.

Here’s a simple example:
    
    
    from fastapi import FastAPI  
    from pydantic import BaseModel  
      
    app = FastAPI()  
      
    class User(BaseModel):  
        username: str  
        age: int  
      
    @app.post("/users/")  
    async def create_user(user: User):  
        return {"message": f"User {user.username} created successfully

In this example, when a POST request is sent to `/users/`, FastAPI uses Pydantic to validate the incoming JSON data. If the data does not conform to the `User` model (e.g., missing `username` or an invalid `age`), FastAPI automatically returns an error response, simplifying input validation and error handling.

### Summary

In summary, leveraging Pydantic with FastAPI enhances your ability to create robust, maintainable applications by ensuring data integrity through clear validations. This powerful combination simplifies the development process while improving security and reliability, making it a preferred choice for building modern APIs.

### References

[Pydantic features in FastAPI](https://fastapi.tiangolo.com/features/#pydantic-features)   
[Pydantic V2 Plan](https://docs.pydantic.dev/2.0/blog/pydantic-v2/)

### In Plain English 🚀

 _Thank you for being a part of the_[** _In Plain English_**](https://plainenglish.io/) _community! Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/)**|**[**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0?si=6b071022ddc847b9)
  * [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
  * More content at [**PlainEnglish.io**](https://plainenglish.io/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [October 12, 2024](https://medium.com/p/a99e34532241).

[Canonical link](https://medium.com/@Kfir-G/building-robust-components-with-fastapi-and-pydantic-a99e34532241)
