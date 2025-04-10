import os
import numpy as np
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR

# 手順：4番目
# EGGのデータをCSV形式に変換する

# sc.deal_dataディレクトリを開いて実行する
# data_date,first_file,last_file,keta_45を設定してから実行する

# 一番上のフォルダ
data_date = 20250304

# ループ回数
# first→変換する初めの発話番号、last→変換する最後の発話番号
first_file = 1
last_file = 503

# スキップしたファイル番号を記録するリスト
skipped_files = []

for file_num in range(first_file, last_file + 1):
    now_deal = str(file_num)

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

    # EGGファイルの名前と場所
    egg_fullpath = FILE_PLACE('egg', data_date, keta_45, file_num)

    # ファイルが存在しない場合はスキップ
    if not os.path.isfile(egg_fullpath):
        print(f"File not found: {egg_fullpath}")
        skipped_files.append(file_num)
        continue

    # 出力するファイルとフォルダ
    output_fullpath = FILE_PLACE('egg_csv', data_date, keta_45, file_num)
    MAKE_OUTPUT_DIR(output_fullpath)

    # データのダウンロード
    try:
        egg_file = np.loadtxt(egg_fullpath)

        # ファイルの保存
        np.savetxt(output_fullpath, egg_file, delimiter=',', fmt='%f')
        # 保存先を表示
        print(f"Saved: {output_fullpath}")
    except Exception as e:
        print(f"Error processing file {egg_fullpath}: {e}")
        skipped_files.append(file_num)

# スキップしたファイル番号を表示
if skipped_files:
    print("\nSkipped files:")
    print(", ".join(map(str, skipped_files)))
else:
    print("\nNo files were skipped.")