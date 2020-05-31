# Russell Rivera
# XOR utilities

def xor_strings(a, b, encoding):
	""" a XOR b with format "encoding", e.g., "utf-8" """
	return a.encode(encoding) ^ b.encode(encoding)

if __name__ == "__main__":
	
	""" TODO: make easy to run """
