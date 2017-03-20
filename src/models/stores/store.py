import uuid
import src.models.stores.errors as StoreErrors


from src.common.database import Database
import src.models.stores.constants as StoreConstants



class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix

        # i.e - "span"
        self.tag_name = tag_name

        # i.e - "itemprop": "price"
        self.query = query
        self.id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)



    def json(self):
        return{

            "_id": self.id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query

        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))



    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTION, self.json())


    @classmethod
    def get_store_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name:": store_name}))


    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        # returns an item from the COLLECTION that has a url_prefix that matches
        return cls(**Database.find_one(StoreConstants.COLLECTION,
                                       {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        """
        return a store from a url like "http:www.johnlewsi.... etc

        :param url:  the item's URL
        :return: a store, or raises a StoreNotFoundException if no store matches the Url
        """

        for i in range(0,len(url) + 1):

            try:
                # checks if the prefix matches, char by char
                store = cls.get_by_url_prefix(url[:i])

                return store

            except:
                raise StoreErrors.StoreNotFoundException("the URL Prefix used to find the store didn't return a match ")