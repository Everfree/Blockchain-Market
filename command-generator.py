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

# This file generates commands to simulate activity on the blockchain.
# It takes a two arguements: the number of commands to generate and the
# number of accounts on the blockchain

# imports
import random
import sys

# list of possible commands
COMMANDS = ['purchase', 'getPrice', 'describe', 'timesBought', 'getBalance',
            'transferETH', 'updatePrice', 'takeOffMarket', 'send']
# minimum price for a SaleListing
MIN = 2
# maximum price for a SaleListing
MAX = 16

# check for proper input
if len(sys.argv) != 3:
    print("Enter two arguments, each an integer specifying the number of\
 commands to generate and the number of accounts on the blockchain")
    sys.exit(1)
elif int(sys.argv[1]) <= 0 or int(sys.argv[2]) <= 0:
    print("Both arguments must be integers greater than 0")
    sys.exit(1)

# pseudorandomly generate commands to be executed,
# along with any needed arguments
output = ''
for i in range(int(sys.argv[1])):
    command = random.choice(COMMANDS)
    if command == 'purchase':
        output += command + ', ' + str(random.randint(MIN, MAX)) +\
            ', ' + str(random.randrange(1, int(sys.argv[2]))) + '\n'
    elif command == 'getPrice':
        output += command + ', ' +\
            str(random.randrange(int(sys.argv[2]))) + '\n'
    elif command == 'describe':
        output += command + ', ' +\
            str(random.randrange(int(sys.argv[2]))) + '\n'
    elif command == 'timesBought':
        output += command + ', ' +\
            str(random.randrange(int(sys.argv[2]))) + '\n'
    elif command == 'getBalance':
        output += command + ', ' +\
            str(0) + '\n'
    elif command == 'transferETH':
        output += command + ', ' + str(random.randint(MIN, MAX)) +\
            ', ' + str(0) + '\n'
    elif command == 'takeOffMarket':
        output += command + ', ' +\
            str(0) + '\n'
    elif command == 'send':
        sender = random.randrange(int(sys.argv[2]))
        reciever = random.randrange(int(sys.argv[2]))
        while (sender == reciever):
            reciever = random.randrange(int(sys.argv[2]))
        output += command + ', ' + str(sender) + ', ' + str(reciever) + \
            ', ' + str(random.randint(MIN, MAX)) + '\n'

# write to file
with open('commands.txt', 'w') as fout:
    fout.write(output)
