
import os

from store.redis_store import Store
from app.carts import API


badge = """
  :oooooo/
  `....-ss`
        os-
        :s+
        `ssssssssssssssssssssssssssss/
         os/---+s+----os/----os/---os:
         :sooooosooooossooooossooooss`
         `ss/::/ss/:::os+:::+so:::+s+
          +s+///ss+///os+///oso///os:
          :so///oso///os+//+ss+//+ss`
          .ss:::+so:::os+::/ss:::+s+
        .+so+++++++++++++++++++++++-
       `ss.
       `os:`
        `/osyhddddyssssssssshddddhyss/
           smy:-:ymy``````.dd+--/dd:`
           ym+```/md      -md.``.ym+
           .ymhsydh-       +ddysddo`
             .://-          `-//:`
"""


if __name__ == '__main__':
    print(badge)
    API(port=os.getenv("MARKET_CARTS_PORT", "15010"),
        store=Store(host=os.getenv('CART_STORE_HOST', 'cart-store'))).start()
