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

'''