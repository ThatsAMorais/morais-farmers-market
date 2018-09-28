# Morais Farmer's Market - Design

A CLI application backed by a shop API with a MySQL database

## Goals

----
Provide the following capabilities:

* Display inventory with price, name, and code
* Create a cart
* Add / Remove items from the cart
* Apply specials automatically
* Display cart incl. price, discounts, and total
* Clear the cart

The result should demonstrate a conscientiousness toward the following characteristics.

 1. Design
 1. Testing
 1. Accuracy
 1. Flexibility
 1. Containerization

## Brainstorming

----
Considering the requirements, lets find a design that covers every feature....

Firstly, the user must be able to enter items and request an invoice for the current cart, which requires input through a CLI. Each command will require some handling code or method.

But first, TDD. Regardless of what the implementation of these commands will be, tests can be written to validate the expected behavior. Also, that means the implementations of the commands must be testable, so they should be abstracted to methods.

Accuracy describes a correct implementation with working features, which requires correct prices, output displayed as requested, discounts applied, and the ability to generate the output on demand. The current register must be persisted for the session or until cleared which could be accomplished with local memory. Products, prices, and specials could be defined as "constants" if we were to assume they will never change.

However, to be flexible to new products, prices, specials, and even technological choices, the design should separate concerns better.

### Greater Flexibility

This is where the design could be broken down into components such as:

* CLI - For operating on the Service as a test client
* RESTful API - Serves the data resources backing the store
* Database - A manageable store for persistent store data
* Cart cache - a cart cache to manage the carts

The complication with breaking things out and using more powerful resources is inevitably transporting that collection of parts to a comparable system with sufficient resources. Luckily, containerization to the rescue.

### Containerization

Containerization, and virtualization, is key to validation of behavior and deployment to a variety of environments. For this reason the components of the application will be arranged as a set of services.

## CLI

----
todo

## API

----
todo

## Database

----
todo

## Cart Cache

----
todo
