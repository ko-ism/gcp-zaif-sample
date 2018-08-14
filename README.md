# gcp-zaif-sample
# 2018/8/14
・概要は以下の通り

1. ビットコイン/イーサリアムの取引価格をZaifAPIで取得
2. 指定するpubsubトピックへpublishする

・デプロイ手順

1. git clone https://github.com/ko-ism/gcp-zaif-sample.git
2. cd gcp-zaif-sample
3. pip install -r requirements.txt
4. gcloud app deploy
