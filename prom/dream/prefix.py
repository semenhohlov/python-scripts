import openpyxl

def main():
    temp = openpyxl.load_workbook("prev.xlsx")
    work_sheet = temp.active
    total = work_sheet.max_row
    percent = int(total / 100)
    current = 1
    tmp = 0
    for row in work_sheet.rows:
        old = str(row[24].value)
        row[24].value = '1003' + old
        tmp += 1
        if tmp > percent:
            tmp = 0
            current += 1
            print('\r{}%'.format(current), end='')
    print()
    temp.save('new_prev.xlsx')
        

if __name__ == '__main__':
    main()