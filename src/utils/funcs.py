import time, requests, sys, os
sys.path.append((os.path.dirname(__file__)))
from statistics import median
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError
from consts import *
from config import *

def Hex(num):
    return str(hex(num))[2:]


def zeroHex(num):
    return Hex(num).rjust(64,"0")


def printn(text):
    print("\n",text)


def printLine():
    printn(40*"-")


def sleepy(secs):
    printn(f"Sleeping {secs} secs...")
    time.sleep(secs)


def getGasPrice():
    gasPriceUrl = "https://api.debank.com/chain/gas_price_dict_v2?chain=avax"
    gasPriceFast = int(requests.get(gasPriceUrl).json()["data"]["fast"]["price"])
    return gasPriceFast


#return the given address's balance
def checkSwimmerBalance(address):
    w3 = Web3(Web3.HTTPProvider(SWIMMER_NETWORK_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    balance = w3.eth.getBalance(address)
    return balance


#return the given address's balance
def checkAvaxBalance(address):
    w3 = Web3(Web3.HTTPProvider(AVAX_NETWORK_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    balance = w3.eth.getBalance(address)
    return balance


#sends transaction from given address with given dataInput, sends type2 EIP-1559 transaction.
def sendSwimmerTx(address, to, dataInput="", value=0, sleepTime=10):
    w3 = Web3(Web3.HTTPProvider(SWIMMER_NETWORK_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    account = w3.eth.account.from_key(PRIVATE_KEYS[address])
    nonce = w3.eth.getTransactionCount(account.address)
    rawTransaction = {
            "chainId" : hex(SWIMMER_CHAIN_ID),
            "from": address,
            "maxFeePerGas": SWIMMER_MAX_FEE_PER_GAS,
            "maxPriorityFeePerGas": SWIMMER_MAX_PRIORITY_FEE_PER_GAS,
            "gas": SWIMMER_GAS_LIMIT, 
            "to": to,
            "value": value,
            "data" : dataInput,
            "nonce" : nonce,
            "type":2,
        } 
    printn("Sending EIP-1559 tx...")
    try:
        gas_estimate = w3.eth.estimate_gas(rawTransaction) #checks if the contract will throw error.
    except ContractLogicError as e:
        printn(f"Tx is expected to be fail. Not sending...\n{e}")
        return
    signedTxn = account.sign_transaction(rawTransaction) 
    w3.eth.send_raw_transaction(signedTxn.rawTransaction) 
    printn("EIP-1559 tx sent...")
    if sleepTime >0:
        sleepy(sleepTime)


#sends transaction from given address with given dataInput, sends type2 EIP-1559 transaction.
def sendAvaxTx(address, to, dataInput="", value=0, sleepTime=10):
    w3 = Web3(Web3.HTTPProvider(AVAX_NETWORK_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    account = w3.eth.account.from_key(PRIVATE_KEYS[address])
    nonce = w3.eth.getTransactionCount(account.address)
    rawTransaction = {
            "chainId" : hex(AVAX_CHAIN_ID),
            "from": address,
            "maxFeePerGas": AVAX_MAX_FEE_PER_GAS,
            "maxPriorityFeePerGas": AVAX_MAX_PRIORITY_FEE_PER_GAS,
            "gas": AVAX_GAS_LIMIT, 
            "to": to,
            "value": value,
            "data" : dataInput,
            "nonce" : nonce,
            "type":2,
        } 
    printn("Sending EIP-1559 tx...")
    try:
        gas_estimate = w3.eth.estimate_gas(rawTransaction) #checks if the contract will throw error.
    except ContractLogicError as e:
        printn(f"Tx is expected to be fail. Not sending...\n{e}")
        return
    signedTxn = account.sign_transaction(rawTransaction) 
    w3.eth.send_raw_transaction(signedTxn.rawTransaction) 
    printn("EIP-1559 tx sent...")
    if sleepTime >0:
        sleepy(sleepTime)


def seperate(data):
    data = data[10:]
    parameters = list()
    while len(data)>0:
        parameters.append(data[:64])
        data = data[64:]
    return parameters


def getDataInput(tusAmount):
    bridgeTusAmount = zeroHex(tusAmount)
    address = MAIN_ADDRESS[2:].lower() + 24 * "0"
    dataInput = ""
    params = [
        "0xdb58a659",
        "000000000000000000000000000000000000000000000000000000000000006a",
        "0000000000000000000000000000c76ebe4a02bbc34786d860b355f5a5cec202",
        "00000000000000000000000000000000000000000000000000000000000000a0",
        "0000000000000000000000000000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000000000000000000000000120",
        "0000000000000000000000000000000000000000000000000000000000000054",
        bridgeTusAmount,
        "0000000000000000000000000000000000000000000000000000000000000014",
        address,
        "0000000000000000000000000000000000000000000000000000000000000000"
    ]
    for param in params:
        dataInput += param
    return dataInput


def getCrosschainFee():
    txsUrl = "https://subnet-explorer-api.avax.network/v1.1/73772/transactions?address=0xe39283E3ABFfa7F3Ba25Bb6dfbed542a775F7742&sort=desc"
    lastTenHaskes = [tx["hash"] for tx in requests.get(txsUrl, headers=HEADERS).json()["transactions"][:10]]
    w3 = Web3(Web3.HTTPProvider(SWIMMER_NETWORK_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    feeList = list()
    for hash in lastTenHaskes:
        tx = w3.eth.getTransaction(hash)
        seperated = seperate(tx["input"])
        tusAmount = int(seperated[6], 16)
        value = tx["value"]
        fee = value - tusAmount
        feeList.append(fee)
    return median(feeList)


def waitForNativeTransfers():
    passedTime = 0
    while True:
        printn(f"waiting for native transfers. passed time: {passedTime}")
        isOk = True
        for address in SIDE_ADDRESSES:
            balance = checkSwimmerBalance(address)
            if balance > 300*pow(10,18):
                isOk = False
        if isOk:
            break


def waitForBridge(bridgeAmount):
    waitTime = 15*60
    passedTime = 0
    sleepTime = 10
    while True:
        printn(f"waiting for bridge. passed time: {passedTime}")
        passedTime += sleepTime
        if passedTime > waitTime:
            return False
        tusAmount = getTusAmount(MAIN_ADDRESS)
        if tusAmount == bridgeAmount:
            return True
        sleepy(sleepTime)    
        

def waitForSwap(amountOutMin):
    printn("Waiting for swap...")
    waitTime = 15*60
    passedTime = 0
    sleepTime = 10
    while True:
        printn(f"waiting for swap TUS to AVAX. passed time: {passedTime}...")
        passedTime += sleepTime
        if passedTime > waitTime:
            return False
        avaxBalance = getAvaxAmount(MAIN_ADDRESS)
        if avaxBalance > amountOutMin:
            return True
        sleepy(sleepTime)


def getTusAmount(address):
    tusApi = f"https://api.snowtrace.io/api?module=account&action=tokenbalance&contractaddress=0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172&address={address}&tag=latest&apikey="
    tusAmount = int(requests.get(tusApi).json()["result"])
    return tusAmount


def getAvaxAmount(address, rounded=False):
    avaxApi = f"https://api.snowtrace.io/api?module=account&action=balance&address={address}&tag=latest&apikey="
    avaxAmount = int(requests.get(avaxApi).json()["result"])
    if rounded:
        return round(avaxAmount/pow(10,18),3)
    return avaxAmount


def getAvaxPrice():
    url = "https://api.dexscreener.com/latest/dex/pairs/avalanche/0xf4003f4efbe8691b60249e6afbd307abe7758adb"
    price = requests.get(url).json()["pair"]["priceUsd"]
    return float(price)


def getTusPrice():
    url = "https://api.dexscreener.com/latest/dex/pairs/avalanche/0x565d20bd591b00ead0c927e4b6d7dd8a33b0b319"
    price = requests.get(url).json()["pair"]["priceUsd"]
    return float(price)


def getAmountOutMinTusToAvax(tusAmount):
    tusPrice = float(getTusPrice())
    avaxPrice = float(getAvaxPrice())
    amountOutMin = ((tusAmount*tusPrice)/avaxPrice) * ((100-SLIPPAGE)/100)
    return int(amountOutMin)


def isAddressValid(address):
    w3 = Web3(Web3.HTTPProvider(SWIMMER_NETWORK_URL))
    return w3.isAddress(address)


def checkAddresses():
    if not isAddressValid(MAIN_ADDRESS):
        raise Exception("Main address is not valid. Please check.")

    if not isAddressValid(BINANCE_AVAX_C_ADDRESS):
        raise Exception("Binance address is not valid. Please check.")

    for address in SIDE_ADDRESSES:
        if not isAddressValid(address):
            raise Exception(f"Address {address} is not valid. Please check.")


if __name__ == "__main__":
    print(isAddressValid("0x804e7499bc3204B01E8e2D5144a5F9826Db2f991"))
    # print(getAvaxAmount("0x804e7499bc3204B01E8e2D5144a5F9826Db2f991"))
