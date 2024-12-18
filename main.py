import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button
from datetime import datetime


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("800x500")
        self.root.configure(bg="#f8f9fa")

        # بيانات التطبيق
        self.categories = {}
        self.transactions = []

        # حالة الإخفاء/الإظهار
        self.categories_visible = False
        self.transactions_visible = False

        # إنشاء تقسيم الشاشة
        self.create_layout()

    def create_layout(self):
        # تقسيم الشاشة إلى نصفين
        self.left_frame = tk.Frame(self.root, bg="#e3f2fd", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, bg="#ffffff", width=400)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # إضافة أقسام الكاتيجوري
        self.add_category_section()

        # إضافة أقسام الريسينت ترانزاكشن
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

        self.btn_add_category = tk.Button(
            self.left_frame, text="Add Category", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
            command=self.add_category, height=2
        )
        self.btn_add_category.pack(fill=tk.X, padx=10, pady=5)

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

        self.btn_add_transaction = tk.Button(
            self.right_frame, text="Add Transaction", bg="#03A9F4", fg="white", font=("Arial", 12, "bold"),
            command=self.add_transaction, height=2
        )
        self.btn_add_transaction.pack(fill=tk.X, padx=10, pady=5)

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

    def refresh_categories(self):
        self.category_listbox.delete(0, tk.END)
        for category, details in self.categories.items():
            remaining = details["max"] - details["spent"]
            self.category_listbox.insert(tk.END, f"{category} (Remaining: ${remaining:.2f})")

    def refresh_recent_transactions(self):
        self.transaction_listbox.delete(0, tk.END)
        for t in reversed(self.transactions[-10:]):
            self.transaction_listbox.insert(tk.END,
                                            f"{t['name']} - ${t['amount']:.2f} | Category: {t['category']} "
                                            f"| Remaining: ${t['remaining']:.2f} | {t['time']}")

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

    def popup_two_inputs(self, title, label1, label2, save_function):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")
        popup.resizable(False, False)

        Label(popup, text=label1).pack(pady=5)
        entry1 = Entry(popup, width=30)
        entry1.pack(pady=5)

        Label(popup, text=label2).pack(pady=5)
        entry2 = Entry(popup, width=30)
        entry2.pack(pady=5)

        Button(popup, text="Submit", command=lambda: [save_function(entry1.get(), entry2.get()), popup.destroy()])\
            .pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
