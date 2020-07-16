#!/usr/bin/python3

import solcx
import time



from settings import *

import server_managment

import server_tools as tools
from server_tools import console


"""
def deploy_contract(file_path, pulse_mining = False):

	compiled_sol = solcx.compile_files([source_path_file])
	contract_id, contract_interface = compiled_sol.popitem()
	tx_hash = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin']).constructor().transact()
	print("Transaction hash : " + str(tx_hash.hex()))

	if (pulse_mining):
		w3.geth.miner.start(1)
		print("Mining started, waiting for transaction validation...")
	else:
		print("Waiting for transaction validation...")

	while True:
		try:
			address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
			break
		except:
			time.sleep(1)

	if (pulse_mining):
		w3.geth.miner.stop()
		print("Mining stopped")

	return w3.eth.contract(address=address,abi=contract_interface['abi'])
"""

def init_contracts():
    


def deploy_intervention_manager():

    compiledInterventionManager = solcx.compile_files([CONTRACT_SOURCES_FOLDER + CONTRACT_IM_SOURCES_FILENAME])
    interventionManagerId, interventionManagerInterface = compiledInterventionManager.popitem()
    deployTransactionHash = w3.eth.contract(abi=interventionManagerInterface['abi'],bytecode=interventionManagerInterface['bin']).constructor().transact()

    console(LOG_FLAG_INFO, "intervention manager contract transaction sent, waiting validation")

    interventionManagerDeployWaitingThread = threading.Thread(target=deploy_waiting , name="interventionManager" , args=(deployTransactionHash, interventionManagerInterface['abi'], ), daemon=True)
    interventionManagerDeployWaitingThread.start()



def deploy_eigenTrust():
	if (tools.conf["geth"]["contract"]["eingenTrust"] != {}):
		console(LOG_FLAG_WARN, "eigenTrust contract already deployed at {}".format(tools.conf["geth"]["contract"]["eingenTrust"]["address"]))
		return False

	compiledEigenTrust = solcx.compile_files([CONTRACT_SOURCES_FOLDER + CONTRACT_EIGENTRUST_SOURCES_FILENAME])
	eigenTrustId, eigenTrustInterface = compiledEigenTrust.popitem()
	deployTransactionHash = w3.eth.contract(abi=eigenTrustInterface['abi'],bytecode=eigenTrustInterface['bin']).constructor().transact()

	console(LOG_FLAG_INFO, "eigenTrust contract transaction sent, waiting validation")

	eigenTrustDeployWaitingThread = threading.Thread(target=deploy_waiting , name="eigenTrust" , args=(deployTransactionHash, eigenTrustInterface['abi'], ), daemon=True)
	eigenTrustDeployWaitingThread.start()



def deploy_waiting(deployTransactionHash,abi)
	while True:
		try:
			address = tools.w3.eth.getTransactionReceipt(deployTransactionHash)['contractAddress']
			break
		except:
			time.sleep(1)
    if (threading.currentThread().name == "eigenTrust"):
        console(LOG_FLAG_INFO, "eigenTrust transaction validated", who="EigenTrust")
        tools.conf["geth"]["contract"]["eigenTrust"]["address"] = address
        tools.conf["geth"]["contract"]["eigenTrust"]["abi"] = abi
        tools.eigenTrust = tools.w3.eth.contract(address=address,abi=abi)
        console(LOG_FLAG_INFO, "eigenTrust fully deployed at {}".format(address), who="EigenTrust")

    elif (threading.currentThread().name == "interventionManager"):
        console(LOG_FLAG_INFO, "interventionManager transaction validated", who="InterManag'")
        tools.conf["geth"]["contract"]["interventionManager"].append({"address": address,"abi": abi})
        tools.interventionManager = .append(tools.w3.eth.contract(address=address,abi=abi))
        number = len(tools.interventionManager)
        if   (number%10 == 1 and number%100 != 11):
            sufixe = "st"
        elif (number%10 == 2 and number%100 != 12):
            sufixe = "nd"
        elif (number%10 == 3 and number%100 != 13):
            sufixe = "rd"
        else:
            sufixe = "th"
        console(LOG_FLAG_INFO, "{0}{1} interventionManager fully deployed at {2}".format(number, sufixe, address), who="InterManag'")

    else:
        console(LOG_FLAG_INFO, "{} transaction validated".format(threading.currentThread().name), who=threading.currentThread().name[:11])
	return 