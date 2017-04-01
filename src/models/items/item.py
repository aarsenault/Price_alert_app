import uuid
import requests
import re
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "Item(name={}, url={}, price={}, _id={}>".format(self.name, self.url, self.price, self._id)

    def load_price(self):

        # Get the page content from the stored url
        request = requests.get(self.url)
        content = request.content

        # Initialize beautiful soup
        soup = BeautifulSoup(content, "html.parser")

        # find the element by tag_name, query
        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()

        # search the returned string for xxxx.xx
        pattern = re.compile("(\d+\.\d+)")  # () gives a matching group
        match = pattern.search(string_price)

        # groups are what are in the parenthesis
        self.price = float(match.group())
        return self.price

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())
        pass

    # @classmethod
    # def get_by_id(cls, item_id):
    #     return Database.find_one(ItemConstants.COLLECTION, {"_id": item_id})

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))