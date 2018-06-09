#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 2018.06.09
# V0.1.5
# 内容：
# 1. 修复：修复logging 输出日志文件时，报错UnicodeEncodeError:  已修复2018.06.08
# 2. 添加：备份指定格式的文件（.mp3, .pdf, .jpg, .） 已完成 2018.06.07
# 3. 优化
# 


__author__  = "Hyper Liu"
__status__  = "production"
__version__ = "V0.1.5"
__date__    = "2018.06.09"

    
import hashlib
import os
import shutil
import time, datetime
import logging


format='%(asctime)s - %(levelname)s: %(message)s' # 设置日志格式
datefmt = '%Y-%m-%d %I:%M:%S %p'    # 设置时间格式
logging.basicConfig(filename='HyperBackup.log',filemode='a', level=logging.DEBUG, format = format, datefmt=datefmt)


def md5check(filename):
    '''计算文件的MD5值'''
    m = hashlib.md5()
    with open(filename, 'rb') as fileobj:   
        while True: 
            data = fileobj.read(4096)
            if not data:
                break
            m.update(data) 
    return m.hexdigest()  # 返回MD5值

 
def handle_multi_folder(dirname):   # 多级目录处理
    '''多级目录处理'''
    dirname2 = os.path.dirname(dirname) # 返回当前文件所在的目录
        
    if not os.path.exists(dirname2):
        handle_multi_folder(dirname2)

    try:
        p1 = os.path.basename(dirname) # 返回路径指的文件名
        dirname = os.path.join(dirname2, p1) # 构建新的路径
        os.mkdir(dirname) # 创建新构建的路径 目录   
    except WindowsError: # 捕获错误
        print('创建目录出错')
    return dirname


def copyfile(path):
    '''复制文件'''
    global _backup_numbers
    
    new_path = path.replace(old_source, new_source) # 构建新路径

    if os.path.isfile(new_path): # 当new_path指的文件存在时： 
        old_md = md5check(path) # 计算旧文件的MD5
        new_md = md5check(new_path) #计算新文件的MD5

        if old_md != new_md:    # 如果两个文件的MD5值不等，说明文件有改动

            # 对改动文件处理：保留原文件，重新命名为新文件
            file_name,file_suffix = os.path.splitext(new_path)
            copy_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            file_name = file_name + ' - ' + copy_time
            new_path = ''.join((file_name, file_suffix))

            shutil.copy(path, new_path) # 执行复制
            _backup_numbers += 1 # 统计已备份的文件数目

            print('Successfully--- ',path, "--- Copy To ---", new_path)
            
            logging.info('Successfully---' + path + ' ___Copy To___ ' + new_path) # 备份日志：文件改动
            logging.info('副本为--- ' + new_path)
            
            
    else: # 当new_path指的文件不存在时，也即该文件是新增加的文件
        
        dirname = os.path.dirname(new_path) # 返回当前文件所在的目录

        if os.path.exists(dirname): # 如果目录dirname存在
            shutil.copy(path, new_path) # 复制文件
            _backup_numbers += 1 # 统计已备份的文件数目

            print('Successfully--- ', path, "--- Copy To ---", new_path)
            logging.info('Successfully---' + path + ' ___Copy To___ ' + new_path) # 备份日志：新增文件
                
        else: # 当前文件所在的目录不存在时，调用多级目录处理函数

            new_path = handle_multi_folder(dirname)
    
            shutil.copy(path, new_path)
            _backup_numbers += 1    # 统计已备份的文件数目

            print('Successfully--- ', path, "--- Copy To ---", new_path)
            logging.info('Successfully---' + path + ' ___Copy To___ ' + new_path) # 备份日志：多级目录


def filter_suffix_file(all_path, target_suffix): # 传入两个列表作为参数
    '''过滤指定后缀名的文件
    target_suffix:['.jpg','.mp3','.png','.pdf']
    '''
    all_suffix = [] # 用于收集指定后缀名的文件路径（实际上这时还是文件的路径）
    for path in all_path:
        file_path, file_suffix = os.path.splitext(path) # 分割出后缀名
        
        if file_suffix in target_suffix: # 
            all_suffix.append(path) # 收集指定后缀名的文件（实际上这时还是文件的路径）  
    return all_suffix

        
def walkdir(folder):
    '''遍历文件夹及其子文件夹中的每个文件'''
    global _total_numbers
    all_path = [] # 收集所有文件（实际上这时还是文件的路径）

    for name in os.listdir(folder): # 遍历folder下的文件和子文件夹
        name = os.path.join(folder, name)  #line = forder + "/" + line

        if os.path.isdir(name): # 判断是否是文件夹 或文件

            # 对空文件夹的处理
            if not os.listdir(name):
                ''' 修复：空文件夹的处理'''
                print('%s 是空文件夹' % name)
                
                logging.warning('[Empty Folder]' + name) # 备份日志：空文件夹
                
            all_path.extend(walkdir(name))     # 如果是文件夹，则继续调用walkdir()
        else:
            _total_numbers += 1 # 统计要备份的文件夹中文件的总数
            all_path.append(name)
    return all_path


def initial_backup(path):
    '''首次备份'''
    
    new_path = path.replace(old_source, new_source)
    print(path, "---Copy To ---", new_path)
    shutil.copytree(path, new_path)

    print("首次备份完成!")
    logging.info('Successfully---首次备份' + path + ' ___Copy To___ ' + new_path) # 备份记录输出到log中
    

def update_backup(path):
    '''更新备份'''
    all_path = walkdir(path)
    #print(len(all_path)) # 统计文件总数

    for name in all_path:
        copyfile(name)

    print("完成更新备份!!!")
    print("文件总数: %d, 此次备份文件数: %d ." % (_total_numbers, _backup_numbers ))
    

def selective_backup(path, target_suffix):
    '''选择性备份. 输入需要备份的文件类型'''
    all_path = walkdir(path) # 所有文件的列表
    all_suffix = filter_suffix_file(all_path, target_suffix) # 调用过滤文件函数,返回一个列表

    for name_suffix in all_suffix:
        copyfile(name_suffix)

    print("完成备份!!!")
    print("文件总数: %d, 此次备份文件数: %d ." % (_total_numbers, _backup_numbers ))


def backup_option(state):
    
    logging.info('\n')
    logging.info(" 执行备份...  ")

    if state == '00':
        print('即将执行首次备份...')
        time.sleep(3)
        
        initial_backup(old_source) # 调用首次备份函数
        
    if state == '11':
        print('即将执行备份更新...')
        time.sleep(3)

        update_backup(old_source)  # 调用更新备份函数

    if state == '22':
        print('即将执行选择性备份...')
        time.sleep(1)
        suffix_list = input("请输入要备份文件的后缀名,用空格分割开不同的后缀：如 .jpg :")
        target_suffix = tuple(suffix_list.split(' '))
        
        time.sleep(3)
        selective_backup(old_source, target_suffix) # 调用选择性备份函数
        
    logging.info(" 完成备份!!!  ")
    logging.info('\n')

def print_script_info():
    print("\n")
    print("\t\t********* HyperBackup Info *********")
    print("\t\t|    Scriptname ---- HyperBeckup   |")
    print("\t\t|    Author     ---- %s     |" % __author__ )
    print("\t\t|    Version    ---- %s        |" % __version__)
    print("\t\t|    Date       ---- %s    |" % __date__)
    print("\t\t************************************")
  
    info = '''
    --Script Info:
        -备份选项：
            - 首次备份  ---请输入00:
            - 更新备份  ---请输入11:
            - 选择性备份---请输入22:
        -
    '''

    warning = '''
    --Warning:
        -请保证路径正确无误!!!
        -如果是主盘符, 如d盘, 直接写 d:
        -如果是文件夹, 如d盘下的test文件夹, 则输入 d:\\test

        -首次备份:
            -此脚本会自动创建存放备份文件的文件夹, 不需要手动创建，请直接输入路径；
            -如: 将文件备份到D盘myfiles下的backup文件夹中，直接输入路径 d:\myfiles\\backup
                 脚本会自动创建backup文件夹，若此文件夹已经存在，则无法备份。

        -选择性备份: 按操作提示, 输入文件后缀名, 如果是多个, 以空格隔开：
            -如: .pdf .mp3 .jpg .avi

    请按提示操作...
    '''
    print(info, warning)

def main():
    global old_source
    global new_source
    global _total_numbers
    global _backup_numbers
    _total_numbers = 0
    _backup_numbers = 0
    
    print_script_info() # 调用打印脚本信息模块
    print('\n')

    print("请输入需要备份的文件(夹)路径：示例: D:\myfiles")
    old_source = input("请输入：")
    print('\n')

    print("请输入存放备份文件的文件夹路径：示例: E:\myfiles\\backup")
    new_source = input("请输入(首次备份时，确保文件backup夹不存在):")
    print('\n')

    print("首次备份---请输入 00; 更新备份---请输入 11; 选择性备份---请输入 22", "\n")
    
    option = input("请输入数字,选择备份选项:")
    print('\n')
    
    backup_option(option) # 调用备份选项函数
    
    input("按Enter键结束")


if __name__ == '__main__':
    main()
