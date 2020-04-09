from socket import *
from datetime import datetime
from numpy.random import randint
from numpy import gcd
from _thread import start_new_thread
import socket

def HELP(data):
    response = "IPADDRESS\nPORT\nCOUNT\nREVERSE\nPALINDROME\nTIME\nGAME\nGCF\nCONVERT\nPRIME\nSQUARE"
    data.send(response.encode("utf-8"))

def IPADDRESS(data):
    response = "IP: " + str(gethostbyname(gethostname()))
    data.send(response.encode("utf-8"))

def PORT(data):
    ip, port = clientAddress
    response = "Port: " + str(port)
    data.send(response.encode("utf-8"))

def COUNT(text, data):
    vowels = 0
    consonants = 0
    for i in text:
        if i in "aeiouyAEIOUY":
            vowels = vowels + 1
        elif i in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ":
            consonants = consonants + 1
    response = "Vowels: " + str(vowels) + "\nConsonants: " + str(consonants)
    data.send(response.encode("utf-8"))

def REVERSE(text, data):
    response = text.strip()
    data.send(response.encode("utf-8"))

def PALINDROME(text, data):
    response = str(True if text == text[::-1] else False)
    data.send(response.encode("utf-8"))

def TIME(data):
    response = str(datetime.now())
    data.send(response.encode("utf-8"))

def GAME(data):
    response = str(randint(1, 35, 5))
    data.send(response.encode("utf-8"))

def GCF(number1, number2, data):
    response = str(gcd(number1, number2))
    data.send(response.encode("utf-8"))

def PRIME(number, data):
    response = str(True)
    if number % 2 == 0:
        response = str(False)
    else:
        for i in range(3, number, 2):
            if number % i == 0:
                response = str(False)
    data.send(response.encode("utf-8"))

def SQUARE(number, clientAddress):
    response = str(number ** 2)
    data.send(response.encode("utf-8"))

def CONVERT(option, number, data):
    response = None
    if option == "cmToFeet":
        response = number * 0.0328084
    elif option == "FeetToCm":
        response = number * 30.48
    elif option == "kmToMiles":
        response = number * 0.621371
    elif option == "MilesToKm":
        response = number * 1.609344
    else:
        raise Exception("wrong convert option")
    response = str(response)
    data.send(response.encode("utf-8"))

def clientThread(data, clientAddress):
    try:
        request = data.recv(128).decode("utf-8").split(' ')

        try:
            if request[0] == "IPADDRESS":
                IPADDRESS(data)
            elif request[0] == "PORT":
                PORT(data)
            elif request[0] == "COUNT":
                COUNT(" ".join(request[1:]), data)
            elif request[0] == "REVERSE":
                REVERSE(" ".join(request[1:]), data)
            elif request[0] == "PALINDROME":
                PALINDROME(" ".join(request[1:]), data)
            elif request[0] == "TIME":
                TIME(data)
            elif request[0] == "GAME":
                GAME(data)
            elif request[0] == "GCF":
                try:
                    temp = int(request[1])
                    temp = int(request[2])
                except Exception:
                    raise Exception("missing/wrong gcf arguments")
                GCF(int(request[1]), int(request[2]), data)
            elif request[0] == "CONVERT":
                try:
                    temp = request[1]
                    temp = float(request[2])
                except Exception:
                    raise Exception("missing/wrong convert arguments")
                CONVERT(request[1], float(request[2]), data)
            elif request[0] == "PRIME":
                try:
                    temp = int(request[1])
                except:
                    raise Exception("missing/wrong prime argument")
                PRIME(float(request[1]), data)
            elif request[0] == "SQUARE":
                try:
                    temp = float(request[1])
                except:
                    raise Exception("missing/wrong square argument")
            elif request[0] == "HELP":
                HELP(data)
            else:
                raise Exception("wrong request")

        except Exception as e:
            response = None
            if str(e) == "wrong request":
                response = "\"" + request[0] + "\" is not recognized as a method."
            elif str(e) == "wrong convert option":
                response = "\"" + request[1] + "\" is not recognized as a convert option."
            elif str(e) == "missing/wrong gcf arguments":
                response = "\"GCF\" takes two integers as arguments."
            elif str(e) == "missing/wrong convert arguments":
                response = "\"CONVERT\" takes two arguments, the convert option and the value to convert."
            data.send(response.encode("utf-8"))

        data.close()
    except:
        return

if __name__ == "__main__":

    TCP_HOST_SERVER = "localhost"
    TCP_PORT = 13000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((TCP_HOST_SERVER, TCP_PORT))
    serverSocket.listen(1)

    print("----------FIEK-TCP-SERVER----------\n")
    print("Server is active...")

    while True:
        try:
            data, clientAddress = serverSocket.accept()

            start_new_thread(clientThread, (data, clientAddress))

        except:
            continue

    serverSocket.close()
    quit()