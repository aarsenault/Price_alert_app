import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active


    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email,
                                                                self.item.name,
                                                                self.price_limit
                                                                )

    def send(self):
        print("Sending Email via Mailgun")
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),  # TODO - CHECK
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "The Price has changed to {}".format(self.item.price)
            }
        )

    # gets the alerts that haven't been updated in the last 10 mins
    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        # returns a datetime that is 10 minutes ago
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)

        # returns a list of alert elements all with a last checked that were more than
        # 10 mins ago
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {
                                                          "last_checked":
                                                              {"$lte": last_updated_limit}
                                                      })]

    def save_to_mongo(self):
        Database.insert_or_modify(AlertConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        # load the current price
        self.item.load_price()
        # update the time last checked
        self.last_checked = datetime.datetime.utcnow()
        # save new price to mongo
        self.save_to_mongo()
        self.item.save_to_mongo()

        return self.item.price

    def send_email(self):
        # - NOTE: might be self.item.price()?
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION,
                                                      {"_id": alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()




