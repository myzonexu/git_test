

#位操作######################################################################
#offset从0开始
#将某一位置为1
def set_bit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)
#将某一位清除为0
def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)
#测试某一位是否位1
def test_bit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)
#组合高低字节
def join_byte_hi_lo(hi,lo,bit_count):
    return (hi<<bit_count | lo)



#表格操作####################################################################
#表格填充数据-二维数组
def table_fill_data_list_2d(table,list_2d,decimal_places=2,fill="new"):
    if fill=="new":
        start_row=0
    elif fill=="append":
        start_row=table.rowCount()

    if list_2d==[]:
        table.clearContents()
    else:
        len_row=len(list_2d)
        len_col=len(list_2d[0])
        table.setRowCount(start_row+len_row)
        table.setColumnCount(len_col)
        for row in range(len_row):
            for col in range(len_col):
                data=list_2d[row][col]            
                if isinstance(data,float):
                    data=round(data,decimal_places)
                item=QTableWidgetItem(str(data))
                table.setItem(start_row+row,col,item)
    table.viewport().update()
