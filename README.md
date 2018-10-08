# Morais Farmer's Market

```text
 #######                  #######                                    ###
    #    #    # ######    #         ##   #####  #    # ###### #####  ###  ####
    #    #    # #         #        #  #  #    # ##  ## #      #    #  #  #
    #    ###### #####     #####   #    # #    # # ## # #####  #    # #    ####
    #    #    # #         #       ###### #####  #    # #      #####           #
    #    #    # #         #       #    # #   #  #    # #      #   #      #    #
    #    #    # ######    #       #    # #    # #    # ###### #    #      ####

        #     #
        ##   ##   ##   #####  #    # ###### #####
        # # # #  #  #  #    # #   #  #        #
        #  #  # #    # #    # ####   #####    #
        #     # ###### #####  #  #   #        #
        #     # #    # #   #  #   #  #        #
        #     # #    # #    # #    # ######   #  
```

A marketplace application to showcase items available for purchase at the farmer's market.

## System Overview

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

See `design.md` for a peek behind the curtain into my implementation decisions.

## How to Run

----
This application depends on Docker, so I will assume it is already installed, and that this repository has been cloned.

**Warning: the `docker-compose build` for this project will take around 10 or 15 minutes**.

### Run the CLI **(Shortest path to testing this application)**

The CLI provides an input interface for creating carts and producing itemized results, much like a test client.

> `docker-compose build client`

then

> `docker-compose run client`

will provide a command prompt with which to interact with the API, i.e. ...

```text
Commands:
   action : description
   ....

>>> CH1, AP1
```

### Run the API standalone

> `docker-compose up market-api`

### Run Tests

Tests may be executed using docker-compose, as well.

Client tests:
> `docker-compose up --build <service-name>-tests`

## Viewing Logs

Often useful is the ability to see how each service is behaving...

> `docker-compose logs <service-name>`
