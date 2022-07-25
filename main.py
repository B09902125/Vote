from logging.config import valid_ident
import random
from stat import ST_SIZE
from tkinter import N
import numpy as np
import os
from colorama import Fore, init

init(autoreset=True)

path1 = 'name.txt'
path2 = 'random.txt'
path3 = 'error.txt'


def name_record(name):
    if name == 'ticket checking' or name == '驗票':
        ticket_checking()
        return 0
    elif len(name) > 4 or len(name) < 2 or name.encode( 'UTF-8' ).isalnum() == True:
        print("姓名輸入錯誤!")
        voter = input("請輸入投票人姓名 : ")
        if voter == 'end':
            return -1
        else:
            revl = name_record(voter)
            return revl
    else:
        with open(path1, 'r', encoding='utf-8') as f:
            for line in f:
                if line == (name + '\n'):
                    print(Fore.YELLOW + "警告!已領過投票序號!")
                    return 0
        last_three_digit = input("請輸入學號末三碼 : ")
        if last_three_digit == 'end':
            return -1
        while (str.isdigit(last_three_digit) == False) or (len(last_three_digit) != 3):
            print("輸入格式錯誤!")
            last_three_digit = input("請輸入學號末三碼 : ")
            if last_three_digit == -1:
                return -1
        with open(path1, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
        return last_three_digit
    
            
def random_num_generator(seed):
    new_rand_num = random.randrange(100000000,1000000000)
    with open(path2, 'r') as f:
        if os.stat(path2).st_size != 0:     
            for line in f:
                if line == new_rand_num:
                    new_rand_num += seed
                    break
    new_rand_num = convertor_to_36(new_rand_num)
    with open(path2, 'a') as f:
        f.write(str(new_rand_num) + '\n')
    
    print('你的個人投票序號為 ', new_rand_num ,'\n')

def ticket_checking():
    valid_voter_num = 0
    invalid_voter_num = 0
    dict_for_check = {}
    while 1:
        checked_num = input('請輸入序號 : ') + '\n'
        if checked_num == 'end\n':
            print('===================')
            print('總計有效投票數 :', valid_voter_num)
            print('總計無效投票數 :', invalid_voter_num)
            print('===================')
            break
        else:
            with open(path2, 'r') as f:
                for line in f:
                    if checked_num == line:
                        if dict_for_check.get(checked_num, 0) == 0:
                            dict_for_check[checked_num] = 1
                            valid_voter_num += 1
                            print(Fore.GREEN + 'Succeed')
                        else:
                            dict_for_check[checked_num] += 1
                        break    
                
                if dict_for_check.get(checked_num, 0) == 0:
                    invalid_voter_num += 1
                    print(Fore.RED + '*******False number %s' %checked_num)
                    with open(path3, 'a') as f:
                        f.write('False number ' + str(checked_num))
                elif dict_for_check.get(checked_num) > 1:
                    invalid_voter_num += 1
                    print(Fore.RED + f'********Somebody votes {dict_for_check.get(checked_num)} times. Please check number {checked_num}')
                    with open(path3, 'a') as f:
                        f.write(f'Somebody votes {dict_for_check.get(checked_num)} times. Please check number ' + str(checked_num))
    dict_for_check.clear()
    
def convertor_to_36 (num):
    num_rep = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f',16:'g',
               17:'h',18:'i',19:'j',20:'k',21:'l',22:'m',23:'n',24:'o',
               25:'p',26:'q',27:'r',28:'s',29:'t',30:'u',31:'v',32:'w',
               33:'x',34:'y',35:'z'}
    
    new_num_str = ''
    current = int(num)
    while current != 0:
        remainder = int(current % 36)
        if 36 > remainder > 9 :
            remainder_str = num_rep.get(remainder)
        else:
            remainder_str = str(remainder)
        new_num_str = remainder_str + new_num_str
        current = (current - remainder) / 36
    return new_num_str

              
# main
while 1:
    voter = input("請輸入投票人姓名 : ")
    if voter == 'end':
        break
    elif voter != ('ticket checking' and '驗票'):
        seed_input = name_record(voter)
        if seed_input == -1:
            break
        elif seed_input != 0:
            random_num_generator(seed_input)
    else:
        ticket_checking()
     
        
    