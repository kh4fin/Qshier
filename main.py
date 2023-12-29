from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
from tkinter.simpledialog import askfloat
from datetime import datetime
import pandas as pd
from openpyxl import Workbook

# inisialisasi database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="qshier"
)
cursor = mydb.cursor()
tree = None  

def get_data_product():
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return data
#  display product
def display_product():
    global tree  

    data = get_data_product()

    selected_item = None  

    def on_select(event):
        nonlocal selected_item
        selected_item = tree.selection()

    def delete_selected_item():
        nonlocal selected_item
        if selected_item:
            selected_item_values = tree.item(selected_item, 'values')
            delete_product(selected_item_values[1])
            tree.delete(selected_item)

    def back():
        button_frame.pack_forget()
        tree.pack_forget()

        btn_transaksi.pack(pady=(10, 10))
        btn_product.pack(pady=(10, 10))
        btn_report.pack(pady=(10, 10))
        bottom_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
        btn_bottom.pack(side=tk.RIGHT, pady=15, padx=15)

    def edit_item():
        nonlocal selected_item
        if selected_item:
            selected_item_values = tree.item(selected_item, 'values')
            update_product(selected_item_values[1])

    def delete_item():
        nonlocal selected_item
        if selected_item:
            selected_item_values = tree.item(selected_item, 'values')
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_item_values[1]}?")
            if confirmation:
                delete_product(selected_item_values[1])
                tree.delete(selected_item)

    root.title("Product List")

    button_frame = Frame(root)
    button_frame.pack(side=tk.TOP, pady=(10, 5))

    btn_back = Button(button_frame, text="Back", padx=30, pady=10, command=back)
    btn_back.pack(side=tk.LEFT, padx=5)

    btn_add = Button(button_frame, text="Add Product", padx=20, pady=10, command=add_product)
    btn_add.pack(side=tk.LEFT, padx=5)

    btn_edit = Button(button_frame, text="Edit Product", padx=20, pady=10, command=edit_item)
    btn_edit.pack(side=tk.LEFT, padx=5)

    btn_delete = Button(button_frame, text="Delete Product", padx=20, pady=10, command=delete_item)
    btn_delete.pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(root)
    tree["columns"] = ("name", "code_product", "price", "qty")

    tree.heading("#0", text="") 
    tree.heading("name", text="Product Name")
    tree.heading("code_product", text="Code Product")
    tree.heading("price", text="Price")
    tree.heading("qty", text="Quantity")

    tree.column("#0", width=0, stretch=tk.NO)  
    tree.column("name", anchor=tk.CENTER, width=100)
    tree.column("code_product", anchor=tk.CENTER, width=100)
    tree.column("price", anchor=tk.CENTER, width=100)
    tree.column("qty", anchor=tk.CENTER, width=100)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))
    style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

    for row in data:
        tree.insert("", "end", values=row[1:]) 

    tree.bind("<ButtonRelease-1>", on_select)

    tree.pack(padx=10, pady=10, fill='both', expand=True)

keranjang_produk = {}

def display_transaksi():
    global tree, keranjang_produk, entry_kode_produk, kuantitas_combobox, entry_search_product

    def back():
        frame_tombol.pack_forget()
        tree.pack_forget()

        btn_transaksi.pack(pady=(10, 10))
        btn_product.pack(pady=(10, 10))
        btn_report.pack(pady=(10, 10))
        bottom_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
        btn_bottom.pack(side=tk.RIGHT, pady=15, padx=15)

    root.title("Transaksi")
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - 800 / 2)
    center_y = int(screen_height / 2 - 500 / 2)

    window_width = 1200
    window_height = 700

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    frame_tombol = Frame(root)
    frame_tombol.pack(side=tk.TOP, pady=(10, 5))

    back = Button(frame_tombol, text="Back", padx=15, pady=5, command=back)
    back.pack(side=tk.LEFT, padx=(5,15))

    label_kode_produk = Label(frame_tombol, text="Kode Produk:")
    label_kode_produk.pack(side=tk.LEFT, padx=(0, 5))

    entry_kode_produk = Entry(frame_tombol, width=20, font=("Helvetica", 16), bd=3, justify="center", insertwidth=4)
    entry_kode_produk.pack(side=tk.LEFT, padx=(0, 5))

    label_kuantitas = Label(frame_tombol, text="Kuantitas:")
    label_kuantitas.pack(side=tk.LEFT, padx=(0, 5))

    kuantitas_combobox = ttk.Combobox(frame_tombol, values=[i for i in range(1, 11)], state="readonly")
    kuantitas_combobox.set("1")
    kuantitas_combobox.pack(side=tk.LEFT, padx=(0, 5))

    btn_tambah_keranjang = Button(frame_tombol, text="Tambah ke Keranjang", padx=10, pady=5, command=lambda: tambah_ke_keranjang())
    btn_tambah_keranjang.pack(side=tk.LEFT)

    btn_checkout = Button(frame_tombol, text="Checkout", padx=10, pady=5, command=checkout)
    btn_checkout.pack(side=tk.LEFT, padx=10)  

    btn_clear = Button(frame_tombol, text="Clear", padx=10, pady=5, command=clear_keranjang)
    btn_clear.pack(side=tk.LEFT, padx=10)  



    tree = ttk.Treeview(root)
    tree["columns"] = ("id_produk", "nama_produk", "kuantitas", "harga_per_unit", "subtotal")

    tree.heading("#0", text="")
    tree.heading("id_produk", text="ID Produk")
    tree.heading("nama_produk", text="Nama Produk")
    tree.heading("kuantitas", text="Kuantitas")
    tree.heading("harga_per_unit", text="Harga per Unit")
    tree.heading("subtotal", text="Subtotal")

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("id_produk", anchor=tk.CENTER, width=100)
    tree.column("nama_produk", anchor=tk.CENTER, width=200)
    tree.column("kuantitas", anchor=tk.CENTER, width=100)
    tree.column("harga_per_unit", anchor=tk.CENTER, width=150)
    tree.column("subtotal", anchor=tk.CENTER, width=150)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))
    style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

    tree.pack(padx=10, pady=10, fill='both', expand=True)

def tambah_ke_keranjang():
    global keranjang_produk, tree, entry_kode_produk, kuantitas_combobox

    produk_terpilih = entry_kode_produk.get()
    kuantitas_terpilih = int(kuantitas_combobox.get())

    query = "SELECT * FROM products WHERE name_product = %s"
    val = (produk_terpilih,)
    cursor.execute(query, val)
    produk_data = cursor.fetchone()

    if produk_data:
        id_produk = produk_data[0]
        nama_produk = produk_data[1]
        harga_per_unit = produk_data[3]

        if id_produk in keranjang_produk:
            
            if kuantitas_terpilih > produk_data[4]:
                messagebox.showerror("Kesalahan", f"Stok produk '{nama_produk}' hanya tersedia sebanyak {produk_data[4]}.")
                return

            keranjang_produk[id_produk]["kuantitas"] += kuantitas_terpilih
            keranjang_produk[id_produk]["subtotal"] += harga_per_unit * kuantitas_terpilih
            update_treeview()
        else:
            
            if kuantitas_terpilih > produk_data[4]:
                messagebox.showerror("Kesalahan", f"Stok produk '{nama_produk}' hanya tersedia sebanyak {produk_data[4]}.")
                return

            keranjang_produk[id_produk] = {
                "nama_produk": nama_produk,
                "kuantitas": kuantitas_terpilih,
                "harga_per_unit": harga_per_unit,
                "subtotal": harga_per_unit * kuantitas_terpilih
            }
            update_treeview()

def update_treeview():
    global tree, keranjang_produk

    for item in tree.get_children():
        tree.delete(item)

    for id_produk, data_produk in keranjang_produk.items():
        tree.insert("", "end", values=(id_produk, data_produk["nama_produk"], data_produk["kuantitas"], data_produk["harga_per_unit"], data_produk["subtotal"]))



def update_stok_produk(id_produk, kuantitas_terpilih):
    query_stok = "SELECT qty FROM products WHERE id_product = %s"
    cursor.execute(query_stok, (id_produk,))
    stok_sekarang = cursor.fetchone()[0]

    stok_baru = stok_sekarang - kuantitas_terpilih

    query_update_stok = "UPDATE products SET qty = %s WHERE id_product = %s"
    cursor.execute(query_update_stok, (stok_baru, id_produk))
    mydb.commit()


def checkout():
    global keranjang_produk

    if keranjang_produk:
        # Iterasi melalui produk di keranjang
        for product_id, data_produk in keranjang_produk.items():
            kuantitas_terpilih = data_produk["kuantitas"]

            # Ambil informasi produk dari tabel products
            query_produk = "SELECT code_product, name_product FROM products WHERE id_product = %s"
            cursor.execute(query_produk, (product_id,))
            product_info = cursor.fetchone()

            # Update stok produk
            update_stok_produk(product_id, kuantitas_terpilih)

            # Insert data ke dalam tabel penjualan
            query = "INSERT INTO sales_report (id_product, code_product, name_product, quantity, total_price) VALUES (%s, %s, %s, %s, %s)"
            val = (product_id, product_info[0], product_info[1], kuantitas_terpilih, data_produk["subtotal"])
            cursor.execute(query, val)

        # Commit perubahan ke database
        mydb.commit()


    total = sum(data_produk["subtotal"] for data_produk in keranjang_produk.values())
    messagebox.showinfo("Checkout", f"Total Belanja: Rp {total}")


    pembayaran = askfloat("Pembayaran", f"Total Belanja: Rp {total}\nMasukkan Jumlah Pembayaran:")

    if pembayaran is not None:
        kembalian = pembayaran - total

        if kembalian >= 0:
            messagebox.showinfo("Pembayaran Berhasil", f"Terima kasih! Uang kembalian Anda: Rp {kembalian:.2f}")
        else:
            messagebox.showwarning("Pembayaran Kurang", f"Jumlah pembayaran tidak mencukupi. Mohon masukkan jumlah pembayaran yang cukup.")



    keranjang_produk = {}
    update_treeview()

def clear_keranjang():
    global keranjang_produk, tree
    keranjang_produk = {} 
    update_treeview()  
def search_product():
    global tree, entry_search_product

    search_term = entry_search_product.get().lower()

    for item in tree.get_children():
        tree.delete(item)

    data = get_data_product()

    for row in data:
        if search_term in row[1].lower():
            tree.insert("", "end", values=row[1:])



def display_laporan():

    sekarang = datetime.now()
    tahun_sekarang = sekarang.year
    query = "SELECT * FROM sales_report WHERE YEAR(transaction_date) = %s"
    cursor.execute(query, (tahun_sekarang,))
    data_laporan = cursor.fetchall()

    def back():
        laporan_window.forget()
        # tree.pack_forget()

        btn_transaksi.pack(pady=(10, 10))
        btn_product.pack(pady=(10, 10))
        btn_report.pack(pady=(10, 10))
        bottom_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
        btn_bottom.pack(side=tk.RIGHT, pady=15, padx=15)

    root.title("Product List")
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - 800 / 2)
    center_y = int(screen_height / 2 - 500 / 2)

    window_width = 1000
    window_height = 650

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    laporan_window = Frame(root)
    laporan_window.pack(side=tk.TOP, pady=(10, 5))

    
    bulan_var = tk.StringVar()
    bulan_combobox = ttk.Combobox(laporan_window, values=[str(i) for i in range(1, 13)], state="readonly", textvariable=bulan_var)
    bulan_combobox.set("Pilih Bulan")
    bulan_combobox.pack(pady=(5,5))

    

    PilihTahun = Label(laporan_window, text="Pilih Tahun", font=("Helvetica", 16))
    PilihTahun.pack(pady=5)
    entry_tahun = Entry(laporan_window, width=20, font=("Helvetica", 16), bd=3, justify="center", insertwidth=4)
    entry_tahun.pack(pady=(1,10))

    
    def save_to_excel(data, filename="laporan_penjualan.xlsx"):
        df = pd.DataFrame(data, columns=["ID", "id_product", "code_product", "name_product", "quantity", "total_price", "transaction_date"])

        writer = pd.ExcelWriter(filename, engine='openpyxl')

        df.to_excel(writer, index=False)

        writer._save()
        writer.close()



   
    tree_laporan = ttk.Treeview(laporan_window)
    tree_laporan["columns"] = ("code_product", "name_product", "quantity", "total_price", "transaction_date")

    tree_laporan.heading("#0", text="")
    tree_laporan.heading("code_product", text="Product Code")
    tree_laporan.heading("name_product", text="Product Name")
    tree_laporan.heading("quantity", text="Quantity")
    tree_laporan.heading("total_price", text="Total Price")
    tree_laporan.heading("transaction_date", text="Transaction Date")

    tree_laporan.column("#0", width=0, stretch=tk.NO)
    tree_laporan.column("code_product", anchor=tk.CENTER, width=100)
    tree_laporan.column("name_product", anchor=tk.CENTER, width=150)
    tree_laporan.column("quantity", anchor=tk.CENTER, width=80)
    tree_laporan.column("total_price", anchor=tk.CENTER, width=100)
    tree_laporan.column("transaction_date", anchor=tk.CENTER, width=150)



    for row in data_laporan:
        tree_laporan.insert("", "end", values=(row[5],row[6], row[2], row[3], row[4]))

    tree_laporan.pack(padx=10, pady=10, fill='both', expand=True)


    def filter_laporan():
        selected_bulan = bulan_var.get()
        selected_tahun = entry_tahun.get()

        if selected_bulan == "Pilih Bulan" or selected_tahun == "Pilih Tahun":
            messagebox.showinfo("Info", "Pilih bulan dan tahun terlebih dahulu.")
            return

        query = "SELECT * FROM sales_report WHERE MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s"
        cursor.execute(query, (selected_bulan, selected_tahun))
        data_laporan = cursor.fetchall()

        
        for item in tree_laporan.get_children():
            tree_laporan.delete(item)

     
        for row in data_laporan:
            tree_laporan.insert("", "end", values=(row[5],row[6], row[2], row[3], row[4]))
       
    def export_to_excel(data):
        save_to_excel(data)
        messagebox.showinfo("Export Berhasil", "Data berhasil diekspor ke file Excel (laporan_penjualan.xlsx).")

    back = tk.Button(laporan_window, text="Back", padx=20, pady=8, command=back)
    back.pack(side=tk.LEFT, pady=(10,20), padx=10)

    btn_tampilkan = tk.Button(laporan_window, text="Tampilkan Laporan", command=filter_laporan, padx=20, pady=8)
    btn_tampilkan.pack(side=tk.LEFT, pady=(10,20), padx=10)

    export = tk.Button(laporan_window, text="Export", command=lambda: export_to_excel(data_laporan), padx=20, pady=8)
    export.pack(side=tk.LEFT, pady=(10,20))


    


def add_product():
    global cursor, tree

    root.withdraw()

    add_product_window = Toplevel()
    add_product_window.iconbitmap("myLogo.ICO")
    add_product_window.title("Qshier | Add Product")
    add_product_window.resizable(False, False)

    screen_width = add_product_window.winfo_screenwidth()
    screen_height = add_product_window.winfo_screenheight()

    center_x = int(screen_width / 2 - 800 / 2)
    center_y = int(screen_height / 2 - 500 / 2)

    window_width = 800
    window_height = 500

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_product_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    def product_add():
        global cursor, tree
        name = entry_name.get()
        code_product = entry_code_product.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        query = "INSERT INTO products (name_product, code_product, price, qty) VALUES (%s, %s, %s, %s)"
        val = (name, code_product, price, quantity)
        cursor.execute(query, val)
        mydb.commit()

        print(cursor.rowcount, "record inserted.")

        
        tree.insert("", "end", values=(name, code_product, price, quantity))

        root.deiconify()
        add_product_window.destroy()

    label_name = Label(add_product_window, text="Product Name:")
    label_name.pack(pady=(20, 5))
    entry_name = Entry(add_product_window)
    entry_name.pack(pady=5)

    label_code_product = Label(add_product_window, text="Code Product:")
    label_code_product.pack(pady=5)
    entry_code_product = Entry(add_product_window)
    entry_code_product.pack(pady=5)

    label_price = Label(add_product_window, text="Price:")
    label_price.pack(pady=5)
    entry_price = Entry(add_product_window)
    entry_price.pack(pady=5)

    label_quantity = Label(add_product_window, text="Quantity:")
    label_quantity.pack(pady=5)
    entry_quantity = Entry(add_product_window)
    entry_quantity.pack(pady=5)

    btn_add_product = Button(add_product_window, text="Add Product", padx=20, pady=10, command=product_add)
    btn_add_product.pack(pady=20)

    def close():
        root.deiconify()
        add_product_window.destroy()

    add_product_window.protocol('WM_DELETE_WINDOW', close)

def update_product(code_product):
    global tree

    root.withdraw()

    update_product_window = Toplevel()
    update_product_window.iconbitmap("myLogo.ICO")
    update_product_window.title("Qshier | Edit Product")
    update_product_window.resizable(False, False)

    screen_width = update_product_window.winfo_screenwidth()
    screen_height = update_product_window.winfo_screenheight()

    center_x = int(screen_width / 2 - 800 / 2)
    center_y = int(screen_height / 2 - 500 / 2)

    window_width = 800
    window_height = 500

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    update_product_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    query = "SELECT * FROM products WHERE code_product = %s"
    val = (code_product,)
    cursor.execute(query, val)
    product_data = cursor.fetchone()

    def product_update():
        global tree

        name = entry_name.get()
        new_code_product = entry_code_product.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        query = "UPDATE products SET name_product = %s, code_product = %s, price = %s, qty = %s WHERE code_product = %s"
        val = (name, new_code_product, price, quantity, code_product)
        cursor.execute(query, val)

        mydb.commit()

        print(cursor.rowcount, "record updated.")
        
        tree.insert("", "end", values=(name, code_product, price, quantity))

        root.deiconify()
        update_product_window.destroy()

    label_name = Label(update_product_window, text="Product Name:")
    label_name.pack(pady=(20, 5))
    entry_name = Entry(update_product_window)
    entry_name.insert(0, product_data[1])
    entry_name.pack(pady=5)

    label_code_product = Label(update_product_window, text="Code Product:")
    label_code_product.pack(pady=5)
    entry_code_product = Entry(update_product_window)
    entry_code_product.insert(0, product_data[2])
    entry_code_product.pack(pady=5)

    label_price = Label(update_product_window, text="Price:")
    label_price.pack(pady=5)
    entry_price = Entry(update_product_window)
    entry_price.insert(0, product_data[3])
    entry_price.pack(pady=5)

    label_quantity = Label(update_product_window, text="Quantity:")
    label_quantity.pack(pady=5)
    entry_quantity = Entry(update_product_window)
    entry_quantity.insert(0, product_data[4])
    entry_quantity.pack(pady=5)

    btn_update_product = Button(update_product_window, text="Update Product", padx=20, pady=10, command=product_update)
    btn_update_product.pack(pady=20)

    def close():
        root.deiconify()
        update_product_window.destroy()

    update_product_window.protocol('WM_DELETE_WINDOW', close)

def delete_product(code_product):
    query = "DELETE FROM products WHERE code_product = %s"
    val = (code_product,)
    cursor.execute(query, val)
    mydb.commit()
    print("Delete product:", code_product)

def btnProduct():
    btn_transaksi.forget()
    btn_product.forget()
    btn_report.forget()
    bottom_frame.forget()
    display_product()
def btnTransaksi():
    btn_transaksi.forget()
    btn_product.forget()
    btn_report.forget()
    bottom_frame.forget()
    display_transaksi()
def btnReport():
    btn_transaksi.forget()
    btn_product.forget()
    btn_report.forget()
    bottom_frame.forget()
    display_laporan()

root = Tk()
root.iconbitmap("myLogo.ICO")
root.title("Qshier")
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - 800 / 2)
center_y = int(screen_height / 2 - 500 / 2)

window_width = 800
window_height = 500

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

wrapper = tk.Frame(root)
wrapper.pack(fill=tk.BOTH, expand=True)

header = tk.Frame(wrapper)
header.pack(side=tk.TOP, fill=tk.X)

logo_path = "logo.PNG"
logo = Image.open(logo_path)
logo_tk = ImageTk.PhotoImage(logo)

logo_label = Label(header, image=logo_tk)
logo_label.pack()

btn_transaksi = Button(header, text="Transaction", padx=45, pady=20, command=btnTransaksi)
btn_transaksi.forget()
btn_product = Button(header, text="Product", padx=55, pady=20, command=btnProduct)
btn_product.forget()
btn_report = Button(header, text="Report", padx=58, pady=20, command=btnReport)
btn_report.forget()

bottom_frame = tk.Frame(wrapper)
bottom_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

def logout():
    form.pack(fill=tk.BOTH, expand=True)
    btn_report.forget()
    btn_product.forget()
    btn_transaksi.forget()
    btn_bottom.forget()
    

btn_bottom = Button(bottom_frame, text="Logout", padx=30, pady=15, command=logout)
btn_bottom.forget()


form = tk.Frame(header)
form.pack(fill=tk.BOTH, expand=True)

def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    data = cursor.fetchone()

    if data:
        form.forget()
        btn_transaksi.pack(pady=(10, 10))
        btn_product.pack(pady=(10, 10))
        btn_report.pack(pady=(10, 10))
        btn_bottom.pack(side=tk.RIGHT, pady=15, padx=15)
        entry_username.delete(0, END)
        entry_password.delete(0, END)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
def add_user():
    global cursor

    root.withdraw()

    add_user_window = Toplevel()
    add_user_window.iconbitmap("myLogo.ICO")
    add_user_window.title("Qshier | Add User")
    add_user_window.resizable(False, False)

    screen_width = add_user_window.winfo_screenwidth()
    screen_height = add_user_window.winfo_screenheight()

    center_x = int(screen_width / 2 - 800 / 2)
    center_y = int(screen_height / 2 - 500 / 2)

    window_width = 800
    window_height = 500

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_user_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    def user_add():
        global cursor, tree
        username = entry_username.get()
        password = entry_password.get()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        cursor.execute(query, val)
        mydb.commit()

        print(cursor.rowcount, "record inserted.")

        root.deiconify()
        add_user_window.destroy()

    username = Label(add_user_window, text="Username", font=("Helvetica", 16))
    username.pack(pady=(20, 5))
    entry_username = Entry(add_user_window, width=20, font=("Helvetica", 16), bd=3, justify="center", insertwidth=4)
    entry_username.pack(pady=5)

    password = Label(add_user_window, text="Password", font=("arial", 16))
    password.pack(pady=(20, 5))
    entry_password = Entry(add_user_window, show='*', width=20, font=("arial", 16), bd=3, justify="center", insertwidth=4)
    entry_password.pack(pady=5)

    btn_regis = Button(add_user_window, text="Register", padx=20, pady=10, command=user_add)
    btn_regis.pack(padx=5, pady=(20,5))

    def cancel():
        root.deiconify()
        if add_user_window:
            add_user_window.protocol('WM_DELETE_WINDOW', close)
            add_user_window.destroy()

    btn_cancel = Button(add_user_window, text="Cancel", padx=20, pady=10, command=cancel)
    btn_cancel.pack(padx=5, pady=(20,5))

    def close():
        root.deiconify()
        add_user_window.destroy()

    add_user_window.protocol('WM_DELETE_WINDOW', close)


username = Label(form, text="Username", font=("Helvetica", 16))
username.pack(pady=(20, 5))
entry_username = Entry(form, width=20, font=("Helvetica", 16), bd=3, justify="center", insertwidth=4)
entry_username.pack(pady=5)

password = Label(form, text="Password", font=("arial", 16))
password.pack(pady=(20, 5))
entry_password = Entry(form, show='*', width=20, font=("arial", 16), bd=3, justify="center", insertwidth=4)
entry_password.pack(pady=5)

btn_login = Button(form, text="Login", padx=20, pady=10, command=login)
btn_login.pack(padx=5, pady=(20,5))

link_label = tk.Label(form, text="Don't have acount yet?", font=("Garamond", 12), fg="salmon", cursor="hand2")
link_label.pack(pady=10)

link_label.bind("<Button-1>", lambda event: add_user())

root.mainloop()
