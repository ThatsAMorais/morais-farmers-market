#!/usr/bin/env python
import os

from app.client import Client


badge = """
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
"""


if __name__ == "__main__":
    print(badge)

    client = Client(
        service_host=os.getenv('MARKET_SERVICE_HOST'),
        service_port=os.getenv('MARKET_SERVICE_PORT'))
    client.start()
