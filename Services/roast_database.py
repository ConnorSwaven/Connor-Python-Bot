from replit import db

def update_roasts(roast_message):
	if "roasts" in db.keys():
		roasts = db["roasts"]
		roasts.append(roast_message)
		db["roasts"] = roasts
	else:
		db["roasts"] = [roast_message]


def delete_roast(index):
	roasts = db["roasts"]
	if len(roasts) > index:
		del roasts[index]
		db["roasts"] = roasts