# blockchain-market is an experiment in creating a private blockchain and
# building a market on top of it.
# Copyright (C) 2021  Tim Krull tkrull@purdue.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This is the prject's main .py file

# imports
import secrets
import json
from os import getcwd
from web3 import Web3
from eth_account import Account
from solc import compile_standard

# constants
HEX_DIGITS = 32     # number of digits for random hex nums
MIN_ACCTS = 16      # minimum number of accounts to have active
START_BAL = 100      # amount to start accounts off with


# creates dummy users and adds their accounts to the blockchain
# Inputs:
#   - start: int to start indexing users at
#   - num: number of accounts to generate
# Outputs: user keyfiles
def populate_users(start, num):
    # create some hex values to use to generate account keys/addresses
    ex_entropy = [str(secrets.token_hex(HEX_DIGITS)) for
                  i in range(start, num)]

    # create some identifiers for users' keyfiles
    usernames = ['user' + str(x) for x in range(start, num)]

    # generate [num] user accounts, encrypt them, then write them to a keyfile
    # to add them to the blockchain
    for usr in range(num):
        usr_acct = Account.create(ex_entropy[usr])
        encrypted = usr_acct.encrypt(password='password')
        fn = 'Blockchain/keystore/' + usernames[usr] + '-keyfile'
        with open(fn, 'w') as kf:
            kf.write(json.dumps(encrypted))


# sets the default account to use for chain transactions
# Input:
#   - acct_index: the index of the account in X.eth.accounts to use
def set_default_account(acct_index):
    gNode.eth.defaultAccount = gNode.eth.accounts[acct_index]


# simulates activity on the blockchain
def simulate():
    print('Entering simulate()\n')

    gNode.geth.miner.start(4)

    seed_accounts = False
    for account in gNode.eth.accounts:
        if Web3.fromWei(gNode.eth.getBalance(account), 'ether') < START_BAL:
            seed_accounts = True
            break
    if seed_accounts:
        while(Web3.fromWei(gNode.eth.getBalance(gNode.eth.accounts[0]),
              'ether') < (len(gNode.eth.accounts) * START_BAL)):
            # do nothing until default account has enough to seed others
            continue

    gNode.geth.miner.stop()

    # gNode.geth.personal.unlock_account(gNode.eth.accounts[0], 'user0pass', 0)

    # seed other accounts
    for i in range(1, len(gNode.eth.accounts)):
        gNode.eth.sendTransaction({'to': gNode.eth.accounts[i],
                                  'value': START_BAL})

    # start miner
    gNode.geth.miner.start(4)

    # read in commands and execute them
    with open('commands.txt', 'r') as fin:
        for command in fin:
            command = command.strip().split(sep=',')
            print('current command line:')
            print(command)
            if command[0] == 'purchase':
                print('Executing purchase transaction\n')
                set_default_account(int(command[2]))
                th = sale_listing.functions.purchase.value(
                    int(command[1]))().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'getPrice':
                print('Executing getPrice transaction\n')
                set_default_account(int(command[1]))
                th = sale_listing.functions.getPrice().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'describe':
                print('Executing describe transaction\n')
                set_default_account(int(command[1]))
                th = sale_listing.functions.describe().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'timesBought':
                print('Executing timesBought transaction\n')
                set_default_account(int(command[1]))
                th = sale_listing.functions.timesBought().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'getBalance':
                print('Executing getBalance transaction\n')
                set_default_account(int(command[1]))
                th = sale_listing.functions.getBalance().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'transferETH':
                print('Executing transferETH transaction\n')
                set_default_account(int(command[2]))
                th = sale_listing.functions.transferETH(
                    int(command[1])).transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'updatePrice':
                print('Executing updatePrice transaction\n')
                set_default_account(int(command[2]))
                th = sale_listing.functions.updatePrice(
                    int(command[1])).transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'takeOffMarket':
                print('Executing takeOffMarket transaction\n')
                set_default_account(int(command[1]))
                th = sale_listing.functions.takeOffMarket().transact()
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(gNode.eth.getTransactionReceipt(tr))
            elif command[0] == 'send':
                print('Executing send transaction\n')
                th = gNode.eth.sendTransaction({'to': int(command[2]),
                                                'from': int(command[1]),
                                                'value': int(command[3])})
                tr = gNode.eth.waitForTransactionReceipt(th)
                print(json.loads(gNode.eth.getTransactionReceipt(tr)))

    # stop miner
    gNode.geth.miner.stop()


# compile the contract defined using Solidity
# Input:
#   - fn: the name of the json file containing the contract definition
# Returns: a contract object
def compile_contract(fn):
    code = ""

    # open the json file and read it in
    with open(fn, 'r') as file:
        code = json.load(file)

    # compile the Solidity code
    comp_sol = compile_standard(code,
                                allow_paths=getcwd())

    # get the bytecode for the compiled Solidity code
    bytecode = comp_sol['contracts']['SaleListing.sol']['SaleListing']['evm']['bytecode']['object']

    # get the bytecode for the compiled Solidity code
    abi = json.loads(comp_sol['contracts']['SaleListing.sol']['SaleListing']['metadata'])['output']['abi']

    return gNode.eth.contract(abi=abi, bytecode=bytecode)


# prints info about the current state of the chain
def print_info():
    # output if connected to the geth node
    print("Node Connected: " + str(gNode.isConnected()) + "\n")

    # print info on latest block
    print("Details of latest block:")
    print(json.dumps(json.loads(Web3.toJSON(gNode.eth.get_block('latest'))),
                     indent=4, sort_keys=True) + '\n')

    # print user addresses
    print("Current Account Addresses:")
    for acct in gNode.eth.accounts:
        output = 'address: ' + acct + '\tbalance:' + str(Web3.fromWei(
                                                        gNode.eth.getBalance(
                                                         gNode.eth.accounts[0]
                                                         ), 'ether'))
        print(output)
    # print a blank line
    print()


# IPC Provider
gNode = Web3(Web3.IPCProvider('~/Library/Ethereum/geth.ipc'))

if (len(gNode.eth.accounts) < MIN_ACCTS):
    populate_users(len(gNode.eth.accounts), MIN_ACCTS)

# set the first account as the default account
set_default_account(0)

for i in range(len(gNode.eth.accounts)):
    gNode.geth.personal.unlock_account(gNode.eth.accounts[i],
                                       'password', 0)

# get the compiled contract
SaleListing = compile_contract('contract.json')

# Submit the transaction that deploys the contract
trans_hash = SaleListing.constructor("testaddress", 5,
                                     "Test Description").transact()
# start up miner with 4 threads
gNode.geth.miner.start(4)

# Wait for the transaction to be mined, and get the transaction receipt
trans_receipt = gNode.eth.waitForTransactionReceipt(trans_hash)

sale_listing = gNode.eth.contract(address=trans_receipt.contractAddress,
                                  abi=SaleListing.abi)

# call a contract function
sale_listing.functions.describe().call()

# stop the miner
gNode.geth.miner.stop()

simulate()
print_info()
