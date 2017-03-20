import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class alert(object):
    def __init__(self, user_email, price_limit, item_id, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is not None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id



    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email,
                                                                self.item.name,
                                                                self.price_limit
                                                                )

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api, AlertConstats.API_KEY"),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "The Price has changed to {}".format(self.item.price)
                }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.AlERT_TIMOUT):

        # returns a datetime that is 10 minutes ago
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)


        # returns a list of alert elements all with a last checked that were more than
        # 10 mins ago
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {
                                                            "last_checked":
                                                                {"gte": last_updated_limit}

                                                      })]


    def save_to_mongo(self):
        Database.insert(AlertConstants.COLLECTION, self.json())


    def json(self):

        return{

            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item": self.item._id
        }




