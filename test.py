import sys
import os
import time
import json
import random
import traceback
import threading

from PyPtt import PTT

def get_password(password_file):
    try:
        with open(password_file) as AccountFile:
            account = json.load(AccountFile)
            ptt_id = account['id']
            password = account['pw']
    except FileNotFoundError:
        print(f'Please write PTT ID and Password in {password_file}')
        print('{"id":"your ptt id", "pw":"your ptt pw"}')
        sys.exit()

    return ptt_id, password

def init():
    print('===正向===')
    print('===預設值===')
    PTT.API()
    print('===中文顯示===')
    PTT.API(language=PTT.i18n.language.CHINESE)
    print('===英文顯示===')
    PTT.API(language=PTT.i18n.language.ENGLISH)
    print('===log DEBUG===')
    PTT.API(log_level=PTT.log.level.DEBUG)
    print('===log INFO===')
    PTT.API(log_level=PTT.log.level.INFO)
    print('===log SLIENT===')
    PTT.API(log_level=PTT.log.level.SILENT)
    print('===log SLIENT======')

    print('===負向===')
    try:
        print('===語言 99===')
        PTT.API(language=99)
    except ValueError:
        print('通過')
    except:
        print('沒通過')
        sys.exit(-1)
    print('===語言放字串===')
    try:
        PTT.API(language='PTT.i18n.language.ENGLISH')
    except TypeError:
        print('通過')
    except:
        print('沒通過')
        sys.exit(-1)

    def handler(msg):
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    ptt_bot = PTT.API(
        log_handler=handler)
    ptt_bot.log('Test log')

def show_condition(test_board, search_type, condition):
    if search_type == PTT.data_type.post_search_type.KEYWORD:
        type_str = '關鍵字'
    if search_type == PTT.data_type.post_search_type.AUTHOR:
        type_str = '作者'
    if search_type == PTT.data_type.post_search_type.PUSH:
        type_str = '推文數'
    if search_type == PTT.data_type.post_search_type.MARK:
        type_str = '標記'
    if search_type == PTT.data_type.post_search_type.MONEY:
        type_str = '稿酬'

    print(f'{test_board} 使用 {type_str} 搜尋 {condition}')

def get_post_with_condition():
    # PTT1

    if ptt_bot.config.host == PTT.data_type.host_type.PTT1:
        test_list = [('MacShop', PTT.data_type.post_search_type.KEYWORD, '[公告]')]
    else:
        test_list = [('MacShop', PTT.data_type.post_search_type.KEYWORD, '[公告]')]

    test_range = 1
    query = False

    for (board, search_type, condition) in test_list:
        print('1')
        show_condition(board, search_type, condition)
        index = ptt_bot.get_newest_index(
            PTT.data_type.index_type.BBS,
            board,
            search_type=search_type,
            search_condition=condition)
        for i in range(test_range):
            post = ptt_bot.get_post(
                board,
                post_index=index - i,
                # PostIndex=611,
                search_type=search_type,
                search_condition=condition,
                query=query)

            print('列表日期:')
            print(post.list_date)
            print('作者:')
            print(post.author)
            print('標題:')
            print(post.title)

            if post.delete_status == PTT.data_type.post_delete_status.NOT_DELETED:
                if not query:
                    print('內文:')
                    print(post.content)
            elif post.delete_status == PTT.data_type.post_delete_status.AUTHOR:
                print('文章被作者刪除')
            elif post.delete_status == PTT.data_type.post_delete_status.MODERATOR:
                print('文章被版主刪除')
            print('=' * 50)

def get_newest_index(board):
    index = 0
    test_board_list = [board]
    test_range = 1

    for board in test_board_list:
        for _ in range(test_range):
            index = ptt_bot.get_newest_index(PTT.data_type.index_type.BBS, board=board)
            #print(f'{board} 最新文章編號 {index}')
    return index

def mail(userID):
    content = '\r\n\r\n'.join(
        [
            '您好，您徵求的商品我有販售，只賣全新未拆原廠貨，保證在台一年保固，附購買證明，下方連結供您參考:',
            '7-11賣貨便下單連結 https://reurl.cc/YjEmVn',
            '蝦皮賣場(十倍蝦幣) https://shopee.tw/apple.yen',
            'LINE ID: @apple.yen',
            '自取地點:台北信義/新北板橋/台中勤美'
        ]
    )

    try:
        ptt_bot.mail(userID,f'您徵求的商品，我有販售，提供蝦皮/自取/賣貨便',content,0)
    except PTT.exceptions.NoSuchUser:
        pass


if __name__ == '__main__':
    print('Welcome to PyPtt v ' + PTT.version.V + ' test case')

    try:
        
        ptt_bot = PTT.API()
        
        if ptt_bot.config.host == PTT.data_type.host_type.PTT1:
            ptt_id, password = get_password('account_ptt_0.json')
        else:
            ptt_id, password = get_password('account_ptt2.json')
        try:
            ptt_bot.login(
                ptt_id,
                password,
                # kick_other_login=True
            )
        except PTT.exceptions.LoginError:
            ptt_bot.log('登入失敗')
            sys.exit()
        except PTT.exceptions.WrongIDorPassword:
            ptt_bot.log('帳號密碼錯誤')
            sys.exit()
        except PTT.exceptions.LoginTooOften:
            ptt_bot.log('請稍等一下再登入')
            sys.exit()

        if ptt_bot.unregistered_user:
            print('未註冊使用者')

            if ptt_bot.process_picks != 0:
                print(f'註冊單處理順位 {ptt_bot.process_picks}')

        if ptt_bot.registered_user:
            print('已註冊使用者')

        board = 'MacShop'
        rules = ['iPhone','iPad 9th','Ipad 9Th','IPAD 9TH','ipad 9th','iPad 9','Ipad 9','IPAD 9','ipad 9','iPad9th','Ipad9Th','IPAD9TH','ipad9th','iPad9','Ipad9','IPAD9','ipad9','iPad Mini 6th','Ipad Mini 6Th','IPAD MINI 6TH','ipad mini 6th','iPad Mini 6','Ipad Mini 6','IPAD MINI 6','ipad mini 6','iPadMini6th','Ipadmini6Th','IPADMINI6TH','ipadmini6th','iPadMini6','Ipadmini6','IPADMINI6','ipadmini6','iPad Pro 11 inch','Ipad Pro 11 Inch','IPAD PRO 11 INCH','ipad pro 11 inch','iPad Pro 11','Ipad Pro 11','IPAD PRO 11','ipad pro 11','iPadPro11inch','Ipadpro11Inch','IPADPRO11INCH','ipadpro11inch','iPadPro11','Ipadpro11','IPADPRO11','ipadpro11','iPad Pro 12.9 inch','Ipad Pro 12.9 Inch','IPAD PRO 12.9 INCH','ipad pro 12.9 inch','iPad Pro 12.9','Ipad Pro 12.9','IPAD PRO 12.9','ipad pro 12.9','iPadPro12.9inch','Ipadpro12.9Inch','IPADPRO12.9INCH','ipadpro12.9inch','iPadPro12.9','Ipadpro12.9','IPADPRO12.9','ipadpro12.9','Airpods 2nd','Airpods 2Nd','AIRPODS 2ND','airpods 2nd','Airpods 2','Airpods 2','AirPods 2','AIRPODS 2','airpods 2','Airpods2nd','Airpods2Nd','AIRPODS2ND','airpods2nd','Airpods2','Airpods2','AIRPODS2','airpods2','Airpods 3rd','Airpods 3Rd','AIRPODS 3RD','airpods 3rd','Airpods 3','AirPods 3','Airpods 3','AIRPODS 3','airpods 3','Airpods3rd','Airpods3Rd','AIRPODS3RD','airpods3rd','Airpods3','Airpods3','AIRPODS3','airpods3','Airpods Pro Magsafe','Airpods Pro Magsafe','AIRPODS PRO MAGSAFE','airpods pro magsafe','Airpods Pro','AirPods Pro','AirPods','Airpods Pro','AIRPODS PRO ','airpods pro ','AirpodsProMagsafe','Airpodspromagsafe','AIRPODSPROMAGSAFE','airpodspromagsafe','AirpodsPro ','Airpodspro ','AIRPODSPRO ','airpodspro ','Apple Pencil 2nd','Apple Pencil 2Nd','APPLE PENCIL 2ND','apple pencil 2nd','Apple Pencil 2','Apple Pencil 2','APPLE PENCIL 2','apple pencil 2','ApplePencil2nd','Applepencil2Nd','APPLEPENCIL2ND','applepencil2nd','ApplePencil2','Applepencil2','APPLEPENCIL2','applepencil2','Apple Pencil 1st','Apple Pencil 1St','APPLE PENCIL 1ST','apple pencil 1st','Apple Pencil 1','Apple Pencil 1','APPLE PENCIL 1','apple pencil 1','Apple Pencil1st','Apple Pencil1St','APPLE PENCIL1ST','apple pencil1st','ApplePencil1','Applepencil1','APPLEPENCIL1','applepencil1','Apple Pencil','Apple Pencil','APPLE PENCIL','apple pencil','Apple Pencil','Apple Pencil','APPLE PENCIL','apple pencil','Apple Pencil','Apple Pencil','APPLE PENCIL','apple pencil','ApplePencil','Applepencil','APPLEPENCIL','applepencil','iPad Mini6','Ipad Mini6','IPAD MINI6','ipad mini6','iPadMini 6','Ipadmini 6','IPADMINI 6','ipadmini 6','iPad Pro11','Ipad Pro11','IPAD PRO11','ipad pro11','iPadPro 11','Ipadpro 11','IPADPRO 11','ipadpro 11','iPad Pro12.9','Ipad Pro12.9','IPAD PRO12.9','ipad pro12.9','iPadPro 12.9','Ipadpro 12.9','IPADPRO 12.9','ipadpro 12.9','Apple Pencil2','Apple Pencil2','APPLE PENCIL2','apple pencil2','ApplePencil 2','Applepencil 2','APPLEPENCIL 2','applepencil 2','Apple Pencil1','Apple Pencil1','APPLE PENCIL1','apple pencil1','ApplePencil 1','Applepencil 1','APPLEPENCIL 1','applepencil 1']
        index = get_newest_index(board)
        print(f'{board} 最新文章編號 {index}')
        isFirstTime = True
        post_info = ''
        while(True):
            try:
                if isFirstTime == True:
                    isFirstTime = False
                else:
                    currentIndex = get_newest_index(board)
                    if currentIndex > index:
                        index = index +1 
                        post_info = ptt_bot.get_post(
                        board,
                        post_index=index)
                        
                        ptt_bot.log(f'偵測到新文章{post_info.title}')
                        if '徵求' in post_info.title and any(word in post_info.title for word in rules):
                            ptt_bot.log(f'發現符合條件文章{post_info.title}，寄信給作者{post_info.author}')
                            mail(post_info.author)
                            mail('e23882')
                        else:
                           ptt_bot.log(f'不符合設定條件，不做任何動作({post_info.title})')
                        
                    else:
                        pass
                        
                    
            except Exception as e:
                ptt_bot.log('連線發生錯誤，嘗試重新連線...')
                ptt_bot.logout()
                ptt_bot.login(
                ptt_id,
                password,
                # kick_other_login=True
            )
                pass
            time.sleep(10)
        


    except Exception as e:
        print(type(e))
        traceback.print_tb(e.__traceback__)
        print(e)
    except KeyboardInterrupt:
        pass

    ptt_bot.logout()
