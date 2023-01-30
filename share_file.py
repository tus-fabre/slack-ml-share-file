#!/usr/bin/env python
# coding: utf-8
#
# [FILE] share_file.py
#
# [DESCRIPTION]
#  Slackが共有イベントメッセージを受け取ったときに起動する関数を定義する
#
# [NOTES]
#
import os, sys
from pathlib import Path
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# BOTトークンからアプリを初期化する
bot_token = os.environ.get("SLACK_BOT_TOKEN")
if bot_token == None:
    print("環境変数が設定されていません")
    sys.exit()
app = App(token=bot_token)

# アプリトークン
app_token = os.environ["SLACK_APP_TOKEN"]
# ユーザートークン：ファイルの内容を取得するため用いる
user_token = os.environ.get("SLACK_USER_TOKEN")
# ローカルフォルダー
local_folder = os.environ.get("LOCAL_FOLDER")

#
# [EVENT] message
#
# [DESCRIPTION]
#  次のメッセージを受信したときのリスナー関数
#   Unhandled request ({'type': 'event_callback', 'event': {'type': 'message', 'subtype': 'file_share'}})
#
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

#
# [EVENT] file_shared
#
# [DESCRIPTION]
#  ファイルを共有したときに起動するリスナー関数
#  アップロードしたテキストファイルの内容をコンソールに表示し、ローカルフォルダに保存する
#
# [NOTES]
#
@app.event("file_shared")
def file_shared(payload, client, ack, say):
    ack()

    # アップロードしたファイルのIDを取得する
    file_id = payload.get('file').get('id')
    
    # ファイル情報を取得する
    file_info = client.files_info(file = file_id).get('file')
    url = file_info.get('url_private')
    local_path = local_folder + "/" + file_info.get('title')
    file_type = file_info.get('filetype')

    # ファイルタイプをチェックする
    if file_type != 'text':
        say(f"サポートしていないファイル形式です： {file_type}")
        return

    # ファイルの内容を取得しコンソールに表示する
    resp = requests.get(url, headers={'Authorization': 'Bearer %s' % user_token})
    text = (resp.content).decode()
    print("[FILE CONTENT] " + text)

    # テキストをローカルフォルダーに保存する
    save_file = Path(local_path)
    save_file.write_text(text)
    print("[CREATED FILE] " + local_path)
#
# Start the Slack app
#
if __name__ == "__main__":
    print('⚡️App starts...')
    SocketModeHandler(app, app_token).start()

#
# END OF FILE
#