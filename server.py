
import socket

# 이전에 받은 데이터를 저장할 리스트
productlist = []

def start_server():
    # 서버의 IP 주소와 포트 번호
    server_ip = '192.168.137.232'  # 서버의 IP 주소 입력
    server_port = 8000  # 서버의 포트 번호 입력

    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 소켓을 IP 주소와 포트 번호에 바인딩
        server_socket.bind((server_ip, server_port))

        # 클라이언트로부터의 연결을 기다림
        server_socket.listen(1)
        print("Server is listening for incoming connections...")

        while True:  # 클라이언트의 연결을 계속해서 받기 위해 while 루프 사용
            # 클라이언트의 연결을 받음
            client_socket, client_address = server_socket.accept()
            print("Connection established with", client_address)

            while True:  # 클라이언트와의 통신을 계속해서 수행하기 위해 while 루프 사용
                # 클라이언트로부터 데이터 수신
                data = client_socket.recv(1024).decode()
                if not data:
                    break  # 데이터가 없으면 내부 루프 종료
                
                print("Received data from client:", data)

                # 받은 데이터를 productlist에 추가
                productlist.append(data)
                print("productlist: ", productlist)

                # 클라이언트에게 응답 전송
                response = "Message received"
                client_socket.sendall(response.encode())
             

            # 클라이언트와의 연결 종료
            client_socket.close()

    except Exception as e:
        print("Error occurred in server:", e)
    finally:
        # 소켓 닫기
        server_socket.close()

# 서버 시작
start_server()