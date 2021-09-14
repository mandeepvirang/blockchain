Backend Functionalities::\
\
Blockchain() :\
	1. has a array of blocks  
	2. has a dictionary of all the unspent transactions  
	3. creates a genisis block  
  
Wallet() : Creates a wallet   
	1. has a private key  
	2. has a public key  
	3. has a dictionary of unspent transaction outputs  
  
Block(previousBlock.hash) : creates a block of blockchain  
	1. keeps previous block's hash  
	2. has a timestamp  
	3. keeps a array of all the transactions  
  
WalletA.sendFund(WalletB.publicKey,value) : tries to send coins from walletA to walletB, returns a transaction   
	1. calls WalletA.getBalance() :  gets balance of walletA  
		1. for all UTXOs(unspent transaction outputs) in blockchain, checks if it blongs to the same wallet, if yes, add it to the dictionary of the    wallet and counts total balance.  
	2. for all UTXOs in wallet, takes some UTXOs such that their sum is greater than the value and adds them to the inputs array  
	3. calls Transaction(self.publicKey,recipient,value,inputs) : makes a transaction  
		1. has a unique id/hash  
		2. stores all variables and make a empty outputs array	  
	4. signs the transaction by walletA's private key  
	5. deletes all the spent TXOs from self.UTXOs  
	6. returns newTransaction  
  
block.addTransaction(WalletA.sendF...) : adds transaction to the block  
	1. calls transaction.processTransaction() : processes transaction  
		1. verifies transaction's signature  
		2. for all input transactons for this transactoin, update input UTXOs's value from Blockchain.UTXOs  
		3. calls getInputsValue() : get total value of input TXs  
		4. makes transaction to recipirnt of input value and another transaction to self of leftover value  
		5. adds these tranactions to the output array  
		6. also adds them to the Blockchain.UTXOs  
		7. delets all the input TXs from Blockchain.UTXOs  
	2. adds the transaction to the transactions array  

Blockchain.addBlock(block) : adds block to the blockchain array  
	1. calls block.mineBlock(difficulty)  
		1. calls getMerkleRoot(self.transactions) : gets merkle's root  
		2. find a hash string which starts with specific zeros(equals to the difficulty)  
		3. updates the hash/id and the nonce  
	2. adds it to the blockchain   
  
isChainValid() : checks if the blockchain is valid  


Frontend Functionalities  
Routes:  
    1) / : home  
    2) /blockchain : displays complete blockchain  
    3) /blockchain/<index>: displays all tranactions for block number <index>  
    4) /wallet : shows balance and form to make any tranactions  
    5) /mine : to mine new block to add current tranactions to blockchain  
    6) /isValid : to check if current chain is valid or not   
    7) /connect : to connect with peers  
    8) /mykeys : to generate publicKey and privateKey and save them in file  
    9) /about : shows info about team  
