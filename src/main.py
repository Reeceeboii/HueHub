from hueConnect import connect as HC

# attempts to resolve a Hue Bridge on the local logical subnet
hueData = HC.check_connection()
