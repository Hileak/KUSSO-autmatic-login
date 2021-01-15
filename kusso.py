import selenium
from selenium import webdriver
import time


#ログイン後の処理を入力
option_key = input("ログイン後の処理を入力してください"\
 "\n学務情報サービス[g]_LMSコース[l]_メッセージ[m]_履修登録[rish]\n"\
    "ログインするだけ[enter/適当な文字]_その他機能を知りたい場合は[oth]\n" )
if option_key =="oth":
    option_key = input("学務情報サービス[g]_LMSコース[l]_メッセージ[m]_履修登録[rish]\n"\
         "成績参照[score]_全成績のリスト[scorelist]_GPA表示[gpa]\n")

###設定関連###
#chromedriverのPATH
driver = webdriver.Chrome(r"chromedriverの保存ディレクトリ/chromedriver.exe")
#url指定
url_kusso="https://acanthus.cis.kanazawa-u.ac.jp/"
url_acanrhus_top="https://acanthus.cis.kanazawa-u.ac.jp/base/top/"
url_gakumu = "https://eduweb.sta.kanazawa-u.ac.jp/portal/StudentApp/Top.aspx"
url_lms ="https://acanthus.cis.kanazawa-u.ac.jp/base/lms-course/list"
url_message ="https://acanthus.cis.kanazawa-u.ac.jp/base/message/index"

#ログインIDとPW
#kusso_id.txtにIDを、kusso_pass.txtにパスワードを保存してください。
path_id =r"kusso_id.txtの保存ディレクトリ/kusso_id.txt"
path_pass=r"kusso_pass.txtの保存ディレクトリ/kusso_pass.txt"
f_id = open(path_id)
f_pass = open(path_pass)
userid = f_id.readline()
userpw = f_pass.readline()
f_id.close
f_pass.close

###自動ログイン###
def login():
    #対象URLでブラウザ起動
    driver.get(url_kusso)
    #ログイン
    login_first_btn = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div[3]/div/a")
    login_first_btn.click()
    #2秒待機
    time.sleep(2)

    #ログインIdとパスワードの入力領域の取得
    login_id = driver.find_element_by_xpath("//*[@id= 'kuid']")
    login_pw = driver.find_element_by_xpath("//*[@id= 'password']")

    time.sleep(2)

    #ログインIDとPWを入力
    login_id.send_keys(userid)
    login_pw.send_keys(userpw)

    #ログイン
    login_btn = driver.find_element_by_xpath("//*[@id='login_form']/button")
    login_btn.click()
    time.sleep(2)

#学務
def jump_gakumu():
    driver.get(url_gakumu)

#LMS
def jump_lms():
    driver.get(url_lms)
    #スクロール(第２引数は全体の高さ-任意の高さピクセルで調整。)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight -3000);")

#メッセージ機能
def jump_message():
    driver.get(url_message)

#履修登録
def jump_rishutouroku():
    #学務へ移動
    driver.get(url_gakumu) 
    time.sleep(2)
    #「履修・成績」をクリック
    rishu_seiseki_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[4]/td/div/table/tbody/tr/td/ul/li[2]/a")
    rishu_seiseki_btn.click()
    time.sleep(2)
    #「履修登録」をクリック
    rishutouroku_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/ul/li[1]/a")
    rishutouroku_btn.click()
    #最下部までスクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    #「登録期間ではありません」の有無を判定
    if(len(driver.find_elements_by_id("ctl00_phContents_ucRegistEdit_JeLabel2_lbl" ))>0):
        #文字を表示
        driver.execute_script("document.write('登録期間ではありません。3秒後トップへ戻ります');")
        time.sleep(3)
        #アカンサストップへ移動
        driver.get(url_acanrhus_top)
    else:
        pass

#成績参照
def jump_score(option):
    #学務へ移動
    driver.get(url_gakumu) 
    time.sleep(2)
    #「履修・成績」をクリック
    rishu_seiseki_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[4]/td/div/table/tbody/tr/td/ul/li[2]/a")
    rishu_seiseki_btn.click()
    time.sleep(2)
    #「成績参照」をクリック
    seisekisanshou_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/ul/li[3]/a")
    seisekisanshou_btn.click()
    time.sleep(2)
    #引数でもらったoptionで分岐
    if option == "scorelist":
        zenseiseki_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/input")
        zenseiseki_btn.click()
    elif option == "gpa":
        gpa_btn = driver.find_element_by_xpath("/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table[1]/tbody/tr[1]/td[3]/table/tbody/tr[2]/td/input")
        gpa_btn.click()
    else:
        pass

###ログイン後の分岐###
def login_after(option):
    if option == "g":
        jump_gakumu()    
    elif option == "l":    
        jump_lms()
    elif option == "m":
        jump_message()
    elif option =="rish":
        jump_rishutouroku() 
    elif option == "score" or\
         option == "scorelist"or\
         option == "gpa":
        jump_score(option)           
    else:
        pass
    
    time.sleep(2)

###main###

#すべてのfind_elementの処理時に、要素が見つかるまで最大30秒待機
#seleniumの処理が速すぎて要素を取得しないまま次の処理に移るのを防ぐ
driver.implicitly_wait(30)

login()
login_after(option_key)

# 画面サイズ最大化
driver.maximize_window() 
