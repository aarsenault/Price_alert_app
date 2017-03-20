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
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):

        # Get the page content from the stored url
        request = requests.get(self.url)
        content = request.content

        # Initialize beautiful soup
        soup = BeautifulSoup(content, "html.parser")

        # find the element by tag_name, query
        element = soup.find(self.tag_name, self.query)
        element2 = soup.find("span", {"itemprop": "price", "class": "now-price"})

        string_price = element.text.strip()

        # search the returned string for xxxx.xx
        pattern = re.compile("(\d+.\d+)")  # () gives a matching group
        match = pattern.search(string_price)

        # groups are what are in the parenthesis
        self.price = match.group()
        return self.price


    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())
        pass


    @classmethod
    def get_by_id(cls, item_id):
        return Database.find_one(ItemConstants.COLLECTION, {"_id": item_id})

    def json(self):
        return{

            "name": self.name,
            "url": self.url,
            "_id": self._id

        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))