import os
import re  # 正規表現モジュールをインポート
import numpy as np
import pandas as pd
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR

# 手順：7番目
# UIをxyz=0にして各座標を調整する

# sc.deal_dataディレクトリを開いて実行する
# data_date,start_num,end_numを設定してから実行する


# 処理する日付を指定
date = '20250304'  # 処理する日付を1つ指定

# 処理する範囲を指定
start_num = 1  # 処理を開始する番号
end_num = 503  # 処理を終了する番号

# 指定された範囲で処理
for n in range(start_num, end_num + 1):
    # 入力と出力のディレクトリパス設定
    input_dirs = FILE_PLACE('ema_hf_poscsv_cut', date, 10, n)  # リストとして取得
    output_dirs = FILE_PLACE('ema_hf_poscsv_cut_0', date, 10, n)  # リストとして取得

    # 入力ディレクトリが存在しない場合はスキップ
    if not input_dirs or not all(os.path.exists(d) for d in input_dirs):
        print(f"Warning: Input directories do not exist: {input_dirs}")
        continue

    # 出力先ディレクトリを作成
    for output_dir in output_dirs:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # UIファイルを読み込み
    ui_file = os.path.join(input_dirs[0], f"{n}_UI.csv")  # UIファイルのパスを生成
    if not os.path.isfile(ui_file):  # ファイルが存在しない場合はスキップ
        print(f"Warning: UI file does not exist: {ui_file}")
        continue

    ui_data = pd.read_csv(ui_file, header=None).values
    translation = ui_data[:, :3]  # x, y, z座標を取得

    # 入力ディレクトリ内のすべてのファイルを処理
    for file_name in os.listdir(input_dirs[0]):
        input_file = os.path.join(input_dirs[0], file_name)  # 入力ファイルのパスを生成
        output_file = os.path.join(output_dirs[0], file_name)  # 出力ファイルのパスを生成

        if not os.path.isfile(input_file):  # 入力ファイルが存在しない場合はスキップ
            print(f"Warning: Input file does not exist: {input_file}")
            continue

        # ファイルを読み込み
        try:
            data = pd.read_csv(input_file, header=None).values
        except Exception as e:
            print(f"Error reading file {input_file}: {e}")
            continue

        # 並行移動
        try:
            data[:, :3] = data[:, :3] - translation
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")
            continue

        # 保存
        try:
            pd.DataFrame(data).to_csv(output_file, header=False, index=False)
        except Exception as e:
            print(f"Error saving file {output_file}: {e}")
            continue

        # 保存先ディレクトリとファイル名を表示
        print(f"Saved: {output_file}")

print(f"{date}：すべてのファイルを処理しました。")

