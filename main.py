import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, ttk
from datetime import datetime

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f8f9fa")

        self.categories = {}
        self.transactions = []
        self.categories_visible = False
        self.transactions_visible = False
        self.create_layout()

    def create_layout(self):
        self.left_frame = tk.Frame(self.root, bg="#e3f2fd", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, bg="#ffffff", width=400)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.add_category_section()
        self.add_recent_transactions_section()

    def add_category_section(self):
        title_frame = tk.Frame(self.left_frame, bg="#e3f2fd")
        title_frame.pack(fill=tk.X, pady=5)

        label = tk.Label(title_frame, text="Categories", font=("Arial", 14, "bold"), bg="#e3f2fd")
        label.pack(side=tk.LEFT, padx=10)

        self.toggle_categories_btn = tk.Button(
            title_frame, text="▶", command=self.toggle_categories, bg="#4CAF50", fg="white", width=3
        )
        self.toggle_categories_btn.pack(side=tk.RIGHT, padx=10)

        self.category_listbox = tk.Listbox(self.left_frame, font=("Arial", 10), height=15)
        self.category_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.category_listbox.pack_forget()

        self.add_category_buttons = tk.Frame(self.left_frame, bg="#e3f2fd")
        self.add_category_buttons.pack(fill=tk.X, pady=5)

        self.btn_add_category = tk.Button(
            self.add_category_buttons, text="Add Category", bg="#4CAF50", fg="white", font=("Arial", 10),
            command=self.add_category, height=1, width=12
        )
        self.btn_add_category.pack(side=tk.LEFT, padx=5)

        self.btn_delete_category = tk.Button(
            self.add_category_buttons, text="Delete Selected", bg="#d32f2f", fg="white", font=("Arial", 10),
            command=self.delete_selected_category, height=1, width=12
        )
        self.btn_delete_category.pack(side=tk.LEFT, padx=5)

        self.btn_edit_category = tk.Button(
            self.add_category_buttons, text="Edit Category", bg="#ff9800", fg="white", font=("Arial", 10),
            command=self.edit_category, height=1, width=12
        )
        self.btn_edit_category.pack(side=tk.LEFT, padx=5)

        self.btn_delete_all = tk.Button(
            self.add_category_buttons, text="Delete All", bg="#f44336", fg="white", font=("Arial", 10),
            command=self.delete_all_categories, height=1, width=12
        )
        self.btn_delete_all.pack(side=tk.LEFT, padx=5)

    def add_recent_transactions_section(self):
        title_frame = tk.Frame(self.right_frame, bg="#ffffff")
        title_frame.pack(fill=tk.X, pady=5)

        label = tk.Label(title_frame, text="Recent Transactions", font=("Arial", 14, "bold"), bg="#ffffff")
        label.pack(side=tk.LEFT, padx=10)

        self.toggle_transactions_btn = tk.Button(
            title_frame, text="▶", command=self.toggle_transactions, bg="#03A9F4", fg="white", width=3
        )
        self.toggle_transactions_btn.pack(side=tk.RIGHT, padx=10)

        self.transaction_listbox = tk.Listbox(self.right_frame, font=("Arial", 10), height=15)
        self.transaction_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.transaction_listbox.pack_forget()

        self.add_transaction_buttons = tk.Frame(self.right_frame, bg="#ffffff")
        self.add_transaction_buttons.pack(fill=tk.X, pady=5)

        self.btn_add_transaction = tk.Button(
            self.add_transaction_buttons, text="Add Transaction", bg="#03A9F4", fg="white", font=("Arial", 10),
            command=self.add_transaction, height=1, width=12
        )
        self.btn_add_transaction.pack(side=tk.LEFT, padx=5)

        self.btn_delete_transaction = tk.Button(
            self.add_transaction_buttons, text="Delete Selected", bg="#d32f2f", fg="white", font=("Arial", 10),
            command=self.delete_selected_transaction, height=1, width=12
        )
        self.btn_delete_transaction.pack(side=tk.LEFT, padx=5)

        self.btn_edit_transaction = tk.Button(
            self.add_transaction_buttons, text="Edit Transaction", bg="#ff9800", fg="white", font=("Arial", 10),
            command=self.edit_transaction, height=1, width=12
        )
        self.btn_edit_transaction.pack(side=tk.LEFT, padx=5)

        self.btn_delete_all_transactions = tk.Button(
            self.add_transaction_buttons, text="Delete All", bg="#f44336", fg="white", font=("Arial", 10),
            command=self.delete_all_transactions, height=1, width=12
        )
        self.btn_delete_all_transactions.pack(side=tk.LEFT, padx=5)

    def toggle_categories(self):
        if self.categories_visible:
            self.category_listbox.pack_forget()
            self.toggle_categories_btn.config(text="▶")
        else:
            self.category_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.toggle_categories_btn.config(text="▼")
        self.categories_visible = not self.categories_visible

    def toggle_transactions(self):
        if self.transactions_visible:
            self.transaction_listbox.pack_forget()
            self.toggle_transactions_btn.config(text="▶")
        else:
            self.transaction_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.toggle_transactions_btn.config(text="▼")
        self.transactions_visible = not self.transactions_visible

    def add_category(self):
        self.popup_two_inputs("Add Category", "Category Name:", "Max Budget:", self.save_category)

    def add_transaction(self):
        selected_index = self.category_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a category first!")
            return

        category_name = list(self.categories.keys())[selected_index[0]]
        self.popup_two_inputs("Add Transaction", "Transaction Name:", "Transaction Amount:",
                              lambda name, amount: self.save_transaction(name, amount, category_name))

    def save_category(self, name, max_budget):
        try:
            max_budget = float(max_budget)
            if not name or max_budget <= 0:
                raise ValueError("Invalid inputs")
            self.categories[name] = {"max": max_budget, "spent": 0}
            self.refresh_categories()
            messagebox.showinfo("Success", f"Category '{name}' added with max budget ${max_budget:.2f}!")
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs for category!")

    def save_transaction(self, name, amount, category_name):
        try:
            amount = float(amount)
            if not name or amount <= 0:
                raise ValueError("Invalid inputs")
            category = self.categories[category_name]
            if category["spent"] + amount > category["max"]:
                messagebox.showwarning("Warning", "Insufficient budget for this transaction!")
                return

            category["spent"] += amount
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remaining = category["max"] - category["spent"]

            self.transactions.append({
                "name": name, "amount": amount, "category": category_name,
                "remaining": remaining, "time": current_time
            })
            self.refresh_categories()
            self.refresh_recent_transactions()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs for transaction!")

    def delete_selected_transaction(self):
        selected_index = self.transaction_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a transaction to delete!")
            return
        transaction = self.transactions[selected_index[0]]
        confirm = messagebox.askyesno("Delete Transaction", f"Are you sure you want to delete the transaction '{transaction['name']}'?")
        if confirm:
            self.transactions.remove(transaction)
            category_name = transaction["category"]
            self.categories[category_name]["spent"] -= transaction["amount"]
            self.refresh_categories()
            self.refresh_recent_transactions()

    def delete_all_transactions(self):
        confirm = messagebox.askyesno("Delete All Transactions", "Are you sure you want to delete all transactions?")
        if confirm:
            self.transactions.clear()
            for category in self.categories.values():
                category["spent"] = 0
            self.refresh_categories()
            self.refresh_recent_transactions()

    def delete_selected_category(self):
        selected_index = self.category_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a category to delete!")
            return
        category_name = list(self.categories.keys())[selected_index[0]]
        confirm = messagebox.askyesno("Delete Category", f"Are you sure you want to delete the category '{category_name}'?")
        if confirm:
            del self.categories[category_name]
            self.refresh_categories()

    def delete_all_categories(self):
        confirm = messagebox.askyesno("Delete All Categories", "Are you sure you want to delete all categories?")
        if confirm:
            self.categories.clear()
            self.refresh_categories()

    def refresh_categories(self):
        self.category_listbox.delete(0, tk.END)
        for category, data in self.categories.items():
            self.category_listbox.insert(tk.END, f"{category}: Max Budget: {data['max']}, Spent: {data['spent']}")

    def refresh_recent_transactions(self):
        self.transaction_listbox.delete(0, tk.END)
        for trans in self.transactions:
            self.transaction_listbox.insert(tk.END, f"{trans['name']} - {trans['amount']} - {trans['time']}")

    def popup_two_inputs(self, title, label1, label2, save_command):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("350x250")  # تعديل حجم النافذة ليشمل زر الحفظ بشكل أفضل

        label1 = tk.Label(popup, text=label1)
        label1.pack(padx=5, pady=5)

        entry1 = tk.Entry(popup)
        entry1.pack(padx=5, pady=5)

        label2 = tk.Label(popup, text=label2)
        label2.pack(padx=5, pady=5)

        entry2 = tk.Entry(popup)
        entry2.pack(padx=5, pady=5)

        def on_save():
            save_command(entry1.get(), entry2.get())
            popup.destroy()

        save_btn = tk.Button(popup, text="Save", command=on_save)
        save_btn.pack(pady=10)

    def edit_category(self):
        selected_index = self.category_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a category to edit!")
            return
        
        category_name = list(self.categories.keys())[selected_index[0]]
        current_data = self.categories[category_name]
        self.popup_two_inputs(
            "Edit Category", 
            "Category Name:", 
            "Max Budget:", 
            lambda name, max_budget: self.update_category(category_name, name, max_budget)
        )

    def update_category(self, old_name, new_name, new_max_budget):
        try:
            new_max_budget = float(new_max_budget)
            if not new_name or new_max_budget <= 0:
                raise ValueError("Invalid inputs")
            
            # Remove the old category and add the updated one
            del self.categories[old_name]
            self.categories[new_name] = {"max": new_max_budget, "spent": 0}
            
            self.refresh_categories()
            messagebox.showinfo("Success", f"Category '{old_name}' updated to '{new_name}' with max budget ${new_max_budget:.2f}!")
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs for category!")

    def edit_transaction(self):
        selected_index = self.transaction_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a transaction to edit!")
            return
        
        transaction = self.transactions[selected_index[0]]
        
        # عرض نافذة مع تعديل الفئة والاسم والمبلغ
        popup = Toplevel(self.root)
        popup.title("Edit Transaction")
        popup.geometry("350x250")

        label1 = tk.Label(popup, text="Transaction Name:")
        label1.pack(padx=5, pady=5)

        entry1 = tk.Entry(popup)
        entry1.insert(0, transaction["name"])  # ضع الاسم الحالي
        entry1.pack(padx=5, pady=5)

        label2 = tk.Label(popup, text="Transaction Amount:")
        label2.pack(padx=5, pady=5)

        entry2 = tk.Entry(popup)
        entry2.insert(0, str(transaction["amount"]))  # ضع المبلغ الحالي
        entry2.pack(padx=5, pady=5)

        label3 = tk.Label(popup, text="Select Category:")
        label3.pack(padx=5, pady=5)

        category_options = list(self.categories.keys())
        category_combobox = ttk.Combobox(popup, values=category_options)
        category_combobox.set(transaction["category"])  # تعيين الفئة الحالية
        category_combobox.pack(padx=5, pady=5)

        def on_save():
            name = entry1.get()
            amount = entry2.get()
            category = category_combobox.get()
            self.update_transaction(transaction, name, amount, category)
            popup.destroy()

        save_btn = tk.Button(popup, text="Save", command=on_save)
        save_btn.pack(pady=10)

    def update_transaction(self, transaction, new_name, new_amount, new_category):
        try:
            new_amount = float(new_amount)
            if new_amount <= 0 or not new_name or not new_category:
                raise ValueError("Invalid inputs")
            
            # Update the transaction
            category = self.categories[transaction["category"]]
            category["spent"] -= transaction["amount"]
            category["spent"] += new_amount
            transaction["name"] = new_name
            transaction["amount"] = new_amount
            transaction["category"] = new_category

            # Update the remaining budget for the selected category
            remaining = category["max"] - category["spent"]
            transaction["remaining"] = remaining

            self.refresh_categories()
            self.refresh_recent_transactions()
            messagebox.showinfo("Success", "Transaction updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs for transaction!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
