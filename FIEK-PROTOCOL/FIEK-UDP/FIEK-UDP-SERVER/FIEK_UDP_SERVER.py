from socket import *
from datetime import datetime
from numpy.random import randint
from numpy import gcd
import socket

def HELP(clientAddress):
    response = "IPADDRESS\nPORT\nCOUNT\nREVERSE\nPALINDROME\nTIME\nGAME\nGCF\nCONVERT\nPRIME\nSQUARE"
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def IPADDRESS(clientAddress):
    response = "IP: " + str(gethostbyname(gethostname()))
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def PORT(clientAddress):
    ip, port = clientAddress
    response = "Port: " + str(port)
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def COUNT(text, clientAddress):
    vowels = 0
    consonants = 0
    for i in text:
        if i in "aeiouyAEIOUY":
            vowels = vowels + 1
        elif i in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ":
            consonants = consonants + 1
    response = "Vowels: " + str(vowels) + "\nConsonants: " + str(consonants)
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def REVERSE(text, clientAddress):
    response = text.strip()
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def PALINDROME(text, clientAddress):
    response = str(True if text == text[::-1] else False)
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def TIME(clientAddress):
    response = str(datetime.now())
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def GAME(clientAddress):
    response = str(randint(1, 35, 5))
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def GCF(number1, number2, clientAddress):
    response = str(gcd(number1, number2))
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def CONVERT(option, number, clientAddress):
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
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def PRIME(number, clientAddress):
    response = str(True)
    if number % 2 == 0:
        response = str(False)
    else:
        for i in range(3, number, 2):
            if number % i == 0:
                response = str(False)
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

def SQUARE(number, clientAddress):
    response = str(number ** 2)
    serverSocket.sendto(response.encode("utf-8"), clientAddress)

if __name__ == "__main__":

    UDP_HOST_SERVER = "localhost"
    UDP_PORT = 13000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((UDP_HOST_SERVER, UDP_PORT))

    print("----------FIEK-UDP-SERVER----------\n")
    print("Server is active...")

    while True:
        data, clientAddress = serverSocket.recvfrom(128)

        request = data.decode("utf-8").split(" ")

        try:
            if request[0] == "IPADDRESS":
                IPADDRESS(clientAddress)
            elif request[0] == "PORT":
                PORT(clientAddress)
            elif request[0] == "COUNT":
                COUNT(" ".join(request[1:]), clientAddress)
            elif request[0] == "REVERSE":
                REVERSE(" ".join(request[1:]), clientAddress)
            elif request[0] == "PALINDROME":
                PALINDROME(" ".join(request[1:]), clientAddress)
            elif request[0] == "TIME":
                TIME(clientAddress)
            elif request[0] == "GAME":
                GAME(clientAddress)
            elif request[0] == "GCF":
                try:
                    temp = int(request[1])
                    temp = int(request[2])
                except Exception:
                    raise Exception("missing/wrong gcf arguments")
                GCF(int(request[1]), int(request[2]), clientAddress)
            elif request[0] == "CONVERT":
                try:
                    temp = request[1]
                    temp = float(request[2])
                except Exception:
                    raise Exception("missing/wrong convert arguments")
                CONVERT(request[1], float(request[2]), clientAddress)
            elif request[0] == "PRIME":
                try:
                    temp = int(request[1])
                except:
                    raise Exception("missing/wrong prime argument")
                PRIME(int(request[1]), clientAddress)
            elif request[0] == "SQUARE":
                try:
                    temp = float(request[1])
                except:
                    raise Exception("missing/wrong square argument")
                SQUARE(float(request[1]), clientAddress)
            elif request[0] == "HELP":
                HELP(clientAddress)
            else:
                raise Exception("wrong method")

        except Exception as e:
            response = ""
            if str(e) == "wrong method":
                response = "\"" + request[0] + "\" is not recognized as a method."
            elif str(e) == "wrong convert option":
                response = "\"" + request[1] + "\" is not recognized as a convert option."
            elif str(e) == "missing/wrong gcf arguments":
                response = "\"GCF\" takes two integers as arguments."
            elif str(e) == "missing/wrong convert arguments":
                response = "\"CONVERT\" takes two arguments, the convert option and the value to convert."
            elif str(e) == "missing/wrong prime argument":
                response = "\"PRIME\" takes an integer as argument."
            elif str(e) == "missing/wrong square argument":
                response = "\"SQUARE\" takes a number as argument."
            serverSocket.sendto(response.encode("utf-8"), clientAddress)

    serverSocket.close()
    quit()