import tkinter as tk
from tkinter import ttk
import sqlite3
from   datetime import datetime
import Barcode_Generate 

class inventoryWindowClass:

# Main Window 
    def __init__(self, root):
        self.root = root
        # Window size is 550 by 450 pixels
        self.root.geometry("550x450")
        # Window title is Inventory Summary
        self.root.title("Inventory Summary")
        
        ##############################################################################
        # VERTICAL SCROLL BAR - ADJUST WINDOW SIZE WHILE RUNNING TO ACTIVATE SCROLLBAR
        ##############################################################################

        # Create A Main Frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create A CAnvas
        my_canvas= tk.Canvas(main_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add a Scrollbar to the Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # Logout Button - Closes window
        logoutButton=tk.Button(self.root, 
                               text="Logout", 
                               compound=tk.RIGHT, 
                               command = quit,
                               font=("times new roman", 15, "bold"),
                               bg="red",
                               cursor="hand2").place(x=1350, y=8,height=40,width=150)
        
        # Create another frame inside the Canvas
        second_frame = tk.Frame(my_canvas)

        # Add That New frame To A Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        ########################################################
        # Create buttons for data entry
        ########################################################

        # Add spaces in row for centering and aesthetic purposes
        space_row_1 = tk.Label(second_frame, text=' ', font=('Times New Roman', 7))
        space_row_1.grid(row=1, column=4, pady=0)

        # Entry boxes for inputting inventory information
        item_barcode = tk.Entry(second_frame, width=20)
        item_barcode.grid(row=2, column=1, pady=1, sticky=tk.W)

        item_name = tk.Entry(second_frame, width=20)
        item_name.grid(row=3, column=1, pady=1, sticky=tk.W)

        item_price = tk.Entry(second_frame, width=20)
        item_price.grid(row=4, column=1, pady=1, sticky=tk.W)

        item_quantity = tk.Entry(second_frame, width=20)
        item_quantity.grid(row=5, column=1, pady=1, sticky=tk.W)

        item_category = tk.Entry(second_frame, width=20)
        item_category.grid(row=6, column=1, pady=1, sticky=tk.W) 

        item_supplier = tk.Entry(second_frame, width=20)
        item_supplier.grid(row=7, column=1, pady=1, sticky=tk.W)              

        # Labels for entry boxes
        item_barcode_label = tk.Label(second_frame, text='Barcode ID')
        item_barcode_label.grid(row=2, column=0, pady=1, sticky=tk.E)

        item_name_label = tk.Label(second_frame, text='Name ')
        item_name_label.grid(row=3, column=0, pady=1, sticky=tk.E)

        item_price_label = tk.Label(second_frame, text ='Price ($) ')
        item_price_label.grid(row=4,column=0, pady=1, sticky=tk.E)

        item_quantity_label = tk.Label(second_frame,  text='Quantity ')
        item_quantity_label.grid(row=5, column=0, pady=1, sticky=tk.E)

        item_category_label = tk.Label(second_frame,  text='Category ')
        item_category_label.grid(row=6, column=0, pady=1, sticky=tk.E)

        item_supplier_label = tk.Label(second_frame,  text='Supplier ')
        item_supplier_label.grid(row=7, column=0, pady=1, sticky=tk.E)      
          
        item_timestamp_label = tk.Label(second_frame,  text='Timestamp ')
        item_timestamp_label.grid(row=8, column=0, pady=1, sticky=tk.E)

        # Error Label for a duplicate value
        error_label = tk.Label(second_frame,  text='')
        error_label.grid(row=18, column=0, pady=2, sticky=tk.E)

        ########################################################
        # add_new_items - Add items to the database
        ########################################################

        def add_new_items():
            # Open connection to the database
            connection = sqlite3.connect("Mines_slab_data.db")
            # connection.cursor allows editing the database
            cursor = connection.cursor()

            # Select all counts from inventory table where the barcode entry that is typed in matches what is in the inventory
#            try: 
            cursor.execute( """SELECT COUNT(*) AS occurrence_count 
                            FROM inventory 
                            WHERE barcode = ?""",(item_barcode.get(),))
            result = cursor.fetchone()

            # number of occurences the same barcode pops up
            occurrence_count = result[0]

            # If there is already a matching barcode in the inventory table, throw an error that the barcode is already in the database
            if occurrence_count >= 1:
                error_label.config(text="Error: Duplicate value found.",bg="red")

            # Else insert all entry information into the inventory table
            else:
                cursor.execute("""INSERT INTO 
                                inventory(barcode,name,price,quantity,category, supplier, timestamp)
                                VALUES (?,?,?,?,?,?,?)""",
                                (item_barcode.get(), 
                                item_name.get(), 
                                item_price.get(), 
                                item_quantity.get(), 
                                item_category.get(), 
                                item_supplier.get(), 
                                (datetime.now().strftime("%d-%m-%Y %H:%M:%S"))))
                print("Command executed successfully...")
            
                # num = item_barcode.get()
                # num = "0"*(13-len(num))+num if len(num)<12 else num
                barcode_img = Barcode_Generate.generate(item_barcode.get())

            cursor.execute("""SELECT *, oid FROM inventory WHERE barcode = ?""",item_barcode.get())
            records = cursor.fetchall()
            print_records = ''
            for record in records:
                print_records += "Barcode: " + str(record[0]) + ", " + "Name: " + str(record[1]) + ", Price: " + str(record[2]) + ", Quantity: " + str(record[3]) + ", Last Check-In: " + str(record[6]) +"\n"
            show_records_label = tk.Label(second_frame, text=print_records)
            show_records_label.grid(row=12, column=0, columnspan=2)
            # Commit changes and close database link
            connection.commit()
            connection.close()
            
            item_barcode.delete(0, tk.END)
            item_name.delete(0, tk.END)
            item_price.delete(0, tk.END)
            item_quantity.delete(0, tk.END)
            item_category.delete(0, tk.END)
            item_supplier.delete(0, tk.END)


        add_new_items_btn = tk.Button(second_frame, text="Add Record to Database", command=add_new_items)
        add_new_items_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx = 33)
        

        # Create barcode entry box in the window
        item_barcode2 = tk.Entry(second_frame, width=20)
        item_barcode2.grid(row=13, column=1, pady=10, sticky=tk.W) 

        # Create barcode entry label
        item_barcode2_label = tk.Label(second_frame, text='Select Barcode')
        item_barcode2_label.grid(row=13, column=0, pady=10, sticky=tk.E)

        # Call value in the barcode entry box
        def get_barcode():
            if item_barcode2.get() == '':
                raise ValueError('Error: You didnt input a barcode')
            else:
                return item_barcode2.get()


        # Delete inventory items by Barcode
        def delete():
            barcode_var = get_barcode()
            # Input validation
            if not barcode_var:
                print("Barcode cannot be empty.")
                return
            try: 
                connection = sqlite3.connect('Mines_slab_data.db')
                cursor = connection.cursor()
                cursor.execute("""SELECT *, oid FROM inventory WHERE barcode = ?""",barcode_var)
                records = cursor.fetchall()
                
                cursor.execute('DELETE FROM inventory WHERE barcode=?',(barcode_var, ))
                print("Sucessfully deleted " + str(barcode_var) )
                
                item_barcode2.delete(0, tk.END)

                print_records = ''
                for record in records:
                    print_records += "Barcode: " + str(record[0]) + ", " + "Name: " + str(record[1]) + ", Price: " + str(record[2]) + ", Quantity: " + str(record[3]) + ", Last Check-In: " + str(record[6]) +"\n"
                show_records_label = tk.Label(second_frame, text=print_records)
                show_records_label.grid(row=18, column=0, columnspan=2)

                connection.commit()
                connection.close()

            except sqlite3.Error as e:
                print("Error deleting record:", e)

        delete_btn = tk.Button(second_frame, text="Delete by Barcode", command=delete)
        delete_btn.grid(row=15, column=0, columnspan=2, pady=10, padx=10, ipadx=48)
    

if __name__=="__main__":
    root=tk.Tk()
    obj=inventoryWindowClass(root)
    root.mainloop()