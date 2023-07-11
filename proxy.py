import socket
import time as t
SERVER_IP = '54.71.128.194'
SERVER_PORT = 92
LISTEN_PORT = 9090

def get_years_and_genre(msg):
    '''
    The func recieve client msg and return first year ,secind year, genre
    :param msg: client msg
    :type msg: string
    :return: first year ,secind year, genre
    :rtype: string, stirng, string
    '''
    msg = msg.split('&')
    years = msg[1]
    years = years.split(':')
    years = years[1]
    years = years.split('-')
    genre = msg[0]
    genre = genre.split(':')
    genre = genre[1]
    return years[0], years[1], genre

def is_valid(first_year , second_year, genre) -> str:
    '''
    The func is checking if the years are  not years sent into the future
    or the genre is bigger then 20 letters
    :param firstYear: the first data that client enter
    :type firstYear: int
    :param secondYear: the second data that client enter
    :type secondYear: int
    :param genre: genre of the movie
    :type genre: string
    :return: the error
    :rtype: string
    '''
    GENRE_LEN = 20
    if int(first_year) > 1999 or int(second_year) > 2000:
        return "Invalid year!"
    elif len(genre) > GENRE_LEN:
        return "Invalid Genre length!"
    else:
        return None;

def is_num_client_valid(num_client):
    '''
    The func check if the num of clients and return is it exceet the range
    of accept count
    :param num_client: num of client that send query
    :type num_client: int
    :return: if it exceeted the accepting range
    :rtype: int , bool
    '''
    if num_client > 5:
        return num_client, True
    return num_client+1, False

def proxy_server():
    '''
    The func (proxy server) get the query from client then send to main server
    also proxy fixing the errors then it sendes beck to client
    '''
    num_client=0
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('', LISTEN_PORT)
            listening_sock.bind(server_address)
            listening_sock.listen(5)
            num_client, is_exceed = is_num_client_valid(num_client)
            if is_exceed == True:
                server_msg = 'ERROR#"No more request allows! Please wait sec"'
                num_client = 0
                t.sleep(1)
            else:
                client_soc, client_address = listening_sock.accept()
                client_msg = client_soc.recv(1024)
                client_msg = client_msg.decode()

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    server_address = (SERVER_IP, SERVER_PORT)
                    sock.connect(server_address)
                    msg_client = client_msg
                    sock.sendall(msg_client.encode())
                    server_msg = sock.recv(1024)
                    server_msg = server_msg.decode()

                    first_year, second_year, genre = get_years_and_genre(client_msg)
                    if 'SERVERERROR' in str(server_msg) and len(genre) < 20:
                        server_msg = str(server_msg)
                        server_msg = server_msg.replace('SERVER','')
                        server_msg = 'ERROR' + server_msg[server_msg.index('#'):]
                    elif 'France' in str(server_msg):
                        server_msg = 'ERROR#"France is banned!"'
                    elif is_valid(first_year, second_year, genre) != None:
                        server_msg = 'ERROR#' + '"' + is_valid(first_year, second_year, genre) + '"'
                    else:
                        msg = list(str(server_msg).split('&'))
                        msg[7] = msg[7][:(len(msg[7])-4)] + '.' + msg[7][(len(msg[7])-4):]
                        server_msg = '&'.join(msg)

                print(server_msg)
            server_msg = server_msg.encode()
            client_soc.sendall(server_msg)

def main():
    proxy_server()

if __name__ == "__main__":
    main()