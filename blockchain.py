from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import Crypto.Hash
from hashlib import sha256
import time
<<<<<<< HEAD
#from Crypto.PublicKey import ECC
=======
from Crypto.PublicKey import ECC
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
MAX_NONCE = 1000000000

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def apply_ecdsa(privateKey,text):
    text = bytes(text, 'utf-8')
    h = Crypto.Hash.SHA256.new(text)
    signer = DSS.new(privateKey,'fips-186-3')
    signature = signer.sign(h)
    return signature

def verify_ecdsa(publicKey,text,signature):
    text = bytes(text, 'utf-8')
    h = Crypto.Hash.SHA256.new(text)
    verifier = DSS.new(publicKey,'fips-186-3')
    try:
        verifier.verify(h,signature)
        return True
    except ValueError:
        return False

class Block:
    #transactions = []
    #markleRoot = ""
    def __init__(self, previousHash):
        #self.data = data
        self.previousHash = previousHash
        self.timeStamp = str(time.time())
        self.Hash=""
        self.nonce=0
<<<<<<< HEAD
        self.merkleRoot=""
=======
        self.markleRoot=""
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
        self.transactions = []
        #self.calculateHash()
    


    def calculateHash(self):
        calculatedHash = SHA256(str(self.previousHash) + self.timeStamp + str(self.nonce) + self.merkleRoot)
        self.Hash = calculatedHash
        return calculatedHash
   
    def mineBlock(self,difficulty):
        self.merkleRoot = getMerkleRoot(self.transactions)
        prefixStr = difficulty*'0'
        for nonce in range(MAX_NONCE):
            self.nonce=nonce
            Hash = self.calculateHash()
            #text = str(self.previousHash) + self.timeStamp + str(nonce) + self.data
            #Hash = SHA256(text)
            if Hash.startswith(prefixStr):
                print("Block mined with Hash : "+ Hash)
                self.Hash=Hash
                self.nonce = nonce
                return
    
    def addTransaction(self,transaction):
        if(transaction == None ):
            return False
        if self.previousHash != "0":
            if transaction.processTransaction() == False:
                print("Transaction failed to process. Discarded.")
                return False
        self.transactions.append(transaction)
        print("Transaction added to Block successfully!")
        return True



class Wallet():
    def __init__(self):
        self.privateKey = ECC.generate(curve='P-256')
        self.publicKey = self.privateKey.public_key()
        self.UTXOs = {}

    def getBalance(self):
<<<<<<< HEAD
        total = 0
=======
        total = 0;
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
        for i in Blockchain.UTXOs.values() :
            UTXO = i
            if (UTXO.isMine(self.publicKey)) :
                self.UTXOs[UTXO.id] = UTXO
                total+=UTXO.value
        return total

    def sendFunds(self,recipient,value):
        if(self.getBalance()<value):
            print("Not enough funds to send transaction. Transaction discarded")
            return None
        inputs = []
        total=0
        for i in self.UTXOs.values():
            UTXO = i
            total+=UTXO.value
            inputs.append(TransactionInput(UTXO.id))
            if(total > value):
                break
        newTransaction = Transaction(self.publicKey,recipient,value,inputs)
        newTransaction.sign(self.privateKey)

        for i in inputs:
            del self.UTXOs[i.transactionOutputId]
                #UTXOs.remove(i.trasactionOutputId)#remove it

        return newTransaction

def getMerkleRoot(transactions):
    count = len(transactions)
    previousTreeLayer = []
    for transaction in transactions:
        previousTreeLayer.append(transaction.transactionId)
    treeLayer = previousTreeLayer
    while count > 1 :
        treeLayer = []
        for i in range(1,len(previousTreeLayer),2):
            treeLayer.append(SHA256(str(previousTreeLayer[i-1])+str(previousTreeLayer[i])))
        count = len(treeLayer)
        previousTreeLayer = treeLayer
    if len(treeLayer) == 1 :
        return treeLayer[0]
    else :
        return ""


class Transaction():
    sequence = 0
    def __init__(self,sender,reciepient,value,inputs):
        self.sender = sender
        self.reciepient = reciepient
        self.value = value
        self.inputs = inputs
        self.outputs = []
        #self.sequence=0
        self.transactionId = self.calculateHash()
        self.signature = None

    def calculateHash(self):
        Transaction.sequence+=1
        data = str(self.sender)+str(self.reciepient)+str(self.value)+str(Transaction.sequence)
        return SHA256(data)

    def sign(self,privateKey):
        data = str(self.sender)+str(self.reciepient)+str(self.value)
        self.signature = bytes(apply_ecdsa(privateKey,data))
        
    def verify(self):
        data = str(self.sender)+str(self.reciepient)+str(self.value)
        return verify_ecdsa(self.sender,data,self.signature)

    def processTransaction(self):
        if self.verify()==False :
            print("transaction signature failed to varify\n")
            return False
        
        for i in self.inputs :
            i.UTXO = Blockchain.UTXOs[i.transactionOutputId]

        if self.getInputsValue() < Blockchain.minimumTransaction :
            print("Transaction input too small\n")
            return False
        
        leftover = self.getInputsValue() - self.value
        self.transactionId = self.calculateHash()
        self.outputs.append(TransactionOutput(self.reciepient,self.value,self.transactionId))
        self.outputs.append(TransactionOutput(self.sender,leftover,self.transactionId))

        for o in self.outputs :
            Blockchain.UTXOs[o.id] = o #add it
        for i in self.inputs :
            if(i.UTXO.id == None):
                continue
            del Blockchain.UTXOs[i.UTXO.id]

        return True

    def getInputsValue(self):
        total = 0
        for i in self.inputs :
            if not(i.UTXO):
                continue
            total+=i.UTXO.value
        return total

    def getOutputsValue(self):
        total = 0
        for o in self.outputs :
            total+=o.value
        return total



class TransactionOutput():
    def __init__(self,reciepient,value,parentTransactionId):
        self.reciepient = reciepient
        self.value = value
        self.parentTransactionId = parentTransactionId
        self.id = SHA256(str(self.reciepient)+str(self.value)+str(self.parentTransactionId))

    def isMine(self,publicKey):
        return self.reciepient==publicKey

<<<<<<< HEAD
=======


>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
class TransactionInput():
    def __init__(self,transactionId):
        self.transactionOutputId=transactionId
        self.UTXO = None
    
<<<<<<< HEAD
=======


>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
class Blockchain:
    blockchain = []
    UTXOs = {}
    minimumTransaction = float(0.1)
<<<<<<< HEAD
    difficulty = 5
    def __init__(self, wallet):
        coinbase = Wallet()
        WalletA = wallet
        #WalletB = Wallet()
=======
    difficulty = 4;
    def __init__(self):

        coinbase = Wallet()
        WalletA = Wallet()
        WalletB = Wallet()
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96

        self.genesisTransaction = Transaction(coinbase.publicKey,WalletA.publicKey,100,0)
        self.genesisTransaction.sign(coinbase.privateKey)
        self.genesisTransaction.transactionId = "0"
        self.genesisTransaction.outputs.append(TransactionOutput(self.genesisTransaction.reciepient,self.genesisTransaction.value,self.genesisTransaction.transactionId))
        Blockchain.UTXOs[self.genesisTransaction.outputs[0].id] = self.genesisTransaction.outputs[0]

        print("Creating and Mining Genesis block...")
        genesis = Block("0")
        genesis.addTransaction(self.genesisTransaction)
        self.addBlock(genesis)

<<<<<<< HEAD
=======
        b1 = Block(genesis.Hash)
        print("WalletA's balance is : " + str(WalletA.getBalance()))
        #b1.addTransaction(WalletA.sendFunds(WalletB.publicKey,10))
        b1.addTransaction(WalletA.sendFunds(WalletB.publicKey,40))
        #b1.addTransaction(Transaction(WalletA.publicKey,WalletB.publicKey,40,WalletA.inputs))
        #self.addBlock(b1)
        print("WalletA's balance is : " + str(WalletA.getBalance()))
        print("WalletB's balance is : " + str(WalletB.getBalance()))
        b1.addTransaction(WalletA.sendFunds(WalletB.publicKey,10))
        b1.addTransaction(WalletB.sendFunds(WalletA.publicKey,1))
        b1.addTransaction(WalletB.sendFunds(WalletA.publicKey,5))
        print("WalletA's balance is : " + str(WalletA.getBalance()))
        print("WalletB's balance is : " + str(WalletB.getBalance()))
        self.addBlock(b1)

        b2 = Block(b1.Hash)
        b2.addTransaction(WalletB.sendFunds(WalletA.publicKey,100))
        b2.addTransaction(WalletB.sendFunds(WalletA.publicKey,5))
        print("WalletA's balance is : " + str(WalletA.getBalance()))
        print("WalletB's balance is : " + str(WalletB.getBalance()))
        b2.addTransaction(WalletA.sendFunds(WalletB.publicKey,10))
        print("WalletA's balance is : " + str(WalletA.getBalance()))
        print("WalletB's balance is : " + str(WalletB.getBalance()))
        #self.addBlock(b2)

        self.isChainValid()


>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
#        self.difficulty = 4
#        #self.blockchain = []
#        for i in range(1):
#            if i==0:
#                b = Block("Genesis block!",0)
#                print("Mining Genesis block...")
#                b.mineBlock(self.difficulty)
#                Blockchain.blockchain.append(b)
#            else:
#                b = Block("This is block number "+str(i+1),Blockchain.blockchain[i-1].Hash)
#                print("Mining block number "+str(i+1)+"...")
#                b.mineBlock(self.difficulty)
#                Blockchain.blockchain.append(b)
#        print(Blockchain.blockchain)
#        print("Blockchain is valid "+str(self.isChainValid()))
#        walletA = Wallet()
#        walletB = Wallet()
#        print(walletA.publicKey)
#        print(walletA.privateKey)
#        transaction = Transaction(walletA.publicKey,walletB.publicKey,5,0)
#        transaction.sign(walletA.privateKey)
#        print("Is signature verified : "+ str(transaction.verify()))


    def isChainValid(self):
<<<<<<< HEAD
        currentBlock = self.blockchain[0]
        previousBlock = self.blockchain[0]
=======
        currentBlock = Blockchain.blockchain[0]
        previousBlock = Blockchain.blockchain[0]
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
        prefixStr = self.difficulty*'0'
        tempUTXOs = {}
        tempUTXOs[self.genesisTransaction.outputs[0].id] = self.genesisTransaction.outputs[0]

        for i in range(1,len(self.blockchain)):
<<<<<<< HEAD
            currentBlock = self.blockchain[i]
            previousBlock = self.blockchain[i-1]
=======
            currentBlock = Blockchain.blockchain[i]
            previousBlock = Blockchain.blockchain[i-1]
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
            #print(currentBlock.Hash)
            #print(currentBlock.calculateHash())
            #print(currentBlock.Hash)
            #print(currentBlock.calculateHash())
            if currentBlock.Hash != currentBlock.calculateHash():
                #print(currentBlock.Hash)
                #print(currentBlock.calculateHash())
                #print(currentBlock.Hash)
                #print(currentBlock.calculateHash())
                #print("Current Hashes not equal!")
                return False
            if currentBlock.previousHash != previousBlock.Hash:
                print("Previous Hashes not equal!")
                return False
            if not(currentBlock.Hash.startswith(prefixStr)):
                print("This block has not been mined!")
                return False

        for t in range(len(currentBlock.transactions)):
            currentTransaction = currentBlock.transactions[t]
            if currentTransaction.verify()==False:
                print("Signature of transaction "+str(t)+" is invalid")
                return False
            if(currentTransaction.getInputsValue()!=currentTransaction.getOutputsValue()):
                print("Inputs are not equal to outputs on transaction "+str(t))
                return False
            #print(tempUTXOs)
            for inp in currentTransaction.inputs:
                #tempOutput = tempUTXOs[i.transactionOutputId]
                #print(inp.transactionOutputId)
                if not(inp.transactionOutputId in tempUTXOs):
                    print("#Referenced input on Transaction(" + str(t) + ") is Missing")
                    return False
                tempOutput = tempUTXOs[inp.transactionOutputId]

                if(inp.UTXO.value != tempOutput.value):
                    print("#Referenced input on Transaction(" + str(t) + ") is Invalid")
                    return False
                del tempUTXOs[inp.transactionOutputId]

            for o in currentTransaction.outputs:
                tempUTXOs[o.id] = o

            if(currentTransaction.outputs[0].reciepient != currentTransaction.reciepient):
                print("#Transaction(" + str(t) + ") output reciepient is not who it should be")
                return False
            if(currentTransaction.outputs[1].reciepient != currentTransaction.sender):
                print("#Transaction(" + str(t) + ") output 'change' is not sender")
                return False

        print("Blockchain is valid.")
        return True

    def addBlock(self,newBlock):
<<<<<<< HEAD
        start_time = time.time()
        newBlock.mineBlock(Blockchain.difficulty)
        Blockchain.blockchain.append(newBlock)
        return (time.time()-start_time)
=======
        newBlock.mineBlock(Blockchain.difficulty)
        Blockchain.blockchain.append(newBlock)

#print(ECC.generate(curve='P-256'))
Blockchain();
>>>>>>> 6f9629b202a9b3f08576313c6165cd8e930ece96
