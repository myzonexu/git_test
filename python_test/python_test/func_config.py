import csv



def import_csv(file):
    """
    导入csv文件.
 
    :param file: str,文件路径
    :param head: this is a second param
    :returns: list,list:表头,行内容
    :raises: no exception
    """
    with open(file, newline='') as f:
        f_csv = csv.reader(f)
        header = next(f_csv)
        rows=[]
        for row in f_csv:
            rows.append(row)
        #print(header)
        #print(rows)
    return header,rows

def export_csv(file,header,rows):
    """
    导出csv文件.
 
    :param file: str,文件路径
    :param header: list,表头
    :param rows: list,行内容,list成员可为list或dict
    :returns: no return
    :raises: no exception
    """
    with open(file,'w',newline='') as f:
        if len(rows)==0:
            print("空数据")
        elif type(rows[0]) is list:
            #print("list数据")
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(rows)
        elif type(rows[0]) is dict:
            #print("dict数据")
            f_csv = csv.DictWriter(f,header)
            f_csv.writeheader()
            f_csv.writerows(rows)
        else:
            pass

#head,rows=import_csv('./data/config_robot1.csv')
#export_csv('./data/config_robot2.csv',head,rows)
