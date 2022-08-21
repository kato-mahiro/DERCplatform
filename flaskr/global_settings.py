import gspread
###################スプレッドシート操作
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
#DB用
SPREADSHEET_KEY_DB = '1_SzdLbYKpzgC_nogM0LxVZcA2Twxlw9arwsGUNoWHk0'
#EventAPIでslackのログを保存しているスプレッドシート
SPREADSHEET_KEY_slacklog_EventAPI = '1X6hvIH95D6QsojbypzI0nGpuppi7K3hU1u-GYV02Ir8'
#共有設定したスプレッドシートを指定
#DB用
workbook_DB = gc.open_by_key(SPREADSHEET_KEY_DB)
#EventAPIでslackのログを保存しているスプレッドシート
workbook_slacklog_EventAPI = gc.open_by_key(SPREADSHEET_KEY_slacklog_EventAPI)
#ユーザー名からslackのアカウントIDを取ってくるためのシート
userIDchange = workbook_slacklog_EventAPI.worksheet('userIDchange')
#スプレッドシートの中のワークシート名を直接指定
worksheet1 = workbook_DB.worksheet('ポイント管理')
worksheet2 = workbook_DB.worksheet('チャンネル関連')
pointrireki = workbook_DB.worksheet('ポイント履歴')


#ビデオ会議関連のスプレッドシート
SPREADSHEET_webdiscuss = '1CPVCsai9pIGrxCa1Rv5189800S3a2kJoEq9MI6ROQe8'
workbook_webdiscuss = gc.open_by_key(SPREADSHEET_webdiscuss)
webchan = workbook_webdiscuss.worksheet('会議チャンネル関連')


#歩数計算のワークシート
SPREADSHEET_hosuukeisana = '1iCCoezUqcFrtcY7uISYm3k4zgkFz_5Uh2evZ6zomAQ8'
SPREADSHEET_hosuukeisan = gc.open_by_key(SPREADSHEET_hosuukeisana)
hosuukeisan = SPREADSHEET_hosuukeisan.worksheet('歩数')


#日常生活のワークシート
SPREADSHEET_rita = '1lEJuoj2-8wCQ1CErkQ4baHqemm9plFacwyYW4VgjBjU'
SPREADSHEET_rita = gc.open_by_key(SPREADSHEET_rita)
ritasheet = SPREADSHEET_rita.worksheet('利他行為')

###################スプレッドシート操作終わり


all_user =["shimamoto","komori","shimaoka","hiramoto","asakura","banno","morinaga","sumitani","iwata","yamato","test"]
all_user_pswd=["lucas","afro","dark","gene","hero","riot","poruka","takemi","boss","tutida","aaa"]
all_user_ID =  ["slackの個人ID","slackの個人ID","X","","","","","","","",""]
chan_IDlist = ["slackのチャンネルID","slackのチャンネルID","","",""]

member_data = {}
message_data = []