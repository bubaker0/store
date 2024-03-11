from tkinter import Tk, Label, Entry, Button, Scrollbar, Frame
from ttkbootstrap import Style
from tkinter import ttk
from tkinter import messagebox
from database import InventoryDB
import tkinter.font as tkFont
import webbrowser


class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("نظام المخزون")
        window_width = 800
        window_height = 550
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        
        self.master.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        self.style = Style(theme="flatly")  
        self.db = InventoryDB('inventory.db')
        
        
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10, ipadx=5, ipady=5)  

        self.labels_frame = Frame(self.frame, bg="lightgray", padx=10, pady=10, relief="raised", borderwidth=2)  
        self.labels_frame.pack(fill="both", padx=(0, 10), pady=10, side="right")

        self.item_name_label = Label(self.labels_frame, text="اسم الصنف:", font=("Arial", 12), bg="lightgray")
        self.item_name_label.grid(row=0, column=0, pady=5, sticky="e")
        self.item_name_entry = Entry(self.labels_frame, font=("Arial", 12),justify="center")
        self.item_name_entry.grid(row=0, column=1, pady=5)

        self.quantity_label = Label(self.labels_frame, text="العدد:", font=("Arial", 12), bg="lightgray")
        self.quantity_label.grid(row=1, column=0, pady=5, sticky="e")
        self.quantity_entry = Entry(self.labels_frame, font=("Arial", 12),justify="center")
        self.quantity_entry.grid(row=1, column=1, pady=5)

        self.purchase_price_label = Label(self.labels_frame, text="سعر الشراء:", font=("Arial", 12), bg="lightgray")
        self.purchase_price_label.grid(row=2, column=0, pady=5, sticky="e")
        self.purchase_price_entry = Entry(self.labels_frame, font=("Arial", 12),justify="center")
        self.purchase_price_entry.grid(row=2, column=1, pady=5)

        self.selling_price_label = Label(self.labels_frame, text="سعر الايجار:", font=("Arial", 12), bg="lightgray")
        self.selling_price_label.grid(row=3, column=0, pady=5, sticky="e")
        self.selling_price_entry = Entry(self.labels_frame, font=("Arial", 12),justify="center")
        self.selling_price_entry.grid(row=3, column=1, pady=5)

        self.selling_price_label1 = Label(self.labels_frame, text=" البحث:", font=("Arial", 12), bg="lightgray")
        self.selling_price_label1.grid(row=4, column=0, pady=5, sticky="e")
        self.selling_price_entry1 = Entry(self.labels_frame, font=("Arial", 12),justify="center")
        self.selling_price_entry1.grid(row=4, column=1, pady=5)

        

        self.buttons_frame = Frame(self.labels_frame, bg="lightgray", padx=25, pady=10, relief="raised", borderwidth=2)
        self.buttons_frame.grid(row=5, columnspan=2, pady=10)

        self.close_button = Button(self.buttons_frame, text="بحث", command=self.search_and_display, font=("Arial", 12), bg="black", fg="white", width=20)
        self.close_button.grid(row=0, column=0, pady=5)

        self.add_button = Button(self.buttons_frame, text="حفظ", command=self.add_item, font=("Arial", 12), bg="black", fg="white", width=20)
        self.add_button.grid(row=1, column=0, pady=5)

        self.edit_button = Button(self.buttons_frame, text="تعديل", command=self.edit_item, font=("Arial", 12), bg="black", fg="white", width=20)
        self.edit_button.grid(row=2, column=0, pady=5)

        self.delete_button = Button(self.buttons_frame, text="حذف", command=self.delete_item, font=("Arial", 12), bg="black", fg="white", width=20)
        self.delete_button.grid(row=3, column=0, pady=5)

        self.close_button1 = Button(self.buttons_frame, text="تحديث", command=self.clear_entry_fields, font=("Arial", 12), bg="black", fg="white", width=20)
        self.close_button1.grid(row=4, column=0, pady=5)

        self.close_button = Button(self.buttons_frame, text="المطور", command=self.Tiktok, font=("Arial", 12), bg="black", fg="white", width=20)
        self.close_button.grid(row=5, column=0, pady=5)

        self.close_button = Button(self.buttons_frame, text="خروج", command=self.master.destroy, font=("Arial", 12), bg="black", fg="white", width=20)
        self.close_button.grid(row=6, column=0, pady=5)

        

        self.data_frame = Frame(self.frame, bg="lightgray", padx=10, pady=10, relief="raised", borderwidth=2)  
        self.data_frame.pack(fill="both", expand=True, padx=(0, 10), pady=10)

        self.tree = ttk.Treeview(self.data_frame, columns=("ID", "الصنف", "العدد", "سعر الشراء", "سعر الايجار"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("الصنف", text="الصنف", anchor="center")
        self.tree.heading("العدد", text="العدد", anchor="center")
        self.tree.heading("سعر الشراء", text="سعر الشراء", anchor="center")
        self.tree.heading("سعر الايجار", text="سعر الايجار", anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.data_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=self.scrollbar.set)
        
        self.load_data()
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        
    def load_data(self):
        # Fetch data from the database
        data = self.db.cursor.execute("SELECT * FROM inventory").fetchall()

        # Clear existing data from Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert data into the treeview
        for record in data:
            self.tree.insert("", "end", values=record)

        # Stretch columns to fit content and center-align cell data
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
            # Resize the column width to fit the header text
            self.tree.column(col, width=tkFont.Font().measure(col), anchor="center")
            # Iterate through each cell in the column
            for item in data:
                # Resize the column width if necessary to fit the contents
                width = tkFont.Font().measure(str(item[self.tree["columns"].index(col)]))
                if self.tree.column(col, width=None) < width:
                    self.tree.column(col, width=width)

    def clear_entry_fields(self):
        if self.item_name_entry.get():
            self.item_name_entry.delete(0, 'end')
        if self.quantity_entry.get():
            self.quantity_entry.delete(0, 'end')
        if self.purchase_price_entry.get():
            self.purchase_price_entry.delete(0, 'end')
        if self.selling_price_entry.get():
            self.selling_price_entry.delete(0, 'end')
        if self.selling_price_entry1.get():
            self.selling_price_entry1.delete(0, 'end')
        
    def Tiktok(self):
       # العنوان URL المطلوب
        url = "https://www.tiktok.com/@x_23ly"

        # فتح العنوان URL في المتصفح الافتراضي
        webbrowser.open(url)


    def add_item(self):
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        purchase_price = self.purchase_price_entry.get()
        selling_price = self.selling_price_entry.get()

        # Check if any field is empty
        if not (item_name and quantity and purchase_price and selling_price):
            messagebox.showwarning("تحذير", "الرجاء ملء جميع الحقول")
            return

        try:
            # Attempt to convert quantity, purchase_price, and selling_price to int/float
            quantity = int(quantity)
            purchase_price = float(purchase_price)
            selling_price = float(selling_price)
        except ValueError:
            # Show a warning if conversion fails (i.e., if the user entered non-numeric values)
            messagebox.showwarning("تحذير", "يرجى إدخال قيم صحيحة للعدد وسعر الشراء وسعر البيع")
            return

        # If all checks pass, add the item to the database
        self.db.add_item(item_name, quantity, purchase_price, selling_price)
        self.clear_entry_fields()  # Clear entry fields after adding the item

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch data from the database
        data = self.db.cursor.execute("SELECT * FROM inventory").fetchall()

        # Insert data into the treeview at the end
        for record in data:
            self.tree.insert("", "end", values=record)

    def edit_item(self):
        selected_item = self.tree.selection()
        if len(selected_item) != 1:
            messagebox.showwarning("تحذير", "يرجى تحديد صف واحد للتعديل")
            return

        item_id = self.tree.item(selected_item)["values"][0]
        item_name = self.item_name_entry.get()
        quantity = int(self.quantity_entry.get())
        purchase_price = float(self.purchase_price_entry.get())
        selling_price = float(self.selling_price_entry.get())
        self.db.cursor.execute("UPDATE inventory SET item_name=?, quantity=?, purchase_price=?, selling_price=? WHERE id=?",
                            (item_name, quantity, purchase_price, selling_price, item_id))
        self.db.conn.commit()
        self.clear_entries()  # Clear entry fields after editing an item

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch data from the database
        data = self.db.cursor.execute("SELECT * FROM inventory").fetchall()

        # Insert data into the treeview
        for record in data:
            self.tree.insert("", "end", values=record)
    
    
    def delete_item(self):
        selected_item = self.tree.selection()
        if len(selected_item) != 1:
            messagebox.showwarning("تحذير", "يرجى تحديد صف واحد للحذف")
            return

        confirm = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا الصنف؟")
        if confirm:
            item_id = self.tree.item(selected_item)["values"][0]
            self.db.cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
            self.db.conn.commit()

            # Remove the item directly from Treeview without reloading data
            self.tree.delete(selected_item)

            # Reorder the IDs after deletion
            self.reorder_ids()

            self.clear_entry_fields()  # Clear entry fields after deleting an item


    def reorder_ids(self):
        # Fetch all remaining items
        remaining_items = self.db.cursor.execute("SELECT id FROM inventory").fetchall()
    
        # Reorder the IDs
        for index, item in enumerate(remaining_items, start=1):
            self.db.cursor.execute("UPDATE inventory SET id=? WHERE id=?", (index, item[0]))
    
        self.db.conn.commit()
    
    
    
    
    
    def search_and_display(self):
        # Get the value entered in the search entry
        search_value = self.selling_price_entry1.get()
    
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
    
        # Fetch data from the database based on the search value
        data = self.db.cursor.execute("SELECT * FROM inventory WHERE item_name LIKE ?", ('%' + search_value + '%',)).fetchall()
    
        # Insert data into the treeview
        for record in data:
            self.tree.insert("", "end", values=record)
    
        # Stretch columns to fit content and center-align cell data (same as in load_data function)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
            for item in data:
                width = tkFont.Font().measure(str(item[self.tree["columns"].index(col)]))
                if self.tree.column(col, width=None) < width:
                    self.tree.column(col, width=width)
    


    def clear_entries(self):
        self.item_name_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.purchase_price_entry.delete(0, 'end')
        self.selling_price_entry.delete(0, 'end')
    
    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            self.item_name_entry.delete(0, "end")
            self.item_name_entry.insert(0, item[1])
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, item[2])
            self.purchase_price_entry.delete(0, "end")
            self.purchase_price_entry.insert(0, item[3])
            self.selling_price_entry.delete(0, "end")
            self.selling_price_entry.insert(0, item[4])
    
    # def search_and_display(self):
    #     # Get the value entered in the search entry
    #     search_value = self.selling_price_entry1.get()

    #     # Clear existing data
    #     for row in self.tree.get_children():
    #         self.tree.delete(row)

    #     # Fetch data from the database based on the search value
    #     data = self.db.cursor.execute("SELECT * FROM inventory WHERE item_name LIKE ?", ('%' + search_value + '%',)).fetchall()

    #     # Insert data into the treeview
    #     for record in data:
    #         self.tree.insert("", "end", values=record)

    #     # Stretch columns to fit content and center-align cell data (same as in load_data function)
    #     for col in self.tree["columns"]:
    #         self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
    #         for item in data:
    #             width = tkFont.Font().measure(str(item[self.tree["columns"].index(col)]))
    #             if self.tree.column(col, width=None) < width:
    #                 self.tree.column(col, width=width)


if __name__ == "__main__":
    root = Tk()
    app = InventoryApp(root)
    root.mainloop()