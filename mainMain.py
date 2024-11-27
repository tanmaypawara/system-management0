import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BillingSystem:

    def createDatabase(self):
        """ Create SQLite database for storing orders """
        self.conn = sqlite3.connect('billing_system.db')
        self.cursor = self.conn.cursor()

        # Create table for storing orders if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                bill_number TEXT,
                item TEXT,
                quantity INTEGER,
                price REAL,
                date TEXT,
                time TEXT,
                payment_type TEXT
            )
        ''')
        self.conn.commit()

    def createWidget(self):
        tk.Label(self.root, text="Billing System", font="Arial 15 bold").pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        date = tk.Label(frame, text=f"Date: ", font="Arial 12")
        date.grid(row=0, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.date).grid(row=0, column=1, sticky="w", padx=5)

        time = tk.Label(frame, text=f"Time: ", font="Arial 12")
        time.grid(row=1, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.time).grid(row=1, column=1, sticky="w", padx=5)

        bill = tk.Label(frame, text="Bill No:", font="Arial 12")
        bill.grid(row=2, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.billNumber).grid(row=2, column=1, sticky='w', padx=5)

        menu = tk.Label(frame, text="Menu:", font="Arial 12")
        menu.grid(row=3, column=0, sticky="w")
        combobox = ttk.Combobox(frame, textvariable=self.selectedItem, values=list(self.menu.keys()), state="readonly")
        combobox.grid(row=3, column=1, sticky="w", padx=5)
        combobox.bind("<<ComboboxSelected>>", self.updatePrice)  # Automatically update price when item is selected

        quantity = tk.Label(frame, text="Quantity:", font="Arial 12")
        quantity.grid(row=4, column=0, sticky='w')
        quantity_entry = tk.Entry(frame, textvariable=self.quantity)
        quantity_entry.grid(row=4, column=1, sticky='w', padx=5)
        quantity_entry.bind("<KeyRelease>", self.updatePrice)  # Automatically update price when quantity changes

        price = tk.Label(frame, text="Price:", font="Arial 12")
        price.grid(row=5, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.price, state='readonly').grid(row=5, column=1, sticky='w', padx=5)

        buttonFrame = tk.Frame(self.root)
        buttonFrame.pack(pady=8)

        update = tk.Button(buttonFrame, text="Update Item", bg="#1874CD", borderwidth=0, fg="white", command=self.updatePrice).pack(side="left", padx=5)
        add = tk.Button(buttonFrame, text="Add Item", bg="light green", borderwidth=0, fg="white", command=self.addOrder).pack(side="left", padx=5)
        delete = tk.Button(buttonFrame, text="Delete Item", bg="#FF4040", borderwidth=0, fg="white", command=self.deleteOrder).pack(side="left", padx=5)

        

    def updatePrice(self, event=None):
        item = self.selectedItem.get()
        quantity = self.quantity.get()

        if item in self.menu and quantity > 0:
            price = self.menu[item] * quantity
            self.price.set(price)

    def addOrder(self):
        item = self.selectedItem.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if item and quantity > 0 and price > 0:
            self.orderItem.append((item, quantity, price))
            self.orderList.insert("", "end", values=(item, quantity, price))
            self.calculateTotal()

    def deleteOrder(self):
        selected = self.orderList.selection()
        if selected:
            for sel in selected:
                self.orderList.delete(sel)
                values = self.orderList.item(sel)["values"]
                self.orderItem.remove(tuple(values))
            self.calculateTotal()

    def calculateTotal(self):
        total = sum(item[2] for item in self.orderItem)
        self.totalBill.set(total)

    def viewSalesGraph(self):
        """ Generate a bar chart to show sales data (quantity sold) from the database """
        # Create a new Toplevel window for the graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Sales Graph")
        graph_window.geometry("800x600")

        # Query sales data from the database: total quantity of each item sold
        self.cursor.execute('''
            SELECT item, SUM(quantity) FROM orders
            GROUP BY item
        ''')
        sales_data = self.cursor.fetchall()

        items = [row[0] for row in sales_data]
        total_quantity = [row[1] for row in sales_data]

        # Plotting the sales data (quantity of items sold)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(items, total_quantity, color='green')

        ax.set_xlabel("Items")
        ax.set_ylabel("Quantity Sold")
        ax.set_title("Quantity of Items Sold Overview")

        # Display the graph in the new Toplevel window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack(pady=20)
        canvas.draw()

if __name__ == "__main__":
    window = tk.Tk()
    BillingSystem(window)
    window.mainloop()


