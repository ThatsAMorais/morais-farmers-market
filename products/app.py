import os

from app.products import products


badge = """
 ######
 #     # #####   ####  #####  #    #  ####  #####  ####
 #     # #    # #    # #    # #    # #    #   #   #
 ######  #    # #    # #    # #    # #        #    ####
 #       #####  #    # #    # #    # #        #        #
 #       #   #  #    # #    # #    # #    #   #   #    #
 #       #    #  ####  #####   ####   ####    #    ####
"""

if __name__ == '__main__':
    print(badge)
    products.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_PRODUCTS_PORT", "15010"))
