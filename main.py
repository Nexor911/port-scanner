import socket
import threading

open_ports = []

def scan_range_threaded(start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def udp(target, start_port, end_port):
    for port in range(start_port, end_port +1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.5)
            sock.sendto(b"", (target, port))
            data, server = sock.recvfrom(1024)
            with open(f"{menu}.txt", "a") as f:
                f.write(f"Udp {port}: ответ получен\n")
            print(f"Порт{port}: Открыт")
            open_ports.append(port)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Ошибка при сканировании порта {port}: {e}")
        finally:
            sock.close()
    if open_ports:
        print(f"Открытые Udp порты: {open_ports}")
    else:
        print("Не найдено открытых udp портов")
    return open_ports

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

protocol = input("Протокол tcp или udp: ").lower()
if protocol == "tcp":
    print(f"Сканирование tcp  портов {target} от {start_port} до {end_port}...")
    scan_range_threaded(start_port, end_port)
    print(f"Сканирование завершено и сохранено в файл {menu}")
elif protocol == "udp":
    print(f"Сканирование udp портов {target} от {start_port} до {end_port}...")
    udp(target, start_port, end_port)
else:
    print("Неверный выбор")
