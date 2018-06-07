# coding=utf-8

'''
# 2018.06.06
# V0.1.1
# 内容：
# 1. 实现文件备份功能（源文件地址 old_source, 备份地址 new_source ）
# 2. 备份选项：
    00 --- 初次备份：简单粗暴直接复制文件夹
    11 --- 更新备份：遍历每个文件夹每个文件，计算每个文件的MD5值，比对MD5值，
                    查找文件变动，如文件有改动则执行备份（跳过未改动的文件，不执行备份）。
# 3. 空文件夹处理:
    标出空文件夹(打印出)

# 4. 更新备份选项：遗留问题：多级目录
问题描述：如果源文件夹下新增加多级文件夹（在备份中不存在），
如：path = d:\backuptest\新建文件夹1\新建文件夹2\新建文件夹3\测试多级目录.txt
那么，new_path = f:\backuptest2\新建文件夹1\新建文件夹2\新建文件夹3\测试多级目录.txt
其中，新建文件夹1\新建文件夹2\新建文件夹3\测试多级目录.txt  为新增加的多级目录
在执行备份时，就会报错 创建文件夹失败。
'''          
       
        
import hashlib
import os
import shutil
import time
import scriptinfo


def md5check(filename):
    '''计算文件的MD5值'''
    # 摘要算法（哈希算法、散列算法）就是通过摘要函数对任意长度的数据data计算出固定长度的摘要digest，
    # 目的是为了发现原始数据是否被改过。
    
    m = hashlib.md5()

    # 读取文件内容，用于计算MD5值。
    with open(filename, 'rb') as fileobj:   # 以二进制打开文件
        # Feeding string objects into update() is not supported, as hashes work on bytes, not on characters

        while True: # while循环，读取文件内容
            data = fileobj.read(4096)
            if not data:
                break
            
            m.update(data) # 更新

    return m.hexdigest()  # 返回MD5值


def copyfile(path):
    
    new_path = path.replace(old_source, new_source) # 构建新路径

    print(path, "--- Copy To ---", new_path)

    # 以下是用来判断
    if os.path.isfile(new_path): # 当new_path指的文件存在时：
        
        old_md = md5check(path) # 计算旧文件的MD5
        
        new_md = md5check(new_path) #计算新文件的MD5

        if old_md != new_md:    # 如果两个文件的MD5值不等，说明文件有改动
            
            shutil.copy(path, new_path) # 

    else: # 当new_path指的文件不存在时：
        
        # 如：new_path = f:\backuptest2\新建文件夹1\新建文件夹2\测试多级目录.txt
        
        dirname = os.path.dirname(new_path) # 返回上一层目录
        
        
        if os.path.exists(dirname): # 判断目录dirname是否存在
            
            shutil.copy(path, new_path) # 复制文件
            
        else:
            try:
                os.mkdir(dirname) # 如果目录不存在，则先创建目录
                shutil.copy(path, new_path) # 复制文件

            except WindowsError: # 捕获错误
                print('创建目录出错')
                

# 遍历指定文件目录folder下及其子目录下的所有文件。
def walkdir(folder):

    for name in os.listdir(folder): # 遍历folder下的文件和子文件夹
        
        name = os.path.join(folder, name)  #line = forder + "/" + line
        # 构建绝对路径

        if os.path.isdir(name): # 判断是否是文件夹或文件

            if not os.listdir(name): # 对空文件夹的处理
                ''' 修复：空文件夹的处理'''

                print('%s 是空文件夹' % name)
            
            walkdir(name)     # 如果是文件夹，则继续调用walkdir()
            
        else:
            copyfile(name)  # 如果是文件，则调用copyfile()函数


def backup_firsttime(path):
    '''首次备份'''
    new_path = path.replace(old_source, new_source)

    print(path, "---Copy To ---", new_path)

    shutil.copytree(path, new_path)
    

def backup_option(state):

    if state == '00':
        print('即将执行首次备份...')
        time.sleep(5)
        backup_firsttime(old_source)
        print("首次备份完成!")
        
    if state == '11':
        print('即将执行备份更新...')
        time.sleep(5)
        walkdir(old_source)
        print("完成更新备份")

 
def main():

    global old_source
    global new_source
    
    scriptinfo.script_info() # 调用打印脚本信息模块
    print('\n')

    old_source = input("请输入要备份的文件地址：")
    print('\n')

    new_source = input("请输入要存放备份文件的目录：(首次备份时，确保文件夹不存在)")
    print('\n')

    print("首次备份---请输入00；更新备份---请输入11")
    print('\n')

    option = input("请输入数字,选择备份选项:")
    print('\n')
    

    # 添加备份选项，首次备份时直接copytree,简单粗暴。
    backup_option(option)
    
    input("按Enter键结束")


if __name__ == '__main__':
    main()
