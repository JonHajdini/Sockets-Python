import socket

if __name__ == "__main__":

    TCP_HOST_SERVER = "localhost"
    TCP_PORT = 13000

    print("----------FIEK-TCP-CLIENT----------\n")
    print("Type \"HELP\" for more information.\n")

    while True:
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((TCP_HOST_SERVER, TCP_PORT))

            request = input(">>> ")

            if request == "":
                continue
            elif request == "EXIT":
                print("Bye!\n")
                break

            clientSocket.send(request.encode("utf-8"))

            returnedData = clientSocket.recv(128)

            print(returnedData.decode("utf-8") + '\n')

        except:
            print("Server is not active.")
            break

    clientSocket.close()
    quit()