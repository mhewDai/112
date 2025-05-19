import string

def stockInfo(s):
    result = ''
    for lines in s.splitlines():
        company = lines.split('-')[1]
        price = lines.split('-')[-1]
        result += company +  ": " + price + '\n'
    return result.strip()


s = '''09/14/07-AAPL-FC3d-E-47.50
       06/05/12-GS-CH86-80.01
       11/12/03-BABA-110.53'''

print(stockInfo(s))