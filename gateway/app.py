
import os
from app.api import app


badge = """
                #    ######  ###
               # #   #     #  #
              #   #  #     #  #
             #     # ######   #
             ####### #        #
             #     # #        #
             #     # #       ###
"""

if __name__ == '__main__':
    print(badge)
    app.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_GATEWAY_PORT", "15000"))
