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

### Run the CLI

The CLI provides an input interface for creating carts and producing itemized results, much like a test client.

> `docker-compose up client`

```text
TODO
```

### Run the API standalone

> `docker-compose up api`

 todo: show how to use curl to test against the API

### Run Tests

Tests may be executed using docker-compose

> `docker-compose up --build tests`
