def script_info():
    print("\n")
    print("\t********* HyperBackup Info *********")
    print("\t|    Scriptname ---- HyperBeckup   |")
    print("\t|    Author     ---- Hyper Liu     |")
    print("\t|    Version    ---- V0.1.1        |")
    print("\t|    Date       ---- 2018.06.06    |")
    print("\t************************************")
    #print("\n")

    info = '''
    --Script Info:
        -备份选项：首次备份---请输入00；更新备份---请输入11
        -
        -
    '''

    warning = '''
    --Warning:
      -请保证目录路径正确无误!!!
      -如果是主盘符, 如d盘, 直接写 d:
      -如果是文件夹, 如d盘下的test文件夹, 则输入 d:\\test
      -如果是首次使用此脚本进行备份，请注意：
          -确保存放备份文件的文件夹不存在，脚本会自动创建。
          -如将文件备份到myfiles下的backup文件夹中，直接输入路径 d:\myfiles\\backup
          -如果backup文件夹已经存在，则无法备份。

    请按提示操作...
    '''
    print(info, warning)


if __name__ == '__main__':
    script_info()
