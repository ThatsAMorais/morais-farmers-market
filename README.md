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

Feel free to open `design.md` for a peek behind the curtain into my implementation decisions.

## How to Run

----
This application depends on Docker, so I will assume it is already installed, and that this repository has been cloned.

### Run the CLI **(Shortest path to testing this application)**

The CLI provides an input interface for creating carts and producing itemized results, much like a test client.

> `docker-compose build client`

> `docker-compose run client`

You will be given a command prompt with which to interact with the API, i.e. ...

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
> `docker-compose up --build client-tests`

Market API tests:
> `docker-compose up --build market-api-tests`

Products Service tests:
> `docker-compose up --build products-tests`

Carts Service tests:
> `docker-compose up --build carts-tests`

Cashier Service tests:
> `docker-compose up --build cashier-tests`
