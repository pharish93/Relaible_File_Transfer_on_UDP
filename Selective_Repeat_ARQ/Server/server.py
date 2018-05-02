import socket
import struct
import random
import sys

COMMAND_LINE_INPUT  = True

def Verify_Check_sum(data,check_sum):
    sum_element = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            element_16bits = ord(data[i]) + (ord(data[i + 1]) << 8)
            k = sum_element + element_16bits
            a = (k & 0xffff)
            b = k >> 16
            sum_element = a + b  # carry around addition
    Recieved_data_check_sum = sum_element & 0xffff
    check_sum_verified = Recieved_data_check_sum & check_sum
    return check_sum_verified

def Make_Ack_Header(seq_num):
    ackPacket = struct.pack('!IHH', seq_num, 0, 43690)  # SEQUENCE NUMBER BEING ACKED
    return ackPacket


def Decode_packet(packet_data):
    Header = struct.unpack('!IHH', packet_data[0:8])
    seq_num = Header[0]
    check_sum = Header[1]
    data = packet_data[8:]
    valid_frame = False
    check_sum_verified = Verify_Check_sum(data,check_sum)
    #print data

    if check_sum_verified == 0 and Header[2] == 21845:
        valid_frame = True

    return valid_frame, seq_num, data


def main():
    Server_Soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.gethostbyname(socket.gethostname())
    print ip

    if COMMAND_LINE_INPUT:
        port = int(sys.argv[1])
        file_name = sys.argv[2]
        prob = float(sys.argv[3])
    else :
        port = 7735
        file_name = 'Harish_testing.txt'
        prob = 0.05


    Server_Soc.bind((ip, port))
    prev_sequence_number = -1
    temp_data_buffer = {}
    Max_seq = 0


    flag = True
    while flag or len(temp_data_buffer) <= Max_seq:
        packet_data, Client_Address = Server_Soc.recvfrom(2048)
        valid_frame, sequence_number, data = Decode_packet(packet_data)

        if valid_frame:
            if random.uniform(0, 1) > prob:  # packet accepted
                Ack_packet = Make_Ack_Header(sequence_number)
                Server_Soc.sendto(Ack_packet, Client_Address)
                if data == 'endofframe':
                    flag = False
                    Max_seq = sequence_number
                    print 'End of file command in data format received ' + str(Max_seq)
                temp_data_buffer[int(sequence_number)] = data
                #print len(temp_data_buffer), Max_seq

            else:
                print 'Packet Loss, Sequence Number =' + str(sequence_number)

    print 'Complete file received - Closing connection'
    file_writer = open(file_name, 'wb')
    for i in range(0, Max_seq-1):
        file_writer.write(temp_data_buffer[i])
    file_writer.close()
    Server_Soc.close()


if __name__ == '__main__':
    main()
