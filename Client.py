import tkinter as tk
from tkinter import messagebox, Toplevel
import socket
import pickle

fraud_number={}

def send_transaction_data(transaction_data):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.1.4' 
        port = 12345 
        client_socket.connect((host, port))

        client_socket.send(pickle.dumps(transaction_data))

        result_data = client_socket.recv(1024)
        result = pickle.loads(result_data)

        if result['is_fraudulent']:
            print("Fraud Detection Result:", result['is_fraudulent'])
            messagebox.showerror("Fraud Detected", "Fraudulent Transaction Detected! Please try again.")
        else:
            print("Transaction Successful")
            messagebox.showinfo("Success", "Transaction Successful!")

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "An error occurred during the transaction.")

    finally:
        client_socket.close()


def open_report_stolen_window():
    report_stolen_window = Toplevel(root)
    report_stolen_window.title("Report Stolen Card")

    report_stolen_window.geometry("300x200")

    def report_stolen():
        card_number = card_number_entry.get()
        cvv = cvv_entry.get()

        fraud_number[card_number]=1

        transaction_data = transaction_data = {
                'sender_card_number': card_number,
                'cvv_number': cvv,
                'amount': None,
                'receiver_card_number':None,
                'stolen_or_lost':fraud_number[card_number]
            }
        
        send_transaction_data(transaction_data)
        
        print(f"Card reported as stolen\nCard Number: {card_number}\nCVV: {cvv}")
        report_stolen_window.destroy()

    card_number_label = tk.Label(report_stolen_window, text="Card Number:")
    card_number_label.pack(pady=5)
    card_number_entry = tk.Entry(report_stolen_window, width=30)
    card_number_entry.pack(pady=5)

    cvv_label = tk.Label(report_stolen_window, text="CVV:")
    cvv_label.pack(pady=5)
    cvv_entry = tk.Entry(report_stolen_window, width=30)
    cvv_entry.pack(pady=5)

    report_button = tk.Button(report_stolen_window, text="Report Stolen", command=report_stolen)
    report_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Credit Card Transaction")

    
    root.geometry("400x300")

    def submit():
        try:
            sender_card_number = sender_card_entry.get()
            cvv_number = cvv_entry.get()
            amount = amount_entry.get()
            receiver_card_number = receiver_card_entry.get()

            if sender_card_number in fraud_number:
                transaction_data = {
                'sender_card_number': sender_card_number,
                'cvv_number': cvv_number,
                'amount': amount,
                'receiver_card_number': receiver_card_number,
                'stolen_or_lost':1
                }
            else:
                transaction_data = {
                'sender_card_number': sender_card_number,
                'cvv_number': cvv_number,
                'amount': amount,
                'receiver_card_number': receiver_card_number,
                'stolen_or_lost':0
            }
                
            send_transaction_data(transaction_data)

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Error", "An error occurred during the transaction.")

    sender_card_label = tk.Label(root, text="Sender's Card Number:")
    sender_card_label.grid(row=0, column=0, padx=10, pady=5)
    sender_card_entry = tk.Entry(root, width=30)
    sender_card_entry.grid(row=0, column=1, padx=10, pady=5)

    cvv_label = tk.Label(root, text="CVV Number:")
    cvv_label.grid(row=1, column=0, padx=10, pady=5)
    cvv_entry = tk.Entry(root, width=30)
    cvv_entry.grid(row=1, column=1, padx=10, pady=5)

    amount_label = tk.Label(root, text="Amount:")
    amount_label.grid(row=2, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(root, width=30)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    receiver_card_label = tk.Label(root, text="Receiver's Card Number:")
    receiver_card_label.grid(row=3, column=0, padx=10, pady=5)
    receiver_card_entry = tk.Entry(root, width=30)
    receiver_card_entry.grid(row=3, column=1, padx=10, pady=5)

    report_stolen_button = tk.Button(root, text="Report Stolen", command=open_report_stolen_window)
    report_stolen_button.grid(row=4, column=0, columnspan=2, pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()
