from app import *

def getCustomerAllTurn():
	all_turn_user_id = []
	responseDict = {}
	#print("Consulta de todos los turnos para un determinado cliente")
	customerTurn = 'select rl.table_id, u.username, u.id, rl.number from requestlist rl '
	customerTurn += 'inner join users u on rl.user_id = u.id '
	customerTurn += 'where cust_name = "%s" ' % ('kairopy')
	customerTurn += 'and status = 0 '
	customerTurn += 'group by table_id '
	cturn = db.engine.execute(customerTurn)
	for row in cturn:
		all_turn_user_id.append(row.id)
		responseDict["%s-%s" % (row.table_id, row.id)] = [row.username, row.id, row.number]
	#print all_turn_user_id
	#print responseDict
	# print(','.join(map(str, all_turn_user_id)))
	#print("------------------------------------------\n")
	return ','.join(map(str, all_turn_user_id)), responseDict

def getMaxTurnfordealer(alldealer, responseDict):
	maxturnfordealerdic = {}
	#print("consulta de los ultimos turnos por comercio")
	maxTurnfordealer = 'select  user_id, max(number) as number from requestlist '
	maxTurnfordealer += 'where status > 1 '
	maxTurnfordealer += 'and user_id in (%s)' % alldealer
	maxTurnfordealer += 'group by user_id '
	mtd = db.engine.execute(maxTurnfordealer)
	for row in mtd:
		maxturnfordealerdic[str(row.user_id)] = row.number
	#print maxturnfordealerdic
	for k, v in responseDict.items():
		keys = k.split('-')
		if keys[1] in maxturnfordealerdic:
			values = responseDict[k]
			values.append(maxturnfordealerdic.get(keys[1]))
		#print keys
	#print("------------------------------------------\n")

alldealer, responseDict = getCustomerAllTurn()
getMaxTurnfordealer(alldealer, responseDict)
print responseDict