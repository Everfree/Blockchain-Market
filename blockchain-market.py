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

# IPC Provider
gNode = Web3(Web3.IPCProvider('/Users/tkrull/Library/Ethereum/geth.ipc'))

# check connection
print(gNode.isConnected())

# get info on latest block
print(gNode.eth.get_block('latest'))
