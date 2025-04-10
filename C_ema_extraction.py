import os
import pandas as pd
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR
from def_for_C import DETECT_DELIMITER, PROCESS_FILE

# 手順：3番目(2番目はwav変換)
# EMAのデータをCSV形式に変換するスクリプト

# sc.deal_dataディレクトリを開いて実行する
# data_date,first_file,last_file,keta_45を設定してから実行する

# 一番上のフォルダ
data_date = 20250304

# ループ回数
first_file = 1
last_file = 503

# メイン処理
skipped_files = []  # スキップしたファイル番号を記録するリスト

for file_num in range(first_file, last_file + 1):
    print(f"Processing file number: {file_num}")

    # keta_45の設定
    if file_num <= 50:
        keta_45 = 20
    elif file_num <= 100:
        keta_45 = 10
    elif file_num <= 150:
        keta_45 = 10
    elif file_num <= 200:
        keta_45 = 10
    elif file_num <= 250:
        keta_45 = 10
    elif file_num <= 300:
        keta_45 = 30
    elif file_num <= 350:
        keta_45 = 10
    elif file_num <= 400:
        keta_45 = 10
    elif file_num <= 450:
        keta_45 = 10
    else:
        keta_45 = 10

    # ファイルを処理
    PROCESS_FILE(file_num, data_date, keta_45, skipped_files)

# スキップしたファイル番号を表示
if skipped_files:
    print("\nSkipped files:")
    print(", ".join(map(str, skipped_files)))
else:
    print("\nNo files were skipped.")