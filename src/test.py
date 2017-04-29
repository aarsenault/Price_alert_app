from src.models.stores.store import Store

from src.models.items.item import Item

from src.common.database import Database

Database.initialize()


# Item("John Lewis Zurich 55cm 4-Wheel Cabin Case", "https://www.johnlewis.com/john-lewis-zurich-55cm-4-wheel-cabin-case/p3128131?colour=Arctic%20Blue", Store("John Lewis", "https://www.johnlewis.com", "span", {"itemprop": "price", "class": "now-price"} ))


i = Item("Washing Machine", "https://www.johnlewis.com/aeg-l7fee865r-freestanding-washing-machine-8kg-load-a-energy-rating-1600rpm-spin-white/p3170003")

print(i.price)
print(i.store)




'''
to run in ipython terminal:

execfile('./src/test.py')

# '''



## COMMANDS TO ENTER THINGS INTO DB
# use fullstack

# db.users.insert({"_id": "1234", "email": "test@test.com", "password": "$pbkdf2-sha256$7665$WKs1ZkwJ4ZxT6t07R0iplQ$ZKfMMAMzKxH64g.3XwaFONAlVwoZf76dWdqW6uSlQtE"})
db.stores.insert({"_id": "a980989112d746a793448e706a6ad976", "query": {"class": "now-price", "itemprop": "price"}, "tag_name": "span", "name": "John Lewis", "url_prefix": "http://www.johnlewis.com"})
db.items.insert({"_id": "d5527d22c0a74a8199fbbc0aab440463", "url": "https://www.johnlewis.com/john-lewis-the-basics-dexter-tall-wide-bookcase/p562354?navAction=jump&_requestid=6493617", "price": 45, "name": "Dexter" })
db.alerts.insert({"_id": "896045e647084cacb37a702f418be707", "price_limit": 100, "last_checked": ISODate("2016-02-09T10:35:31.542Z"), "item_id": "d5527d22c0a74a8199fbbc0aab440463", "user_email": "adriel.arsenault@gmail.com"})