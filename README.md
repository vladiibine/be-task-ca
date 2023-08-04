# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
   2. Answer: Probabably the best way to split would be one which does not create distributed transactions. As such, 
      ideally, we'd have a user service, and an item & cart_item service. The item & cart_item service would make 
      sense because there are transactional operations that must be done on cart checkout: we shouldn't be able to buy 
      (check out) more items than the number of items we have in physical storage; we also should not be able to even 
      put them in the cart to begin with - which is why the item & cart_item microservice should not rely on data from 
      external services in order to execute these transactions
2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, 
   usecases and the model?
   3. Answer: his project fails to adhere to the clean architecture because the clean architecture consists of 4 layers: 
      entities, usecases, interfaces/adaptors and frameworks. The codebase seems to be completely missing the 4th layer, 
      the adapters. All the layers of this application know about and pass along references to sqlalchemy objects. While 
      this kind of structure is common for code bases, one of the purposes of the clean architecture, is to make it really 
      easy to switch frameworks and other specific technologies and tools, while keeping all the business rules unmodified. 
      One place that could work as the "interfaces/adaptors" layer is in the app.py and api.py files. 
      It could work as an anti-corruption layer, initializing the DB connection, but passing adaptor objects into 
      the other layers.
3. What would be your plan to refactor the project to stick to the clean architecture?
   4. First, create the entities layer (currently, a adaptor-like components are being used instead of "pure" entities)
      (this has been implemented for the Item entity)
   5. Second, get fastapi references out of the use-cases layer
4. How can you make dependencies between modules more explicit?
   5. The instantiation of all repositories, and passing all repositories down to the use-case layer should be explicit
      (in the original version of this repo, use-cases would freely use any repository action they please)
   6. An architectural fitness function could be written, to ensure we never import and instantiate items from
      "outward" layers in "inward" layers (for instance, we don't import usecases from the entity layer)

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.