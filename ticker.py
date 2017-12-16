from web3 import Web3, HTTPProvider
from os import path
import json

class CatSalesContract:
    def __init__(self):
      self.web3 = Web3(HTTPProvider('http://pub-node1.etherscan.io:8545'))
      dir_path = path.dirname(path.realpath(__file__))
      with open(str(path.join(dir_path, 'kittysales.json')), 'r') as abi_definition:
        self.abi = json.load(abi_definition)
      self.contract_address = '0xb1690c08e213a35ed9bab7b318de14420fb57d8c'
      self.contract = self.web3.eth.contract(self.abi, self.contract_address)

    def getBalance(self, address):
      return self.contract.call().balanceOf(address)

class CatCoreContract:
    def __init__(self):
      self.web3 = Web3(HTTPProvider('http://pub-node1.etherscan.io:8545'))
      dir_path = path.dirname(path.realpath(__file__))
      with open(str(path.join(dir_path, 'kittycore.json')), 'r') as abi_definition:
        self.abi = json.load(abi_definition)
      self.contract_address = '0x06012c8cf97BEaD5deAe237070F9587f8E7A266d'
      self.contract = self.web3.eth.contract(self.abi, self.contract_address)

def kitty_sale_callback(event):
    kittyId = event['args']['tokenId']
    startPrice = Web3.fromWei(event['args']['startingPrice'],unit='ether')
    endPrice = Web3.fromWei(event['args']['endingPrice'], unit='ether')
    duration = int(event['args']['duration']/3600)
    print("Kitty #{0} for sale: E{1} - E{2}, Duration: {3}h".format(kittyId,startPrice,endPrice,duration))

cat_sales = CatSalesContract()
new_kitty_sale_filter = cat_sales.contract.on('AuctionCreated')
new_kitty_sale_filter.watch(kitty_sale_callback)

while True:
    if new_kitty_sale_filter.stopped:
        break
