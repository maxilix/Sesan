import	json
import	server
import	threading
import 	math


from	settings		import	*

import 	geth

import	server_managment
import	server_contract

import	server_tools	as 		tools
from	server_tools	import	console

import 	spy_PoRX
import 	spy_eigenTrust


import	debug




#################################   SYSTEM   ###################
def exit():
	comfirm = (input("please use secure_exit() [y/n] : ") == "y")
	if comfirm:
		tools.secure_exit()
################################################################



#################################   DISPLAY   ##################
def help():
	print("not implement")


def print_configuration():
	print(json.dumps(tools.conf, indent=2))


def print_clients(hashOrId = None, full=False):
	if (hashOrId != None):
		clients = server_managment.client_match(hashOrId)
		if (clients == -1):
			print("aborted")
			return
	else:
		clients = tools.clients

	if (len(clients) == 0):
		print("void")
		return
	for c in clients:
		print(c)
		print("\tid                " + str(tools.clients[c]["id"]))
		if (full):
			print("\tsocket            " + str(tools.clients[c]["socket"]))
		else:
			print("\tsocket            " + str(tools.clients[c]["socket"])[:64] + "...")
		print("\ttimestamp         " + str(tools.clients[c]["timestamp"]))			
		print("\tip                " + "".join(str(x)+'.' for x in tools.clients[c]["ip"])[:-1])
		print("\tpyPort            " + str(tools.clients[c]["pyPort"]))
#		print("\tgethPort          " + str(tools.clients[c]["gethPort"]))
		if (full):
			print("\tenodeString       " + str(tools.clients[c]["enodeString"]))
		else:
			print("\tenodeString       " + str(tools.clients[c]["enodeString"])[:64] + "...")
		print("\tpeerable          " + str(tools.clients[c]["peerable"]))
		print("\taddressString     " + str(tools.clients[c]["addressString"]))
		print("\tisValidAddress    " + str(tools.clients[c]["isValidAddress"]))
		print()
	print()


def print_trust():
	"""
	check
	"""
	users = tools.eigenTrust.functions.get_users().call()
	t = spy_eigenTrust.get_normalize_global_trust_matrix()
	n = len(users)

	z = list(zip(range(n),users,t))
	print("  id                                      address     trust")
	for user in sorted(z , key=lambda t: t[2], reverse=True):
		print("{0:4} - {1} : {2:7.2f}".format(user[0], user[1], user[2]*1000))
################################################################





#################################   SERVER   ###################
def close_client_connexion(hashOrId = None):
	clients = server_managment.client_match(hashOrId)
	if (clients == -1):
		return

	if (len(clients)==0):
		print("no client match")
		return

	print("{0} client{1} match".format(len(clients) , ("","s")[len(clients)>=2] ))
	for c in clients:
		print("\t" + c)
	confirm = input("comfirm close [y/n] : ") == "y"
	if (confirm):
		for c in clients:
			server_managment.close_connexion(c)
	else:
		print("aborted")


def server(status):
	if type(status) != bool:
		print("bool value needed")
		print("aborted")
		return

	if (status):
		for t in threading.enumerate():
			if t.name == "serverThread":
				print("server already started")
				return
		server_managment.enable_server()
	else:
		for t in threading.enumerate():
			if t.name == "serverThread":
				server_managment.disable_server()
				return
		print("server already stopped")
################################################################



#################################   TOOLS   ####################
def change_verbosity(newVerbosity):
	if (newVerbosity>=0 and newVerbosity<=6):
		tools.verbosity = v
	else:
		print("aborted")
################################################################



#################################   GETH   #####################
def mine(status):
	if (status == True):
		th = 1
	elif (type(status) == int and status >= 0):
		th = status
	elif (status == False):
		th = 0
	else:
		console(LOG_FLAG_WARN, "wrong argument for mine(status), bool or positive integer")
		return

	if (th > 0):
		tools.w3.geth.miner.start(min(th,GETH_MAX_MINING_THREAD))
	else:
		tools.w3.geth.miner.stop()

def unlock(s = 3600):
	geth.unlock_coinbase(s)
################################################################



#################################   EIGENTRUST   ###############
def eigenTrust_add(i): # must be private in contract
	confirm = input("Add " + str(tools.w3.eth.accounts[i]) + " [y/n] : ") == 'y'
	if (confirm):
		tools.eigenTrust.functions.add_user(tools.w3.eth.accounts[i]).transact()
	else:
		print("aborted")


def eigenTrust_vote(i,v=True):
	if (v):
		confirm = input("Vote for " + str(tools.w3.eth.accounts[i]) + " [y/n] : ") == 'y'
	else:
		confirm = input("Vote against " + str(tools.w3.eth.accounts[i]) + " [y/n] : ") == 'y'

	if (confirm):
		tools.eigenTrust.functions.vote(tools.w3.eth.accounts[i],v).transact()
	else:
		print("aborted")


def eigenTrust_get_trust():
	return spy_eigenTrust.get_normalize_global_trust_matrix()
	

def eigenTrust_add_preTrusted(i):
	confirm = input("Add " + str(tools.w3.eth.accounts[i]) + " as preTrusted [y/n] : ") == 'y'
	if (confirm):
		tools.eigenTrust.functions.add_preTrusted(tools.w3.eth.accounts[i]).transact()
	else:
		print("aborted")


def eigenTrust_set_alpha(alpha):
	if (alpha < 0 or alpha > 1):
		print("alpha must be in [0;1]")
		return

	if   (alpha == 0):
		tools.eigenTrust.functions.set_alpha(0).transact()
	elif (alpha == 1):
		tools.eigenTrust.functions.set_alpha(2**256 - 1).transact()
	else:
		tools.eigenTrust.functions.set_alpha(math.floor(alpha * (2**256))).transact()

################################################################













print("\n\n\n")
print("Welcome to the server management console")
print("- Use help() to see informations")
print("- Use 'tail -f ./eth_{0}/{1}' in an other terminal to see server log".format(tools.nodeName,LOG_SERVER_FILENAME))
print("- Use 'tail -f ./eth_{0}/{1}' in an other terminal to see geth log".format(tools.nodeName,LOG_GETH_FILENAME))
print("- Use 'geth --datadir ./eth_{0}/ attach' in an other terminal to use JS console".format(tools.nodeName))