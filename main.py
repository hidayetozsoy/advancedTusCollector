from time import sleep
from src.tusCollector import main as collectTus
from src.bridge import main as bridgeTus
from src.sendAvaxToBinance import main as sendAvaxToBinance
from src.tusToAvax import main as tusToAvax
from src.utils.config import *
from src.utils.funcs import *

def main():
    checkAddresses()
    if input(f"\n All the money will sent to this address: {BINANCE_AVAX_C_ADDRESS}\n Do you agree? (Y/n):") != "Y":
        printn("process declined.")
        return
    collectTus()
    sleep(10)
    waitForNativeTransfers()
    bridgeAmount = bridgeTus()
    successfulBridge = waitForBridge(bridgeAmount)
    if successfulBridge:
        amountOutMin = tusToAvax(bridgeAmount)
    else:
        raise Exception("something happened during the bridge")
    if waitForSwap(amountOutMin):
        sendAvaxToBinance(amountOutMin)
    print("process is done")


if __name__ == "__main__":
    main()
