
## 年月日の値の整合性チェック
def check_str_calen(s_year :str , s_month :str, s_day : str ) -> bool:
  
  if s_year is None or s_month is None or s_day is None:
    return False

  try :
    year = int(s_year)
    month = int(s_month)
    day = int(s_day)

  except ValueError:
    return False

  if not 0 <= year <= 9999 :
    return False

  if month in [4,6,9,11] :
    if 1 <= day <= 30: 
      return True
    else :
      return False

  elif month in [1,3,5,7,8,10,12]:
    if 1 <= day <= 31:
      return True
    else :
      return False

  elif month == 2:

    if year % 4 == 0 :
      if year % 100 == 0 and year % 400 != 0:
        if 1 <= day <= 28:
          return True
        else :
          return False
      
      else :
        if 1 <= day <= 29:
          return True
        else :
          return False

    else :
      
      if 1 <= day <= 28:
        return True
      else :
        return False

  else :
    return False



#python [このファイル].pyで実行した場合の動作
if __name__ == '__main__' :
  print('年月日の情報を順に改行して入力してください : ')
  list_disp = ['年','月','日']
  val = [input( list_disp[i] + ' : ') for i in range(3)]
  str_year , str_month , str_day = val[0] , val[1] , val[2] 

  res = check_str_calen(str_year , str_month , str_day)

  print(f'入力値:{val}・出力値:{res}')




