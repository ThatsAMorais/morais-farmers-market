
import os

from app.api import API


badge = """
               `.-:o         .o:-`
            `-:+:/:o         `s+/+//.
``````````-:++/+-/-o         `o:-+:++/:-``````````
/:/:/:/://do+::/-/-o         `o:-/-/:/sd/:::::/:/:
:::::----:m+/-:/-/-o         `o:-/-/:-+m:------:::
-----....-d//-:/-/-o         `o:-/-/:-+d-......---
----.....-d//-:/-/-o         `o:-/-/:-+d-......---
----.....-d//-:/-/-o         `o:-/./:-+d-......---
-----....-m//-:/-/-o         `o:-/./:-+m-......---
:::::::::/h++//+:+:o         `s/:+:+//+h/:::::::::
`````````./```...:-/         `/-.-..``./.`````````
    ````````````````         `````````````````````
                   GATEWAY API
"""


if __name__ == '__main__':
    print(badge)
    API(port=os.getenv("MARKET_GATEWAY_PORT", "15000"),
        products_service_host=os.getenv('PRODUCT_SERVICE_HOST'),
        carts_service_host=os.getenv('CART_SERVICE_HOST'),
        cashier_service_host=os.getenv('CASHIER_SERVICE_HOST')).start()
