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
from web3 import Web3
from eth_account import Account

# constants
HEX_DIGITS = 32
NUM_USERS = 16


# creates dummy users and adds their accounts to the blockchain
def populateUsers(start, num):
    # create some hex values to use to generate account keys/addresses
    ex_entropy = [str(secrets.token_hex(HEX_DIGITS)) for
                  i in range(start, num)]

    # create some identifiers for users' keyfiles
    usernames = ['user' + str(x) for x in range(start, num)]

    # generate [num] user accounts, encrypt them, then write them to a keyfile
    # to add them to the blockchain
    for usr in range(num):
        usr_acct = Account.create(ex_entropy[usr])
        encrypted = usr_acct.encrypt(password=str(usernames[usr] + 'pass'))
        fn = 'Blockchain/keystore/' + usernames[usr] + '-keyfile'
        with open(fn, 'w') as kf:
            kf.write(json.dumps(encrypted))


# IPC Provider
gNode = Web3(Web3.IPCProvider('/Users/tkrull/Library/Ethereum/geth.ipc'))

# check connection
print(gNode.isConnected())

# get info on latest block
print(gNode.eth.get_block('latest'))

if (len(gNode.eth.accounts) < NUM_USERS):
    populateUsers(len(gNode.eth.accounts), NUM_USERS)
