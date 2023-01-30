@echo off
rem Slackアプリに用いる環境変数
rem
rem Botトークン（環境に合わせて変更する）
set SLACK_BOT_TOKEN=xoxb-***
rem アプリトークン（環境に合わせて変更する）
set SLACK_APP_TOKEN=xapp-***
rem ユーザートークン（環境に合わせて変更する）
set SLACK_USER_TOKEN=xoxp-***
rem ファイルを一時保存するフォルダー
set LOCAL_FOLDER=_temp
rem 環境設定 production: 本番環境 development: 開発環境
set NODE_ENV=development
rem ----- END OF FILE -----