import random
import pprint

player_health = 20
coin_purse = 10

player_inventory = {
  'cookie': {"name" : "Cookies", "stock": 1},
  'horse': {"name" : "Horses", "stock": 0},
  'sword': {"name" : "Swords", "stock": 0},
}

store_inventory = {
  'cookie': {"name" : "Cookies", "stock": 5, 'cost': 1, "sell_value": 3},
  'horse': {"name" : "Horses", "stock": 1, 'cost': 15, "sell_value": 7},
  'sword': {"name" : "Swords", "stock": 1, 'cost': 10, "sell_value": 5},
}

def check_inventory():
  print("---------------")
  if player_inventory['cookie']['stock'] > 0:
    print("|", player_inventory['cookie']['name'], "-", player_inventory['cookie']['stock'], "|")
  if player_inventory['horse']['stock'] > 0:
    print("|", player_inventory['horse']['name'], " -", player_inventory['horse']['stock'], "|")
  if player_inventory['sword']['stock'] > 0:
    print("|", player_inventory['sword']['name'], " -", player_inventory['sword']['stock'], "|")
  print("---------------")

def collect():
  num = random.randint(1,25)
  print("You found", num, "coin(s).")
  global coin_purse
  coin_purse += num
  print("You now have", coin_purse, "coin(s).")

def buy(item_name):
  cost = store_inventory[item_name]['cost']
  global coin_purse
  if cost <= coin_purse and store_inventory[item_name]['stock'] > 0:
    player_inventory[item_name]['stock'] += 1
    print("You bought a", item_name, "for", cost, "coin(s)")
    coin_purse -= cost
    print("You have", coin_purse, "coin(s) remaining.")
    store_inventory[item_name]['stock'] -= 1
    if store_inventory[item_name]['stock'] > 0:
      print("The Merchant has", store_inventory[item_name]['stock'], "remaining", item_name + "(s).")
    else:
      print("That was the Merchant's last", item_name + ".")
  elif cost > coin_purse and store_inventory[item_name]['stock'] == 0:
    print("Neither you nor the Mechant have what is needed for this transaction.")
  elif store_inventory[item_name]['stock'] == 0:
    print("The Merchant rolls their eyes and shrugs."
          "Looks like they don't have any", item_name + "s right now.")
  elif cost > coin_purse:
    print("You broke, bud. No", item_name, "for you.")

def eat(item_name):
  if player_inventory[item_name]['stock'] > 0:
    global player_health
    if item_name == 'cookie':
      player_inventory[item_name]['stock'] -= 1
      player_health += 5
      print("The sugar seems to lift your spirits. You now have", player_health, "health units.")
    elif item_name == 'horse':
      player_health -= 10
      print("You bite your horse... but it bites back."
            "What's left of you is worth", player_health, "health units.")
    else:
      print("That doesn't go there.")
  else:
    print("If only you had a", item_name + ".")

def restock():
  store_inventory['cookie']['stock'] += 5
  store_inventory['sword']['stock'] += 1

collect()
collect()
collect()
collect()
buy('sword')
buy('horse')
buy('cookie')
buy('cookie')
buy('cookie')
buy('cookie')
check_inventory()

"""buy('sword')
buy('cookie')
buy('cookie')
print(player_inventory)"""


"""collect()
buy('horse')
eat('horse')"""

"""collect()
collect()
collect()
print(coin_purse)"""

#print(store_inventory['horse'])
#buy(store_inventory["horse"]["name"],store_inventory["horse"]["cost"])
#buy("cookie", 5)
#buy("zebra", 15)
#print(player_inventory)
#print(coin_purse)
