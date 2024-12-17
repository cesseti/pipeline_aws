class Lampada:
    def __init__(self, ligada):
        self.ligada = ligada 
    
    def liga(self):
        self.ligada = True
    
    def desliga(self):
        self.ligada = False
    
    def esta_ligada(self):
         if self.ligada:
            return True
         else:
             return False

interruptor= Lampada(True)
interruptor.liga()
print(f'A lâmpada está ligada?', interruptor.esta_ligada())

interruptor.desliga()
print(f'A lâmpada está ligada?', interruptor.esta_ligada())