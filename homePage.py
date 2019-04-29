from tkinter import *
import tkfontchooser as tf


class homePage:

    numOrders = 0
    orders = {"bluelight": 0, "popcorn": 0, "coke": 0, "pretzels": 0, "hotdog": 0, "coffee": 0, "sodapop": 0, "pizzaslice": 0}
    orders_cost = {"bluelight": 10, "popcorn": 5, "coke": 5, "pretzels": 3, "hotdog": 10, "coffee": 3, "sodapop": 3, "pizzaslice": 8}
    root = Tk()
    root.geometry("1200x1000")

    def bluelight(self):
        self.orders["bluelight"] += 1
        self.numOrders += 1

    def popcorn(self):
        self.numOrders += 1
        self.orders["popcorn"] += 1

    def coke(self):
        self.numOrders += 1
        self.orders["coke"] += 1

    def pretzels(self):
        self.numOrders += 1
        self.orders["pretzels"] += 1

    def hotdog(self):
        self.numOrders += 1
        self.orders["hotdog"] += 1

    def coffee(self):
        self.numOrders += 1
        self.orders["coffee"] += 1

    def sodapop(self):
        self.numOrders += 1
        self.orders["sodapop"] += 1

    def pizzaslice(self):
        self.numOrders += 1
        self.orders["pizzaslice"] += 1

    def numberoforder(self):
        print("You have ordered", self.numOrders, "items", sep=" ")
        print("Your Orders Contain : ")
        print(" | Item", "|", "Number of Items |", sep=" ")
        print("_______________________________________")
        sum = 0;
        for k, v in self.orders.items():
            print(" |", k, "|", v, "| ", sep=" ")
            if(v > 0):
                sum += self.orders_cost[k] * v
        print(" Total Cost : ", sum)

    def ordersuccess(self):
        print("Order Placed")
        homePage().numberoforder()
        self.root.destroy();

    def orderfailure(self):
        print("Order Cancelled")
        self.orders = {"bluelight": 0, "popcorn": 0, "coke": 0, "pretzels": 0, "hotdog": 0, "coffee": 0, "sodapop": 0, "pizzaslice": 0}
        self.root.destroy()


    def createhomepage(self, customer_name):
        self.root.title("Face Recognition")
        # ************* Fonts ****************
        helv36 = tf.Font(family='Helvetica', size=36)
        helv24 = tf.Font(family='Helvetica', size=24)
        helv22 = tf.Font(family='Helvetica', size=22)
        helv16 = tf.Font(family='Helvetica', size=16)

        frame = Frame(self.root, width=1200, height=100)
        header = Label(frame, text="Delaware North", bg="#88D1F9", font=helv36, width=43, height=2)
        msg = Label(frame, text="Welcome " + customer_name, fg="black", font=helv24)
        #mi = PhotoImage('Saurabh_Sharma.jpg')
        #tmi = mi.subsample(6,6)
        if(customer_name == "Saurabh Sharma"):
            history = Label(frame, text="Last time you were here. You ordered Coke and Popcorn", bg="white", fg="black", font=helv22)
        elif(customer_name == "Disha Shetty"):
            history = Label(frame, text="Last time you were here. You ordered Coke and Pizza Slice", bg="white", fg="black", font=helv22)
        elif (customer_name == "Disha Shetty"):
            history = Label(frame, text="Last time you were here. You ordered Coke and Pizza Slice", bg="white", fg="black", font=helv22)
        else:
            history = Label(frame, text="Last time you were here. You ordered Blue Light and Popcorn", bg="white",fg="black", font=helv22)
        current = Label(frame, text="What would you like to have today?", bg="white", fg="black", font=helv22)

        # ************* Tool Bar ****************
        toolbar = Frame(self.root, bg="#387CA1", width=1000, height=20)
        toolbluelight = Button(toolbar, text="Blue Light - $10", bg="#D1DCDC", width=20, height=5, font=helv16, command=homePage().bluelight)
        toolpopcorn = Button(toolbar, text="Popcorn - $5", width=20, bg="#D1DCDC", height=5, font=helv16, command=homePage().popcorn)
        toolcoke = Button(toolbar, text="Coke - $5", width=20, height=5, bg="#D1DCDC", font=helv16, command=homePage().coke)
        toolpretzels = Button(toolbar, text="Pretzels - $3", width=20, bg="#D1DCDC", height=5, font=helv16, command=homePage().pretzels)
        toolhotdog = Button(toolbar, text="Hot Dog - $10", width=20, bg="#D1DCDC", height=5, font=helv16, command=homePage().hotdog)
        toolcoffee = Button(toolbar, text="Coffee - $3", width=20, bg="#D1DCDC", height=5, font=helv16, command=homePage().coffee)
        toolsodapop = Button(toolbar, text="Soda Pop - $3", width=20, bg="#D1DCDC", height=5, font=helv16, command=homePage().sodapop)
        toolpizzaslice = Button(toolbar, text="Pizza Slice - $8", bg="#D1DCDC", width=20, height=5, font=helv16, command=homePage().pizzaslice)

        toolbarButton = Frame(self.root, bg="#323336", width=1000, height=20)
        yes_button = Button(toolbarButton, bg="#9FA0A3", text="Order", fg="black", width=10, height=3, font=helv16, command=homePage().ordersuccess)
        no_button = Button(toolbarButton, bg="#9FA0A3", text="Cancel", fg="black", width=10, height=3, font=helv16, command=homePage().orderfailure)

        # ************* Building Grid ****************
        frame.grid(sticky=N+S+W+E)
        header.grid(row=0, sticky=W+E)
        msg.grid(row=1, pady=30)
        #msg.config(image=tmi, compound=LEFT)
        history.grid(row=2, pady=30)
        current.grid(row=3, pady=30)

        toolpopcorn.grid(row=4, column=1, padx=50, pady=10)
        toolcoke.grid(row=4, column=2, padx=10, pady=10)
        toolbluelight.grid(row=4, column=3, padx=10, pady=10)
        toolpretzels.grid(row=4, column=4, padx=10, pady=10)
        toolhotdog.grid(row=5, column=1, padx=50, pady=10)
        toolcoffee.grid(row=5, column=2, padx=10, pady=10)
        toolsodapop.grid(row=5, column=3, padx=10, pady=10)
        toolpizzaslice.grid(row=5, column=4, padx=10, pady=10)
        toolbar.grid(row=6, pady=10, rowspan=2, sticky=W+E)

        yes_button.grid(row=7, column=0, columnspan=2, padx=290, pady=10)
        no_button.grid(row=7, column=2, columnspan=2, padx=10, pady=10)
        toolbarButton.grid(row=8, pady=20, rowspan=2, sticky=W+E)

        self.root.mainloop()

#homePage().createhomepage("Saurabh Sharma")