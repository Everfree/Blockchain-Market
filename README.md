# Blockchain Market
Experimental project for working with Ethereum based private blockchain and creating a marketplace on top of it.

# The Blockchain
For this project, I am using Ethereum's 'Go Ethereum' aka 'geth' to create a private blockchain to experiment on.

# The Contract
I am implementing a smart contract on the blockchain that allows for the sale of digitial assets, primarily targeting digital art, 3D models, and AR effects,
though this can be expanded to any kind of digital content.

## The Twist
The twist to the smart contract initially being tested is that a buyer may pay the current price of an asset being sold, or they may opt to pay more than the
current set price. If they pay more, the current price is changed to the higher amount paid, and all future buyers must pay at least that price. This system
allows buyers to increase the exclusivity of items to make them 'rare' or at least limited to those willing to pay the higher price.
