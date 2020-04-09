import socket

if __name__ == "__main__":

    UDP_HOST_SERVER = "localhost"
    UDP_PORT = 13000

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("----------FIEK-UDP-CLIENT----------\n")
    print("Type \"HELP\" for more information.\n")

    while True:
        try:
            request = input(">>> ")

            if request == "":
                continue
            elif request == "EXIT" :
                print("Bye!\n")
                break

            clientSocket.sendto(request.encode("utf-8"), (UDP_HOST_SERVER, UDP_PORT))

            returnedData, address = clientSocket.recvfrom(128)

            print(returnedData.decode("utf-8") + '\n')
        except:
            print("Server is not active.\n")

    clientSocket.close()
    quit()