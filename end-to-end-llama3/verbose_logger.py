class VerboseLogger:
    def __init__(self, enabled = False, prefix = ''):
    	self.enabled = enabled
    	self.prefix = prefix




    def print(self, message):
        if self.enabled == True:
        	print(self.prefix+' '+message)