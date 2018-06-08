#!/usr/bin/python
# -*- coding: utf-8 -*-


# 2018.06.08
# V0.1.3
# 内容：
# 1. 修复：多级目录问题: 已修复2018.06.07
# 2. 添加：详细备份日志，以单独的文本输出。 已添加2018.06.07
# 3. 添加：对有改动的文件，执行备份，保留原有文件，以备份时间为命名方式。已添加2018.06.07
# 4. 添加：统计文件总数，已备份数量。 已添加2018.06.07
# 5. 添加：备份时间记录

# 5. 遗留问题：备份时提示'--- Logging error ---',写入日志错误，但不影响文件备份
# UnicodeEncodeError:
# 'gbk' codec can't encode character '\xa0' in position 56: illegal multibyte sequence
#



__author__  = "Hyper Liu <byfisherman@outlook.com>"
__status__  = "production"
__version__ = "0.1.3"
__date__    = "2018.06.07"

    
import hashlib
import os
import shutil
import time, datetime
import scriptinfo
import logging


format='%(asctime)s - %(levelname)s: %(message)s' # 设置日志格式
datefmt = '%Y-%m-%d %I:%M:%S %p'    # 设置时间格式
logging.basicConfig(filename='backup.log',filemode='a', level=logging.DEBUG, format = format, datefmt=datefmt)


def md5check(filename):
    
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
        p1 = os.path.basename(dirname)
        dirname = os.path.join(dirname2, p1)
        os.mkdir(dirname) # 如果目录不存在，则先创建目录   
    except WindowsError: # 捕获错误
        print('创建目录出错')
  
    return dirname

def copyfile(path):
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
    
def walkdir(folder):
    global _total_numbers

    for name in os.listdir(folder): # 遍历folder下的文件和子文件夹
        name = os.path.join(folder, name)  #line = forder + "/" + line
        if os.path.isdir(name): # 判断是否是文件夹 或文件

            # 对空文件夹的处理
            if not os.listdir(name):
                ''' 修复：空文件夹的处理'''
                print('%s 是空文件夹' % name)

                logging.warning('[Empty Folder]' + name) # 备份日志：空文件夹

            walkdir(name)     # 如果是文件夹，则继续调用walkdir()

        else:
            _total_numbers += 1 # 统计要备份的文件夹中文件的总数

            copyfile(name)  # 如果是文件，则调用copyfile()函数

def backup_firsttime(path):
    '''首次备份'''
    new_path = path.replace(old_source, new_source)
    print(path, "---Copy To ---", new_path)
    shutil.copytree(path, new_path)

    logging.info('Successfully---首次备份' + path + ' ___Copy To___ ' + new_path) # 备份记录输出到log中
    
    
def backup_option(state):
    
    logging.info('\n')
    logging.info(" 执行备份...  ")

    if state == '00':
        print('即将执行首次备份...')
        
        t_b1 = time.time() # 备份开始的时间
        
        time.sleep(3)
        backup_firsttime(old_source)
        print("首次备份完成!")

        t_e1 = time.time()   # 备份结束的时间
        print("备份耗时：%d s." % (t_e1 - t_b1))

    if state == '11':
        print('即将执行备份更新...')

        t_b2 = time.time()

        time.sleep(3)
        walkdir(old_source)
        print("完成更新备份!!!")
        print("文件总数: %d, 此次备份文件数: %d ." % (_total_numbers, _backup_numbers ))

        t_e2 = time.time()
        print("备份耗时：%d s." % (t_e2 - t_b2))
    
    logging.info(" 完成备份!!!  ")
    logging.info('\n')
 
def main():
    
    global old_source
    global new_source
    global _total_numbers
    global _backup_numbers
    _total_numbers = 0
    _backup_numbers = 0
    
    scriptinfo.script_info() # 调用打印脚本信息模块
    print('\n')

    old_source = input("请输入要备份的文件地址：")
    print('\n')

    new_source = input("请输入要存放备份文件的目录(首次备份时，确保文件夹不存在)：")
    print('\n')

    print("首次备份---请输入00；更新备份---请输入11", "\n")
    

    option = input("请输入数字,选择备份选项:")
    print('\n')
    
    backup_option(option) # 调用备份选项函数
    
    input("按Enter键结束")


if __name__ == '__main__':
    main()
