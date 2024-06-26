/new_task  
calen_check.py  
　　->datetimeによらない、年月日が日付として正しい値か整合性をチェックするpythonスクリプト  
data_file_new.csv  
　　->テストデータのcsvファイル  
delimiter.data  
　　->区切り文字として認識する文字を指定する設定ファイル  
taskformat_non_datetimechek.py  
　　->日付チェックにdatetimeモジュールを使用しない日付フォーマット変換スクリプト  
　　　　数字の並びは(間に区切り文字があっても)年月日の順である必要あり  
　　　　0〜9999年に対応/同一の区切り文字２つ並びまで許容  
　　　　数字のみの場合、曖昧さ回避のため月日はゼロ埋め２桁のみ対応  
　　　　e.g) 4//06//25 ・ 2024--6--25  ・  2220112  などにも対応  
　　　　  　　(それぞれ0004-06-25 ・ 2024-06-25 ・ 0222-01-12  と変換)  
 　  　　　　　mgrg2024r6sgr22 などは、変換処理を行わずNoneを返す  
　　　  ※pandasモジュール使用のため、実行にあたってはpandasモジュールのインストールが必要になります。  
testpython_fromfile_new.py  
　　->pytestでのテストを行うスクリプト  
　　　　$ pytest -v testpython_fromfile_new.py --durations=0  
　　　　にて、実行  
　　　※pytest(testpython_fromfile_new.py)の実行にあたっては、実行環境に、  
　　　　pandas , pytest 両モジュールがインストールされている必要があります。   
wareki_data.csv  
　　　　->和暦データ変換用データのcsvファイル  
  
  
 


