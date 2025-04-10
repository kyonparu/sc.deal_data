import os
import shutil
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR

# 手順：6番目
# EMAのデータをファイル名でどこに貼られていたかわかるようにする

# sc.deal_dataディレクトリを開いて実行する
# data_date,start_num,end_num、chMAPを設定してから実行する

# 日付と観測箇所の設定
data_date = 20250304
start_num = 1
end_num = 503

# 観測箇所とch番号の設定
chMap = [
    ('NA', 5),
    ('ND', 1),
    ('UI', 12),
    ('UL', 7),
    ('LL', 6),
    ('LJ', 8),
    ('T1', 10),
    ('T2', 11),
    ('T3', 4),
    ('ch3', 3),  # 未使用のchを(ch[n],[n])となるようにする
    ('ch9', 9)
]

# ch番号の降順でソート（置換順序を確実にするため）
sortMap = sorted(chMap, key=lambda x: x[1], reverse=True)

# スキップした番号を記録するリスト
skipped_files = []

for l in range(start_num, end_num + 1):
    # 入力と出力のファイルパス設定
    input_dir = os.path.dirname(FILE_PLACE('ema_hf_chcsv_cut', data_date, 10, l)[0])
    output_dir = FILE_PLACE('ema_hf_poscsv_cut', data_date, 10, l)[0]

    # 入力ディレクトリが存在しない場合はスキップ
    if not os.path.exists(input_dir):
        print(f"Input directory does not exist for {l}: {input_dir}. Skipping...")
        skipped_files.append(l)
        continue

    # 出力先のディレクトリを作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 入力フォルダ内のファイル一覧を取得
    files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    # ファイルが存在しない場合はスキップ
    if not files:
        print(f"No CSV files found in input directory for {l}: {input_dir}. Skipping...")
        skipped_files.append(l)
        continue

    # 観測箇所順でファイルを処理
    for ch_name, ch_num in sortMap:
        search_str = f"ch{ch_num}.csv"  # 置換対象のch番号と拡張子を含める

        # 対応するファイルを検索
        for old_name in files:
            old_path = os.path.join(input_dir, old_name)  # 元のファイルパス

            # 完全一致でch番号に対応するファイル名を見つける
            if old_name.endswith(search_str):  # ファイル名が正確に一致する場合のみ処理
                replace_str = ch_name  # 置換後の文字列（観測箇所）
                new_name = f"{l}_{replace_str}.csv"  # 正しい新しいファイル名を生成
                new_path = os.path.join(output_dir, new_name)  # 出力ファイルパスを生成

                # 元のファイルを新しい名前でコピー
                if os.path.isfile(old_path):  # ファイルが存在する場合のみコピー
                    try:
                        shutil.copyfile(old_path, new_path)
                    except Exception as e:
                        print(f"Error copying file from {old_path} to {new_path}: {e}")
                else:
                    print(f"Warning: Source file does not exist: {old_path}")

                # 置換後の名前を確認（デバッグ用）
                print(f'Old Name: {old_name} -> New Name: {new_path}')

    print(f"{l}：すべてのファイルを処理しました。")

# スキップした番号を表示
if skipped_files:
    print("\nSkipped files:")
    print(", ".join(map(str, skipped_files)))
else:
    print("\nNo files were skipped.")