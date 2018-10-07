# Morais Farmer's Market - Design

A CLI application backed by a shop API with a MySQL database.

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

## Value

This is some of the projected value of this design

1. Separation of features into small, sensible services brings high flexibility, scalability, maintainability, and coherence, presenting a tangible perception that the product is valuable to one who is interested in administering such a system (i.e. a customer of a software consultancy).
1. Driven by tests from the beginning, the implementation is guaranteed to adhere to designs, requirements, and be resilient to later modification.
1. smaller services = fewer lines of code = components can be refactored within clearly contracted boundaries, reducing software development costs of future investments
1. Each unit is small enough that scaling is both surgical and low cost, reducing operational costs
1. Containerization makes DevOps's life easier compared to non-virtualized CI/CD, lowering costs and reducing the impact of production incidents
1. Manageable content makes for reusability of the system across different product lines and business cycles
1. SOA reduces the difficulty of integrating a 3rd party with a particular resource, presenting a multitude of growth opportunities

## Break the 4th wall a moment

"This is huge!" I completely understand that reaction. I could have written another CLI application, avoiding deeply nested loops, choosing appropriate data structures, and ensuring my edge cases. However, over the past 5 years the opportunities I have pursued in my career have brought many lessons, and this project was a way to culminate that period of time into a piece of work representative of my knowledge in the API and Web Service problem domain. In truth, it could not possibly cover every detail as it is a specific problem with its own trade-offs, and such products are imperfect therefore prone to improvements over time. So, I am using this opportunity, and taking liberty in it, to "go too far" or consider a wider set of goals than the problem description would imply, especially since this application is somewhat hypothetical with no real stakeholders to suffer at the expense of my liberties.

## Brainstorming

----
Considering the requirements, lets find a design that covers every feature....

Firstly, the user must be able to enter items and request an invoice for the current cart, which requires input through a CLI. Each command will require some handling code or method.

But first, TDD. Regardless of what the implementation of these commands will be, tests can be written to validate the expected behavior. Also, that means the implementations of the commands must be testable, so they should be abstracted to methods.

Accuracy describes a correct implementation with working features, which requires correct prices, output displayed as requested, discounts applied, and the ability to generate the invoice on demand. The current register must be persisted for the session or until cleared which could be accomplished with local memory. Products, prices, and specials could be defined as "constants" if we were to assume they will never change.

However, to be flexible to new products, prices, specials, and even technological choices, the design should separate concerns better. For example, the most important element of this application is conveying prices and products available for only a limited time. Therefore, those elements that may change should be configurable without deploying new code, such as through APIs and a database.

### Greater Flexibility

This is where the design could be broken down into components such as:

* CLI - For operating on the Service as a test client
* Products Service - for serving Products
* Database - A manageable store for persistent data
* Cart Service - serves Cart data
* Redis Cache - temporary key-value storage
* Specials Service - serves Specials data
* Document Store - stores document objects
* RESTful API Gateway - Provides a single public layer to expose to clients

I go into the defense of each component later, but a component-based design with separation of concerns is easier to manipulate than a highly-coupled monolith. As an app that one might like to reuse as the years go by, pick apart to refactor, or modify data without deploying new code, this breakdown provides many positives. These components are easily scalable, they can be replaced easily if deemed insufficient, simpler, coherent, readable, concerns are properly separated throughout the application, and likely many more advantages.

The trade-off is in locality of detail as the implementation of the entire system is spread across different parts. However, this project is stored as a monolithic repository with a composition for local development to make it easier to run and debug the full system. Another trade-off is in how much more difficult it could be to deploy a multi-headed system, but we use container orchestration for that.

### Containerization

Containerization is key to validation of behavior and deployment to a variety of environments. For this reason the components of the application will be arranged as a set of service containers. This is both easy and effective, rather than a traditional installation of such a system directly in an OS without virtualization.

An issue one runs into without containers/virtualization is not only in the difficulty of validating parity of behavior between local-dev and prod, but also with the differences in how technology behaves on a variety of systems such as Postgres vs MySQL.

## API

----
***Note***: The following sections, including this one, may change a little in terms of specifics by the end of the project but the general overview should be the same.

Making the case for the API before discussing the CLI is important, so I am starting there. The description of the problem implies that there are products, carts, discounts, and operations on those resources. One way that e-commerce sites manage such resources is to gate access to them via resource routes. The simpler alternative for this problem description is to hard-code the products and write specialized logic for applying coupons, etc, but it is not very maintainable or generic. At best, it is useful for one season and then will likely have to be modified then redeployed. Organizing the resources into a set of accessors via HTTP that enable management as well as client access is a more tenable solution.

### Product

These are products:
| Product Code |     Name     |  Price  |
|:-------------|:-------------|--------:|
|     CH1      |   Chai       |  $3.11  |
|     AP1      |   Apples     |  $6.00  |
|     CF1      |   Coffee     | $11.23  |
|     MK1      |   Milk       |  $4.75  |
|     OM1      |   Oatmeal    |  $3.69  |

```pseudo
Product{
    code,
    name,
    price,
    active,
    date_added,
}
```

### Specials

Specials must be expressed and codified so the system can apply them. Here are some conceptual data types for the way Specials will be described in the system:

Specials consist of:
> ***condition*** --> ***reward*** (limited to "***limit***")

Conditions have the form:
> if cart contains ***quantity*** of ***product***, then (sufficient conditions met)

Rewards have the form
> ***product*** price changed by ***percent*** (limited to quantity)

Here are a few examples

1. > BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)
1. > APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.
1. > CHMK -- Purchase a box of Chai and get milk free. (Limit 1)
1. > APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apples

The above discounts are simple, but with one concerning overlap regarding an apple discount when buying oatmeal and exceeding 3 bags of apples in one cart. There are three mathematical strategies we can use:

* Add all discounts together as a single percentage, producing the best outcome for the shopper
* More balanced, but on average smaller individually, producing the best outcome for the store
* Apply each in increasing order, producing somewhere in the middle

I will choose the last one for the sake of being able to sort the possible reward from lowest to highest.

#### Storage

Specials do not fit the SQL model. They are a complex expression containing multiple datums that are only relevant to each other. While we want to store and manage them independent of the service implementation, they do not lend themselves well to table columns because of their document nature. For these, a document store would be more appropriate.

For one, specials have too many optional parts, and there needs to be a clear method of conveying them to services. Also, the service could be flexible to different formats of specials descriptions because there is no schema. The main point, its easier than asking "content providers" to fit their coupons into our arbitrary table design.

See the cashier/seed.py for a description of how I codified specials into json to be stored as documents.

## CLI

----
Overshadowed by the larger underlying system, the solution does require a test client, i.e. "store front", for demonstration and analysis. This is a separate application which calls the API as any client would call a RESTFul API, using HTTP. The CLI is flexible in that it can be shipped independently since it is standalone, can be pointed at any API service, or even thrown out and written in a different language. After all, graphical UX is a better way to interact with the API.

## Database

----
The database is intended to store all of the data of an application which is externally fed into the application through behaviors of the system (i.e. client interactions), that is not imperative logic, and which must be persisted independently of the API process.

Databases are a natural fit for storing products, but there are 2 flavors that come to mind, relational and non-relational(i.e. NoSQL). There is a case for the market's products to be stored in a relational database, because they may ultimately be related to other datums such as specials, carts, transactions, recommendations, reviews, distributors, or many others.

I concede that if products are the only thing in the database ever, no exceptions, then they could instead be stored in a key-value store.

## Cart Cache

----
Carts are data that would be persisted for a limited time, at least given the current requirements, so rather than store them in the database where they will build up and be forgotten, they will merely be cached for a finite TTL in a key-value store.

The carts will be stored kinda like this:

| key | value |
|----|----|
|GUID|list(products)|
|invoice:GUID|json|

```python
GUID: [ "product_code", ...]
```

```python
invoice:GUID : {
    "total": 1.0,
    "items": [
        {
            "code": 'product-code',
            "price": 2.0,
            "special": [
                {
                    "code": 'special-code',
                    "adjustment": -1.0
                },  # ....
            ]
        },  # ....
    ]
}
```

The invoice will not be calculated until it is requested, but it will be stored afterward for future queries on the same cart state. Therefore, when a cart is updated, its invoice must be recalculated. Its simplistic to remove the invalidated invoice so that it can be recalculated later with the latest information, but it may be totally sufficient. One could imagine a system that updates the invoice, but that may be complex.

This is where some `Future Work` could be invested to improve this solution. However, one should not optimize a system that might seem to do extra work through its statelessness which could be stored. Furthermore, one should first resort to caching before increasing storage requirements prior to reaching a scale where this solution is costly or prohibitive.

## Is this overly-complex

----
It depends on how the system is used, what happens in the future, etc. whether or not this design is more complex than is necessary. More specifically, it is true that, while this architecture is more maintainable, operable, coherent, and scalable, it would be easier if the app is only for one occasion to write a hard-coded script instead. In short, with such a low value goal, one should not over-invest.

Yet, I assumed that this year's farmer's market debut on e-commerce is just the beginning, with more future plans in the long-term vision. If it costs X to build the basic, one-time-use, unmaintainable solution, then the question is how that compares to the CBA of a simple, service-oriented, and reusable architecture. If the cost is less-than 2X and is useful the following year by only changing live data then there is already a cost savings for the end user.

## Technical Details

----
With those details realized, we may now consider data structures for the solution. At a high level we have the following design:

```pretty drawings
  |-----------|        |-------------|       |-------------|      |---------------|
  | Client(s) | ---->  | Gateway API | ----> | Product Svc |----> | Products (DB) |
  |-----------|        |-------------|       |-------------|      |---------------|
                           |                       ^
                           |                       |
                           |                 |-------------|      |-----------------------|
                           |---------------> | Cashier Svc |----> |  Specials (Documents) |
                           |                 |-------------|      |-----------------------|
                           |                       |
                           |                       v
                           |                 |-----------|        |---------------|
                           |---------------> | Carts Svc |------> | Carts (Cache) |
                           |                 |-----------|        |---------------|
```

The API is a public gateway that proxies to the service layer, which serves data from storage. The CLI is a client application communicating with the API for its views of that data.

### Multiple Apps

Having this many services requires a Dockerfile for each. If you look in the `docker` directory, you will notice multiple directories corresponding to the applications, each containing a Dockerfile. In docker-compose, one merely directs each service to its corresponding Dockerfile under the `build` block (See: `docker-compose.yml`)

### Source Layout

At the root are meta files such as ignore, .env, to avoid shipping them in any images.

In order to aid coherence of the repository for future maintenance, the two applications are split into separate projects. Within those projects are the `src` directory, which contains the code to be shipped in the image, and the apps package dependencies, as `requirements.txt`. The `api` also has a tests directory. The client may require test coverage, but it is less significant

### TDD

I shall adhere to a test-driven approach as much as possible, because being runnable and having tools to verify accurately as you code is key to a healthy progression through the workload of implementing the API.

### Configuration

Connection details and other options will be supplied via environment, but if they aren't provided then reasonable defaults will be used instead to reduce friction for getting it operating in a production environment.

### Tech

The CLI will be written in Python, although it could be written in anything. I almost wrote it in Go because, personally, I enjoy writing Go CLI after doing a considerable research into a few different styles. However, that was not enough of a reason to make the project bilingual.

Using Python/Flask for the API(s) is straight-forward because each API is not yet very complex and Flask grows well with time.

The Products DB will simply be MySQL, but that is an artifact that could likely be changed at the deployment and configuration level.

The store that matches our need for storing Specials as documents is MongoDB based on the fact that its schema-less. There are certainly other options, but MongoDB is a popular choice, and I would not want to investigate a multitude of options without good reason.

For a temporary Cart store we can use the Redis key-value store, as it is a popular choice for volatile memory storage, granting the ability to expire carts automatically via TTL.

The tests are written for pytest, and a docker-compose command will run them (see README.md).

## Future Work

----
Always room to improve...

### Better UX

A proper frontend, such as an application or web view, would be more fluid for the customer than a CLI, amounting to greater sales. Likely the most valuable return on investment.

For this Flask API one could follow the pack and use Jinja 2 to render data from the backend in HTML, but since the interface is HTTP it could be almost any popular frontend technology.

### Security and Access Control

Any web resource, especially one exposing endpoints to backend data, must be secured. OAuth2 and OpenID are means to control and authorize access. There is also TLS for service security.

### Better Data Management

The technical knowledge required to operate the system could be decreased if better management tools were provided for adding new specials, modifying products, etc.

### Specials Microservice

Breaking out the coupons/specials to a micro-service, which I might like to write in Go, would allow for the gritty details of parsing and 3rd party noise to be extracted from the otherwise straight-forward API layer.

### Live prediction

While typing, the CLI could interpret each key-press and produce a real-time response, such as predicting what the user may be typing.

### API-side caching

Caching to avoid database calls can be beneficial for data that does not often change, but it can be a pitfall if not executed correctly. There is not very much database access, but we can look at each storage and make a call:

* Products: The API needs to stay as up-to-date on this as possible, so I would shy away from traditional response caching unless the database was seeing significant traffic. Instead, I might implement E-Tag caching on responses because then at least the client does not have to frequently consume the same data to ensure that it has the most recent data. For those that are not aware, E-Tag caching, unlike response caching which avoids database access, reduces bandwidth usage between the Client and the API by sending a "304 - Not Modified" where appropriate.
* Carts: Already in a "cache" and not of much concern unless on a highly constrained system
* Specials: The document store could possibly benefit from a response cache, but, again, this could be a pitfall for the API to have latency between an update to a Special (maybe someone entered the wrong price or product) and when that update takes effect.
* Gateway: Both Response and E-Tag caching should be applied to present this layer with as many options to decrease load on the services.

To be sure, none of the data in this small example is at the scale to deserve caching, but many large-scale APIs implement it with great rewards.

### Container Orchestration

K8s, obviously; The compose for this project is quite large. Naturally, if this project was headed to a `stage` server, it should be done via a helm script.

### Service Base Image

A base image containing several of the requirements on all flask-based services would speed up the initial build of all services. Such libs as Flask, pytest, and requests, are included in all 5 services, except for the client that doesn't use Flask. It doesn't take forever, but its enough to go AFK (which might not be so bad).

### Reduce Python Package Dependencies

Arguably, Python culture is one that favors reuse, but with adoption of a package comes binding to the patterns and styles of it. I would like to reduce the dependency on any but the most basic wrappers on 3rd party tech, which I attempted to do but feel there is room for improvement.
