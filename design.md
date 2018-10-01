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

I go into the defense of each component later, but a component-based design with separation of concerns is easier to manipulate than a highly-coupled monolith. As an app that one might like to reuse as the years go by, pick apart to refactor, or modify data without deploying new code, this breakdown provides many positives. These components are easily scalable, they can be replaced easily if deemed insufficient, simpler, coherent, readable, concerns are properly separated throughout the application, and probably many more advantages.

The trade-off is in locality of detail as the implementation of the entire system is spread across different parts. However, this project is stored as a monolithic repository with a composition for local development to make it easier to run and debug the full system. Another trade-off is in how much more difficult it could be to deploy a multi-headed system, but we use container orchestration for that when necessary.

### Containerization

Containerization is key to validation of behavior and deployment to a variety of environments. For this reason the components of the application will be arranged as a set of service containers. This is both easy and effective, rather than a traditional installation of such a system directly in an OS without virtualization.

An issue one runs into without containers/virtualization is not only in the difficulty of validating parity of behavior between local-dev and prod, but also with the differences in how technology behaves on a variety of systems such as Postgres vs MySQL.

## API

----
***Note***: The following sections, including this one, may change a little in terms of specifics by the end of the project but the general overview should be the same.

Making the case for the API before discussing the CLI is important, so I am starting there. The description of the problem implies that there are products, carts, discounts, and operations on those resources. One way that e-commerce sites manage such resources is to gate access to them via resource routes. The simpler alternative for this problem description is to hard-code the products and write specialized logic for applying coupons, etc, but it is not very maintainable or generic. At best, it is useful for one season and then will likely have to be modified then redeployed. Organizing the resources into a set of accessors via HTTP that enable management as well as client access is a more tenable solution.

The following are some rough ideas of datums the API will serve

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

### Carts

```pseudo
CartItem{
    cart
    items
}
```

### Specials

Here are some conceptual data types for the way Specials will be described in the system:

Specials can vary, but they always consist of the form:
> ***condition*** --> ***reward*** (limited to "***limit***")

Conditions also come in a common format
> if cart contains ***quantity*** of ***product***, then (sufficient conditions met)

Rewards then have the form
> ***product*** price changed by ***percent***

Here are a few examples

1. > BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)
1. > APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.
1. > CHMK -- Purchase a box of Chai and get milk free. (Limit 1)
1. > APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apples

And here is a potential anatomy for specials, conditions, and rewards

```pseudo
Special{
    code,
    condition,
    reward,
    limit,
}
```

```pseudo
Condition{
    product,
    quantity,
}
```

```pseudo
Reward{
    id,
    product,
    price_change,
    quantity
}
```

So, the specials might be translated into the following descriptions

```python
todo/wip

special: {
    code: 'BOGO',
    limit: 0,
    condition: {
        product: '<product code>'
    },
    reward: {
        free: {
            product: '<product code>'
        }
    },
}
```

```python
todo: APPL
```

```python
todo: CHMK
```

```python
todo: APOM
```

## CLI

----
Overshadowed by the larger underlying system, the solution does require a test client, i.e. "store front", for demonstration and analysis. This is a separate application which calls the API as any client would call a RESTFul API, using HTTP. The CLI is flexible in that it can be shipped independently since it is standalone, can be pointed at any API service, or even thrown out and written in a different language. After all, graphical UX is a better way to interact with the API.

## Database

----
The database is intended to store all of the data of an application which is externally fed into the application through behaviors of the system (i.e. client interactions), that is not imperative logic, and which must be persisted independently of the API process.

Databases are a natural fit for storing products, but there are 2 flavors that come to mind, relational and non-relational(i.e. NoSQL). There is a case for the market's products to be stored in a relational database, because they may ultimately be related to other datums such as specials, carts, transactions, recommendations, reviews, distributors, or many others.

I concede that if products are the only thing in the database ever, no exceptions, then they could instead be stored in a key-value store.

### Storing Specials

Specials do not fit the SQL model. They are a complex expression containing multiple datums that are only relevant to each other. While we want to store and manage them independent of the service implementation, they do not lend themselves well to table columns because of their document nature. For these, a document store would be more appropriate.

For one, specials have too many optional parts, and there needs to be a clear method of conveying them to services. Also, the service could be flexible to different formats of specials descriptions because there is no schema. The main point, its easier than asking "content providers" to fit their coupons into our arbitrary table design.

## Cart Cache

----
Carts are data that would be persisted for only a session, at least given the current requirements, so rather than store them in the database where they will build up and be forgotten, they will merely be cached for a TTL server-side.

## Is this overly-complex

----
It depends on how the system is used, what happens in the future, etc. whether or not this design is more complex than is necessary. More specifically, it is true that, while this architecture is more maintainable, operable, coherent, and scalable, it would be easier if the app is only for one occasion to write a hard-coded script instead. In short, with such a low value goal, one should not over-invest.

Yet, I assumed that this year's farmer's market debut on e-commerce is just the beginning, with more future plans in the long-term vision. If it costs X to build the basic, one-time-use, unmaintainable solution, then the question is how that compares to the CBA of a simple, service-oriented, and reusable architecture. If the cost is less-than 2X and is useful the following year by only changing live data then there is already a cost savings for the end user.

## Technical Details

----
At a high level we have a system with the following design:

```pretty drawings
  |-----------|        |---------|       |-------------|      |---------------|
  | Client(s) | ---->  | Gateway | ----> | Product Svc |----> | Products (DB) |
  |-----------|        |---------|       |-------------|      |---------------|
                           |                   ^
                           |                   |
                           |             |-----------|        |---------------|
                           |-----------> | Carts Svc |------> | Carts (Cache) |
                           |             |-----------|        |---------------||
                           |                   |
                           |                   v
                           |             |--------------|     |-----------------------|
                           |-----------> | Specials Svc |---> |  Specials (Documents) |
                           |             |--------------|     |-----------------------|
```

The API is a public gateway that proxies to the service layer, which serves data from storage. The CLI is a client application communicating with the API for its views of that data.

### Multiple Apps

Having this many services requires a Dockerfile for each. If you look in the `docker` directory, you will notice multiple directories corresponding to the applications, each containing a Dockerfile. In docker-compose, one merely directs each service to its corresponding Dockerfile under the `build` block (See: `docker-compose.yml`)

### Source Layout

At the root are meta files such as ignore, .env, to avoid shipping them in any images.

In order to aid coherence of the repository for future maintenance, the two applications are split into separate projects. Within those projects are the `src` directory, which contains the code to be shipped in the image, and the apps package dependencies, as `requirements.txt`. The `api` also has a tests directory. The client may require test coverage, but it is less significant

### SOA

Because there are various faculties of the API which could grow in complexity, it is desirable to insulate the API layer from that possibility, as it is comprised of contracts, customer-facing, and should always be available. This is accomplished by abstracting data access from the interface itself. The interface (API) presents a view of data, the store contains data, but the service provides data. This way, if we want to break out a service, the API is none the wiser, as long as the output from the service layer is the same.

### TDD

I shall adhere to a test-driven approach as much as possible, because being runnable and having tools to verify accurately as you code is key to a healthy progression through the workload of implementing the API.

### Configuration

Connection details and other options will be supplied via environment, but if they aren't provided then reasonable defaults will be used instead to reduce friction for getting it operating in a production environment.

### Tech

The CLI will be written in Python, although it could be written in anything. I almost wrote it in Go because, personally, I enjoy writing Go CLI after doing a considerable research into a few different styles. However, that was not enough of a reason to make the project bilingual.

Using Python/Flask for the API is straight-forward, in my opinion, because the API is not yet very complex and Flask grows well with time.

The Products DB will simply be MySQL, but that is an artifact that could likely be changed at the deployment and configuration level.

The store that matches our need for storing Specials as documents is MongoDB based on the fact that its schema-less. There are certainly other options, but MongoDB is a popular choice, and I would not want to investigate a multitude of options without good reason.

For a temporary Cart store we can use the Redis key-value store, as it is a popular choice for volatile memory storage, granting the ability to expire carts automatically via TTL.

The tests are written for pytest, and a docker-compose command will run them (see README.md).

## Notes

----
These are updates or additional comments about the design added afterward...

## Future Work

----
Always room to improve...

### Better UX

A proper frontend, such as an application or web view, would be more fluid for the customer amounting to greater sales, and likely the most valuable return on investment.

For this Flask API one could follow the pack and use Jinja 2 to render data from the backend in HTML, but since the interface is HTTP it could be almost any popular frontend technology.

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
