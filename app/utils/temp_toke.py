from threading import Timer,Thread,Event


# clase que ejecuta una funcion cada cierto tiempo
class perpetualTimer():

    def __init__(self,t):
        self.t=t
        
        self.thread = Timer(self.t,self.handle_function)

    # anexar funcion qeu sera ejecutada
    def setFunction(self, hFunction):        
        self.hFunction = hFunction        
        
    # ciclo infinito de hilo de ejecucio
    def handle_function(self):        
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    # inicio de ciclo
    def start(self):
        #self.thread.cancel()       
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
