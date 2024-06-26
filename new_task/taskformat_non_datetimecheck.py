import re
from datetime import datetime
import pandas as pd
from calen_check import check_str_calen 


# 和暦→西暦変換関数
# 変換できない場合は、変換できないことをprintしてNoneを返す
# 和暦(明治〜)については、1868-10-23以降の日付となるため、
# 前回(taskformat_use_pandas.py)から変更は加えない
def to_seireki(s_input : str, era : str, year : str, month : str, day : str) -> str:

    WAREKI_CSV_PATH = 'wareki_data.csv'
    
    df = pd.read_csv(WAREKI_CSV_PATH, header=0 , encoding='utf-8')
    df_tmp = df.eq(era)

    df_res = df[(df_tmp['wareki'] == True)|(df_tmp['waryaku'] == True)|(df_tmp['letterupper'] == True)|(df_tmp['letterlower'] == True)]
    
    if not df_res.empty :
      era = df_res.iat[0, 0]
    else :
      print(f"{s_input}:和暦でないため、処理終了")
      return None

    era_start, era_end = pd.to_datetime(df_res.iat[0,4] , format='%Y-%m-%d') , pd.to_datetime(df_res.iat[0,5] , format='%Y-%m-%d')

    ad_year = era_start.year + int(year) - 1

    try:
      todate = pd.Timestamp(ad_year,int(month),int(day))

    except ValueError as e:
      print(e)
      print(f'{s_input}:日付として正しくないため、処理終了')
      return None

    
    if not pd.notnull(todate):
      print(f'{s_input}:日付として正しくないため、処理終了')
      return None

    if era_start <= todate <= era_end :
      restr = todate.strftime('%Y-%m-%d')
      return restr

    else :
      print(f'{s_input}:和暦として正しくないため、処理終了')
      return None


# 様々なフォーマットの日付を"yyyy-mm-dd"形式(0埋め)に変換した文字列を返す
# 変換できない場合は、変換できない旨をprintしてNoneを返す
# (数字のみのフォーマットの場合、月日については0埋め２桁でない場合は、Noneを返す)
# 0<=年数<=9999に対応するため、２桁年は２桁の年としてそのまま扱う
def to_hyphen_dateformat(s_input_date : str) -> str:
  
  #引数の日付文字列内の全角文字(英数記号)を半角に変換
  s_date = s_input_date.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

  res = None

  str_matches = re.search(r'^\D+', s_date)

  #数字のみの場合(月と日の数字については、0埋め２桁のみ対応)
  try:
      _ = int(s_date)
      
      if len(s_date) > 4:
        year , month , day = s_date[:-4] , s_date[-4:-2] , s_date[-2:]

        if check_str_calen(year,month,day) :
          
          res = year.zfill(4) + '-' + month + '-' + day
          return res

      print(f'{s_input_date}:正確な日付の判別ができないため、処理終了')
      return None

  except ValueError:
    pass


  #数字でない文字が頭=和暦の場合、
  if str_matches is not None :
    year = ''
    month = ''
    day = ''
    wareki_era = str_matches.group()
    num_list = re.findall(r'\d+', s_date)
    
    gannen_pos = wareki_era.find('元')
    if gannen_pos > 0 :
      year = '1'
      wareki_era = wareki_era[:gannen_pos]
      if len(num_list) != 2 :
        print(f'{s_input_date}:年月日の情報が正しく取得できないため、処理終了')

        return None
      month , day = num_list[0] , num_list[1]
    else :
      if len(num_list) != 3 :
        print(f'{s_input_date}:年月日の情報が正しく取得できないため、処理終了')

        return None
      year , month , day = num_list[0] , num_list[1] , num_list[2]
     
    res = to_seireki(s_input_date, wareki_era, year, month, day)

    return res
    

  #"数字頭"の場合、
  else :
    delimiterFilePath = 'delimiter.data'
    data_set_list = []
    with open(delimiterFilePath,mode='r',encoding='UTF-8') as f:
      for line in f:
      
        data_set_list.append(re.sub("\n", "", line))

    meaningful_pattern = r'[\d]+[年|y|Y]|[\d]+[月|m|M]|[\d]+[日|d|D]'

    num_list = re.findall(meaningful_pattern, s_date)
    
    #num_listには、年月日順に入っているため、年月日文字消去
    #pattern matchしているため、listに要素があれば、数字と年月日のいづれかの文字は必ず入っている
    num_list = [x[:-1] for x in num_list]

    if len(num_list) == 0:
      s_date = s_date.lower()
      etc_meaningful_pattern = r'[\d]+year|[\d]+month|[\d]+day'
      num_list = re.findall(etc_meaningful_pattern, s_date)
      num_list = [re.findall(r'^[\d]+',x)[0] for x in num_list]
      
      if len(num_list) == 0:
      
        if len(data_set_list) == 0 :
          print(f'{s_input_date}:区切り文字の設定がないため、処理終了')
          return None
        
        # 区切り文字設定ファイルの区切り文字で同一のものが二つ並ぶ場合のみ許容
        # e.g.) 2024--06--26 や 2024//6//26
        delimiter_data_pattern = ''
        for delimiter_data in data_set_list :
          delimiter_data_pattern += '['
          delimiter_data_pattern += delimiter_data
          delimiter_data_pattern += ']{1,2}|'

        delimiter_data_pattern = delimiter_data_pattern[:-1]
        num_list = re.split(delimiter_data_pattern, s_date)

    if len(num_list) != 3:
      print(f'{s_input_date}:年月日の情報として処理できないため、処理終了')
      return None
    
    else :
      year , month , day = num_list[0] , num_list[1] , num_list[2]
      if check_str_calen(year,month,day) :
          
          res = year.zfill(4) + '-' + month.zfill(2) + '-' + day.zfill(2)
          return res

      print(f'{s_input_date}:正確な日付の判別ができないため、処理終了')
      return None



#python [このファイル].pyで実行した場合の動作
if __name__ == '__main__':

  val = input('年月日の情報を入力してください : ')

  res = to_hyphen_dateformat(val)

  print(f'入力値:{val}・出力値:{res}')


