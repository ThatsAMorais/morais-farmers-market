#!/usr/bin/env python
import argparse
import sys


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

    # Initialize / Parse CLI
    parser = argparse.ArgumentParser(description='pipeline!')
    args = parser.parse_args()
