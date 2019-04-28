from tkinter import *
import tkfontchooser as tf


class homePage:

    numOrders = 0
    orders = {"kingfisher": 0, "water": 0, "chips": 0}
    root = Tk()
    #root.geometry("500*500")

    def kingfisher(self):
        print("before kingfisher : ", self.numOrders, sep=" ")
        self.orders["kingfisher"] += 1
        self.numOrders += 1
        print("added kingfisher : ", self.numOrders, sep=" ")

    def water(self):
        self.numOrders += 1
        self.orders["water"] += 1

    def chips(self):
        self.numOrders += 1
        self.orders["chips"] += 1

    def numberoforder(self):
        print("You have ordered", self.numOrders, "items", sep=" ")
        print("Your Orders Contain : ")
        print("Item", " -> ", "Number of Items", sep=" ")
        for k, v in self.orders.items():
            print(k, " -> ", v, sep=" ")

    def ordersuccess(self):
        print("Order Placed")
        homePage().numberoforder()
        self.root.destroy();

    def orderfailure(self):
        print("Order Cancelled")
        self.orders = {"kingfisher": 0, "water": 0, "chips": 0}
        self.root.destroy()


    def createhomepage(self, customer_name):
        self.root.title("Face Recognition")
        helv36 = tf.Font(family='Helvetica', size=36)

        frame = Frame(self.root, width=1800, height=1800, bg="grey")
        header = Label(frame, text="Delaware North", bg="blue", fg="white", font=helv36)
        msg = Label(frame, text="Welcome !! " + customer_name, bg="blue", fg="white")
        history = Label(frame, text="Last time you were here. You ordered Kingfisher Beer", bg="white", fg="black")
        yes_button = Button(frame, text="Order", fg="black", command=homePage().ordersuccess)
        no_button = Button(frame, text="Cancel", fg="black", command=homePage().orderfailure)


        # ************* Tool Bar ****************
        toolbar = Frame(frame, bg="green", )
        toolbarkingfisher = Button(toolbar, text="Kingfisher", command=homePage().kingfisher)
        toolbarwater = Button(toolbar, text="Water", command=homePage().water)
        toolbarchips = Button(toolbar, text="Chips", command=homePage().chips)

        frame.grid(row=0)
        header.grid(row=1, columnspan=4, pady=20)
        msg.grid(row=2, columnspan=4, pady=10)
        history.grid(row=3, columnspan=3, pady=10, padx=20)
        toolbarkingfisher.grid(row=4, sticky=E, padx=10, pady=10)
        toolbarwater.grid(row=4, column=1, sticky=E, padx=10, pady=10)
        toolbarchips.grid(row=4, column=2, sticky=E, padx=10, pady=10)
        toolbar.grid(row=5, columnspan=3, rowspan=2, pady=10)
        yes_button.grid(row=7, sticky=E, columnspan=2, pady=10)
        no_button.grid(row=7, column=1, sticky=W, columnspan=2, pady=10)


        self.root.mainloop()

#homePage().createhomepage("Saurabh Sharma")