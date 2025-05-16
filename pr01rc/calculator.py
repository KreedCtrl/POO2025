import tkinter as tk
import math
#radical din nr negativ
#memoria la calc
#inca un log 
#problema cu punct dupa o cifra
class Calculator:
    def __init__(self):
        self.memory = None

def show_error(self):#afiseaza eroare
    self.entry.delete(0, tk.END)
    self.entry.insert(tk.END, str("Error"))     
    self.master.after(1000, lambda: self.entry.delete(0, tk.END))

def show_result(result, self):#afiseaza rezultatul
    self.entry.delete(0, tk.END)
    self.entry.insert(tk.END, str(result))


class CalculatorGui:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.calculator = Calculator()

        self.entry = tk.Entry(master, width=30)
        self.entry.grid(row =0, column = 0, columnspan = 5)
        self.create_buttons()
    def create_buttons(self): 
        buttons = [
            'MC', 'MR', 'M+', 'M-', 'MS',
            '√x', '%', 'x^2', '1/x', 'sin',
            '7', '8', '9', '/', 'cos',
            '4', '5', '6', '*', 'tg',
            '1', '2', '3', '-', 'ctg',
            'C', '0', '.', '+', 'lg',
            'hex', 'dec',  '=', "⌫",'ln'

        ]
        row_val = 1
        col_val = 0
        for button in buttons:
            action = lambda x = button: self.on_button_click(x)
            tk.Button(self.master, text=button,
                       command=action, width=5, height=2).grid(row=row_val, column = col_val)
            col_val+=1
            if col_val>4:
                col_val = 0
                row_val += 1
    def on_button_click(self, char):
        if (char == "="):
            try: 
                expression = self.entry.get()
                result = eval(expression)#evalueaza expresia
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "C"):
            self.entry.delete(0, tk.END) #sterge toata expresia
        elif (char == "MC"):#sterge memoria
            self.calculator.memory = None
        elif (char == "M+"):#adauga in memorie
            self.calculator.memory = self.entry.get()
        elif (char == "M-"):#scade din memorie
            self.calculator.memory = self.entry.get()
        elif (char == "MR"):#citeste din memorie
            self.entry.insert(tk.END, self.calculator.memory)
        elif (char == "MS"):#salveaza in memorie
            self.calculator.memory = self.entry.get()
        elif (char == "√x"):#radical
            try:
                expression = self.entry.get()
                result = eval(expression + '**(1/2)')#radical, ridicarea la puterea 1/2
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "%"):#transforma in procent (imparte la 100)
            try:
                expression = self.entry.get()
                result = eval(expression + '/100')
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "x^2"): 
            try:
                expression = self.entry.get()
                result = eval(expression + '**2') #ridica la patrat
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "1/x"):
            try:
                expression = self.entry.get()
                result = eval("1/" + expression) #x^-1
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "sin"):
            try: 
                expression = self.entry.get()
                result = math.sin(math.radians(float(expression))) #sin
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "cos"):
            try:
                expression = self.entry.get()
                result = math.cos(math.radians(float(expression))) #cos
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "tg"):
            try:
                expression = self.entry.get()
                result = math.tan(math.radians(float(expression))) #tangenta
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "ctg"):
            try:
                expression = self.entry.get()
                result = 1/math.tan(math.radians(float(expression))) #cotangenta
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "lg"):
            try:
                expression = self.entry.get()
                result = math.log10(float(expression)) #logaritm in baza 10
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "ln"):
            try:
                expression = self.entry.get()
                result = math.log(float(expression)) #logaritm natural
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "hex"):
            try:
                expression = self.entry.get()
                result = hex(int(expression))#transforma in hexazecimal 0x(hex)
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "dec"):
            try:
                expression = self.entry.get()
                result = int(expression, 16) #transfroma din hex in decimal
                show_result(result, self)
            except Exception as e:
                show_error(self)
        elif (char == "."):############ de reparat pentru ex 7.03+17.5
            entry_text = self.entry.get()
            if entry_text == "" or entry_text[-1] in "-+*/":#verifica daca expresia este goala sau daca ultimul caracter este un operator
                self.entry.insert(tk.END, "0.")#daca este goala adauga 0 inainte de .
            elif '.' in self.entry.get().split("+-*/", 1)[-1]:
                pass
            elif self.entry.get()[-1] == ".":#verifica daca ultimul caracter este .
                pass
            else:
                self.entry.insert(tk.END, char)
        elif (char == "⌫"):
            self.entry.delete(len(self.entry.get())-1, tk.END)#sterge ultimul caracter
        else :
            self.entry.insert(tk.END, char)

if __name__ == "__main__":
    root = tk.Tk()
    gui = CalculatorGui(root)
    root.mainloop()
            