import socket
import threading

print("Это меню\nНажми (1) для сканирования новой цели\nНажми (2) для выхода")
sel = input(": ")
if sel == "1":
    menu = input("Name: ")
    with open(f"{menu}.txt", "w") as f:
        f.close()
    x = input("введите айпи адрес: ")
    a = int(input("стартовый порт: "))
    b = int(input("конечный порт: "))
    target = x
    start_port = a
    end_port = b
elif sel == "2":
        print("Exit...")
        exit()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port}: Open")
            with open(f"{menu}.txt", "a") as f:
                f.write(f"Порт {port}: Открыт\n")
        sock.close()
    except socket.error as e:
        pass

def scan_range():
    for port in range(start_port, end_port + 1):
        scan_port(port)

def scan_range_threaded():
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

print(f"Сканирование портов {target} от {start_port} до {end_port}...")
scan_range_threaded()
print(f"Сканирование завершено и сохранено в файл {menu}.")
