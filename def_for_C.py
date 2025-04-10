from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR
import os
import pandas as pd

def DETECT_DELIMITER(file_path):
    """
    ファイルの区切り文字を判定する関数
    """
    with open(file_path, 'r') as f:
        first_line = f.readline()
        if ',' in first_line:
            print(f"Detected delimiter ',' for file: {file_path}")
            return ','
        elif '\t' in first_line:
            print(f"Detected delimiter '\\t' for file: {file_path}")
            return '\t'
        else:
            print(f"Detected delimiter ' ' (space) for file: {file_path}")
            return ' '  # デフォルトでスペース区切り

def PROCESS_FILE(file_num, data_date, keta_45, skipped_files):
    """
    指定されたファイル番号のch1およびch3~12の.dataファイルを処理し、CSV形式で保存する関数
    """
    # ch1の処理
    try:
        file1in_fullpath = FILE_PLACE('ema', data_date, keta_45, file_num)[0]  # ch1のファイルパスを取得
        file1out_fullpath = FILE_PLACE('ema_hf_chcsv', data_date, keta_45, file_num)[0]  # ch1出力パス

        # ファイルが存在しない場合はスキップ
        if not os.path.isfile(file1in_fullpath):
            print(f"File not found: {file1in_fullpath}")
            skipped_files.append(file_num)
            return

        MAKE_OUTPUT_DIR(file1out_fullpath)

        # 区切り文字を判定
        delimiter = DETECT_DELIMITER(file1in_fullpath)

        # .dataファイルを読み取る
        hf_file1 = pd.read_csv(file1in_fullpath, delimiter=delimiter, header=None)
        # print(f"Read data from {file1in_fullpath}:\n{hf_file1.head()}")  # デバッグ用にデータの先頭を表示

        # CSV形式で保存（カンマ区切り）
        hf_file1.to_csv(file1out_fullpath, sep=',', index=False, header=False, encoding='utf-8')
        print(f"Saved: {file1out_fullpath}")
    except Exception as e:
        print(f"Error processing ch1 file {file1in_fullpath}: {e}")

    # ch3~12の処理
    for ch_num in range(3, 13):
        try:
            hf_file_fullpath = FILE_PLACE('ema', data_date, keta_45, file_num)[ch_num - 2]  # ch3~12のファイルパスを取得
            fileout_fullpath = FILE_PLACE('ema_hf_chcsv', data_date, keta_45, file_num)[ch_num - 2]  # ch3~12出力パス

            # ファイルが存在しない場合はスキップ
            if not os.path.isfile(hf_file_fullpath):
                print(f"File not found: {hf_file_fullpath}")
                skipped_files.append(file_num)
                return

            MAKE_OUTPUT_DIR(fileout_fullpath)

            # 区切り文字を判定
            delimiter = DETECT_DELIMITER(hf_file_fullpath)

            # .dataファイルを読み取る
            hf_file = pd.read_csv(hf_file_fullpath, delimiter=delimiter, header=None)
            #print(f"Read data from {hf_file_fullpath}:\n{hf_file.head()}")  # デバッグ用にデータの先頭を表示

            # CSV形式で保存（カンマ区切り）
            hf_file.to_csv(fileout_fullpath, sep=',', index=False, header=False, encoding='utf-8')
            print(f"Saved: {fileout_fullpath}")
        except Exception as e:
            print(f"Error processing ch{ch_num} file {hf_file_fullpath}: {e}")