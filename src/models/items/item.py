import uuid

import requests
import re
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        tag_name = store.tag_name
        query = store.query
        self.price = self.load_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):

        # Get the page content from the stored url
        request = requests.get(self.url)

        # DEBUG
        # print("here is the content {}".format(request.content) )

        content = request.content

        # Initialize beautiful soup
        soup = BeautifulSoup(content, "html.parser")

        # find the element by tag_name, query
        element = soup.find(tag_name, query)
        element2 = soup.find("span", {"itemprop": "price", "class": "now-price"})


        # # DEBUG
        # print("here is the element 1 text: {} ".format(element))
        # print("here is the element 2 text: {}".format(element2))




        string_price = element.text.strip()

        # search the returned string for xxxx.xx
        pattern = re.compile("(\d+.\d+)")  # () gives a matching group
        match = pattern.search(string_price)

        #finds the group from the regex and returns it
        return match.group()


    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())
        pass


    def json(self):
        return{

            "name": self.name,
            "url": self.url,
            "_id": self._id

        }



    # for AMAZON
    # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$1,798.00</span>
