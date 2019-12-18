import datetime
class Logger:
    def __init__(self, file, doLogging):
        self.file = file
        self.doLogging = doLogging
    
    def info(self, msg):
        self.__write("INFO",msg)
    def warning(self,msg):
        self.__write("WARNING",msg)
    def error(self,msg):
        self.__write("ERROR",msg)
    def __write(self,tag,msg):
        if(self.doLogging):
            with open(self.file,"a") as wr:
                wr.write(str(datetime.datetime.now()) + "\t" + tag + ":\t\t" + msg + "\n")