import time, sys, os
sys.path.append((os.path.dirname(__file__)))
from utils.config import *
from utils.funcs import *
from utils.consts import *

def main(tusAmount):
    amountOutMin = getAmountOutMinTusToAvax(tusAmount)
    parameters = {
        "amountIn": zeroHex(tusAmount),
        "amountOutMin": zeroHex(amountOutMin),
        "unknown1": zeroHex(160),
        "userAddress": (MAIN_ADDRESS[2:]).rjust(64,"0").lower(),
        "deadline": zeroHex(round(time.time() * 1000) + 120000),
        "unknown2": zeroHex(2),
    }
    dataInput = METHODS["swapExactTokensForAVAX"]
    for parameter in parameters.keys():
        dataInput += parameters[parameter]
    dataInput += TUS_TO_AVAX_PATH.lower()
    sendAvaxTx(address=MAIN_ADDRESS, to=TRADER_JOE_CONTRACT_ADDRESS, dataInput=dataInput)   
    return amountOutMin

if __name__ == "__main__":
    main()

