
These scripts are meant to setup the private blockchain locally. They were written for use on macOS. Remember to give them permission to execute by running "chmod +x [script-filename]"

*****IMPORTANT*****
These scripts require the geth (Go Ethereum) executable be located 1 level up in the directory. Geth can be downloaded here: https://geth.ethereum.org/downloads/

*****WARNING*****
The scripts in this folder are meant to be run from this folder, i.e. do NOT move them into another folder, they will not be able to find their targets.

*****Script Descriptions*****

This section describes the scripts in the order they should be run in. The node and console scripts should be run in seperate terminals simultaneously.

geth-init.bash - this initializes the private blockchain. it requires the geth executable along with its config file named geth-init.json be located 1 level up in the directory and creates the blockchain in a folder called Blockchain located 1 level up in directory. Run this ONCE only.

run-geth-node.bash - this starts the geth executable running the private blockchain with network ID 343 on port 34343 using IPC protocol. It looks in the Blockchain folder located 1 level up in the directory for the blockchain data. Run this anytime you need to start up the geth node.

run-geth-console.bash - this starts the geth console and attaches it to the geth node running on the IPC address run-geth-node.bash started it on. Run this anytime you need to launch the geth console. ***Will work IFF the geth node is running.***
