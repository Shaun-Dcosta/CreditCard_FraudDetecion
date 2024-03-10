import socket
import pickle
import threading

fraud_number = {}
lock = threading.Lock()

def fraud_detection(transaction_data):
    if transaction_data['stolen_or_lost'] == 1 and transaction_data['cvv_number']==None:
        card_number = transaction_data.get('sender_card_number')
        fraud_number[card_number]=1
        return True, f"Card reported as stolen or lost: {card_number}"
    else:
        card_number = transaction_data.get('sender_card_number', 0)
        amount = transaction_data.get('amount', 0)
        cvv = transaction_data.get('cvv_number', 0)

        with lock:
            if card_number in fraud_number:
                return True, "Fraudulent transaction detected"
            else:
                return False, None

def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(1024)
        if not data:
            return

        transaction_data = pickle.loads(data)

        is_fraudulent, message = fraud_detection(transaction_data)
        if not is_fraudulent:
            print(f"Received Transaction Data from {addr}: {transaction_data}")
        else:
            print(f"Transaction from {addr}: {transaction_data} was blocked. {message}")
        client_socket.send(pickle.dumps({'is_fraudulent': is_fraudulent, 'message': message}))

    except Exception as e:
        print(f"Error handling client {addr}: {e}")

    finally:
        client_socket.close()
        print(f"Connection from {addr} closed")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.1.4'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()