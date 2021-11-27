#!python3

import time

# logger = logging.getLogger(__name__)
from pycoingecko import CoinGeckoAPI

# Constants
COIN_LIST = ["gala", "shiba-inu", "cardano", "ripple", "algorand", "uniswap"]
SLEEP_TIME = 60 # Seconds
ITERATIONS = 60 

# Starting values
wallet = 100
cur_coin_id = ''
cur_coin_price = 0
cur_coin_vol = 0

# Volumes
gala_orig = 0
gala_last = 0
shiba_orig = 0
shiba_last = 0
cardano_orig = 0
cardano_last = 0
ripple_orig = 0
ripple_last = 0
algo_orig = 0
algo_last = 0
uni_orig = 0
uni_last = 0

def main():
    cg = CoinGeckoAPI()
    state = 'run'

    # Load coin list
    coin_list = COIN_LIST

    # Dictionary to hold coin info
    coin_data = {}

    # numbers
    _original_wallet = wallet

    _holding_coin = False

    _pot_coin_id = ''
    _pot_coin_price = 0
    _pot_coin_delta = 0

    run_counter = 0
    # print("--starting run")
    while state == 'run':
        
        # print(f"--------------checking coins")
        # get coin list data
        for coin in coin_list:
            
            # Get historic price
            historic = cg.get_coin_ohlc_by_id(coin, 'usd',1)
            old_price = historic[len(historic) - 1]
            
            # Get current price
            close_price = cg.get_price(coin, "usd")
            close_price = close_price[coin]['usd']

            # Calculate price delta
            price_diff = close_price / old_price[4]

            # Store coin/delta/bought price
            coin_data[coin] = [price_diff, close_price]

            # print(f"--Checking=<{coin: <10}> --- ${round(old_price[4],5): <10}/${round(close_price,5): <10} ({round(price_diff,5): <10}%)")

        # Get  min difference coin
        price_diff_min_id = get_min(coin_data)
        _pot_coin_id = price_diff_min_id
        _pot_coin_price = coin_data.get(_pot_coin_id)[1]
        _pot_coin_delta = coin_data.get(_pot_coin_id)[0]

        # print(f"----Minimum delta=<{_pot_coin_id}> --- ${round(_pot_coin_price,5)} ({round(_pot_coin_delta,5)}%)")

        # Already bought coin
        if _holding_coin:
            # _min_curr_diff = coin_data.get(_cur_coin_id)[0]
            # Calculate current coin price change reference
            global cur_coin_id
            global cur_coin_price
            global cur_coin_vol
            
            current_price = coin_data.get(cur_coin_id)[1]
            current_delta = current_price / cur_coin_price

            # print(f'----check held_coin={cur_coin_id}, cur_price={current_price}, held_delta={current_delta}, pot_coin={_pot_coin_id}, pot_delta={_pot_coin_delta}')
            # Check if potential coin is the same one we already bought
            if not cur_coin_id == _pot_coin_id and current_delta > _pot_coin_delta:
                # Found a new coin, sell current coin
                _holding_coin = False
                sell(cur_coin_id, cur_coin_vol, current_price)
            # Current coin is still the lowest
            else:
                print(f'Heartbeat -- {cur_coin_id} is still the lowest || Current:<{cur_coin_id}>({round(current_delta,5)}%), Potential:<{_pot_coin_id}>({round(_pot_coin_delta,5)}%)')

        if not _holding_coin:
            # buying coin
            _holding_coin = True
            # print(f'-------- Buying {_pot_coin_id} at {_pot_coin_price}')
            buy(_pot_coin_id, _pot_coin_price)

        if run_counter >= ITERATIONS:
            state = "stopped"
        run_counter += 1

        coin_data.clear()
        time.sleep(SLEEP_TIME)
    wallet_balance = get_balance
    global gala_orig,gala_last,shiba_orig,shiba_last,cardano_orig,cardano_last,ripple_orig,ripple_last,algo_orig,algo_last,uni_orig,uni_last
    print(f'Overall performance: {((wallet_balance - _original_wallet) / _original_wallet) * 100}%. Wallet: {wallet_balance}')
    print(f'gala={round(gala_last,4)}/{round(gala_orig,4)}({gala_last/gala_orig}),\
            shiba-inu={round(shiba_last,4)}/{round(shiba_orig,4)}({shiba_last/shiba_orig}),\
            cardano={round(cardano_last,4)}/{round(cardano_orig,4)}({cardano_last/cardano_orig}),\
            ripple={round(ripple_last,4)}/{round(ripple_orig,4)}({ripple_last/ripple_orig}),\
            algorand={round(algo_last,4)}/{round(algo_orig,4)}({algo_last/algo_orig}),\
            uniswap={round(uni_last,4)}/{round(uni_orig,4)}({uni_last/uni_orig})')

def buy(id, price):
    global cur_coin_id, cur_coin_price, cur_coin_vol
    global gala_orig,gala_last,shiba_orig,shiba_last,cardano_orig,cardano_last,ripple_orig,ripple_last,algo_orig,algo_last,uni_orig,uni_last

    cur_coin_id = id
    cur_coin_price = price

    wallet_balance = get_balance()
    bought_volume = wallet_balance / price
    cur_coin_vol = bought_volume

    match id:
        case "gala":
            if gala_orig == 0:
                gala_orig = bought_volume
            else:
                gala_last = bought_volume
                print(f'{gala_last}/{gala_orig}({gala_last/gala_orig}%)')
        case "shiba-inu":
            if shiba_orig == 0:
                shiba_orig = bought_volume
            else:
                shiba_last = bought_volume
                print(f'{shiba_last}/{shiba_orig}({shiba_last/shiba_orig}%)')
        case "cardano":
            if cardano_orig == 0:
                cardano_orig = bought_volume
            else:
                cardano_last = bought_volume
                print(f'{cardano_last}/{cardano_orig}({cardano_last/cardano_orig}%)')
        case "ripple":
            if ripple_orig == 0:
                ripple_orig = bought_volume
            else:
                ripple_last = bought_volume
                print(f'{ripple_last}/{ripple_orig}({ripple_last/ripple_orig}%)')
        case "algorand":
            if algo_orig == 0:
                algo_orig = bought_volume
            else:
                algo_last = bought_volume
                print(f'{algo_last}/{algo_orig}({algo_last/algo_orig}%)')
        case "uniswap":
            if uni_orig == 0:
                uni_orig = bought_volume
            else:
                uni_last = bought_volume
                print(f'{uni_last}/{uni_orig}({uni_last/uni_orig}%)')

    print(f'Wallet: ${round(wallet_balance, 3)}. Bought {round(bought_volume, 6)} of <{id}> at ${round(price, 5)}')

def sell(id, bought_vol, sold_price):
    # Found a new coin, sell current coin
    update_wallet(bought_vol * sold_price)
    wallet = get_balance()
    print(f'Wallet: ${round(wallet, 3)}. Sold {round(bought_vol, 6)} of <{id}> at ${round(sold_price,5)}')


def update_wallet(amount):
    global wallet
    wallet = amount

def get_balance():
    global wallet
    return wallet

def get_min(dict):
    min = 0
    id = ''
    for x in dict:
        if min == 0:
            min = dict.get(x)[0]
            id = x
        else:
            if dict.get(x)[0] < min:
                min = dict.get(x)[0]
                id = x

    return id



if __name__ == "__main__":
    main()


