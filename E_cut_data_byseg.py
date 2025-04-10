# Juliusのデータ読み取り
import numpy as np
import pandas as pd
import csv
import os
import math
from scipy.io import wavfile
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR

# 手順：5番目(4番目(D)のあとにJuliusでラベリングする。)
# ラベリングデータをもとに音声、EGG、EMAの無音区間をカットする

# sc.deal_dataディレクトリを開いて実行する
# {data_date}edit内に{data_date}segディレクトリをつくり、{発話番号三桁}.labがあるようにする
# data_date,start_num,end_num、カットする対象(最初にやるときは全部指定)を設定してから実行する

data_date = '20250304'
start_num = 1
end_num = 503

# スキップしたファイル番号を記録するリスト
skipped_files = []

# カットする対象を指定（'wav50k', 'wav16k', 'egg', 'ema' の中から選択）
cut_targets = ['wav50k', 'wav16k', 'egg', 'ema']  # 必要に応じて変更

for speech_num in range(start_num, end_num + 1):
    seg_path = FILE_PLACE('seg', data_date, 10, speech_num)
    wav_path = FILE_PLACE('wav50k', data_date, 10, speech_num)
    wav16_path = FILE_PLACE('wav16k', data_date, 10, speech_num)
    egg_path = FILE_PLACE('egg_csv', data_date, 10, speech_num)
    ema_path = FILE_PLACE('ema_hf_chcsv', data_date, 10, speech_num)

    # 必要なファイルが存在するか確認
    if not os.path.isfile(seg_path):
        print(f"Missing seg file for speech_num {speech_num}. Skipping...")
        skipped_files.append(speech_num)
        continue

    ## labファイルの読み込み
    try:
        silB_int = pd.read_csv(seg_path, header=None, sep=r'\s+', names=['start', 'end', 'letter']).head(1)
        silE_int = pd.read_csv(seg_path, header=None, sep=r'\s+', names=['start', 'end', 'letter']).tail(1)

        silB_time = silB_int.iloc[0]['end']
        silE_time = silE_int.iloc[0]['start']

        print(silB_time, silE_time)
    except Exception as e:
        print(f"Error reading seg file for speech_num {speech_num}: {e}")
        skipped_files.append(speech_num)
        continue

    ## サンプル数に置き換える
    sample_250_B = math.floor(silB_time * 250)
    sample_250_E = math.ceil(silE_time * 250)
    ten_time_B = sample_250_B / 250
    ten_time_E = sample_250_E / 250

    sample_50k_B = math.floor(ten_time_B * 50000)
    sample_50k_E = math.ceil(ten_time_E * 50000)
    sample_16k_B = math.floor(ten_time_B * 16000)
    sample_16k_E = math.ceil(ten_time_E * 16000)

    print('修正した時間', ten_time_B, ten_time_E)
    print('50k sample', sample_50k_B, sample_50k_E)
    print('16k sample', sample_16k_B, sample_16k_E)
    print('250 sample', sample_250_B, sample_250_E)

    ###############################################
    # wavのカット50k
    if 'wav50k' in cut_targets:
        try:
            sampling_rate, data = wavfile.read(wav_path)

            # 新しいフォルダの作成
            cutwav_path = FILE_PLACE('wav50k_cut', data_date, 10, speech_num)
            MAKE_OUTPUT_DIR(cutwav_path)

            cut_data = data[sample_50k_B:sample_50k_E]

            # 書き換えた音声データを新しいファイルに保存
            wavfile.write(cutwav_path, sampling_rate, cut_data)

            print(f"Processed file saved to: {cutwav_path}")
        except Exception as e:
            print(f"Error processing wav50k file for speech_num {speech_num}: {e}")
            skipped_files.append(speech_num)
            continue

    ################################################
    # wavのカット16k
    if 'wav16k' in cut_targets:
        try:
            sampling_rate16, data16 = wavfile.read(wav16_path)

            # 新しいフォルダの作成
            cutwav16_path = FILE_PLACE('wav16k_cut', data_date, 10, speech_num)
            MAKE_OUTPUT_DIR(cutwav16_path)

            cut_data16 = data16[sample_16k_B:sample_16k_E]

            # 書き換えた音声データを新しいファイルに保存
            wavfile.write(cutwav16_path, sampling_rate16, cut_data16)

            print(f"Processed file saved to: {cutwav16_path}")
        except Exception as e:
            print(f"Error processing wav16k file for speech_num {speech_num}: {e}")
            skipped_files.append(speech_num)
            continue

    ###############################################
    # EGGのカット
    if 'egg' in cut_targets:
        try:
            egg_data = pd.read_csv(egg_path, header=None, encoding='cp932')

            # 新しいフォルダの作成
            cutegg_path = FILE_PLACE('egg_csv_cut', data_date, 10, speech_num)
            MAKE_OUTPUT_DIR(cutegg_path)

            # eggデータの分割(最初がヘッダーで削られるため-1)
            cutegg_data = egg_data.iloc[sample_50k_B-1:sample_50k_E]

            # 分割したデータをCSVファイルとして保存
            cutegg_data.to_csv(cutegg_path, index=False, header=False, encoding='cp932')

            print(f"Processed file saved to: {cutegg_path}")
        except Exception as e:
            print(f"Error processing EGG file for speech_num {speech_num}: {e}")
            skipped_files.append(speech_num)
            continue

    ###############################################
    # EMAデータ
    if 'ema' in cut_targets:
        try:
            # ch1
            ema_ch1_path = ema_path[0]
            ema_ch1_data = pd.read_csv(ema_ch1_path, header=None, encoding='cp932')

            # 新しいフォルダの作成
            cutema_path = FILE_PLACE('ema_hf_chcsv_cut', data_date, 10, speech_num)[0]
            MAKE_OUTPUT_DIR(cutema_path)

            # emaデータの分割
            cutema_ch1_data = ema_ch1_data.iloc[sample_250_B-1:sample_250_E]

            # 分割したデータをCSVファイルとして保存
            cutema_ch1_data.to_csv(cutema_path, index=False, header=False, encoding='cp932')

            print(f"Processed file saved to: {cutema_path}")

            # ch3~12
            for ch in range(3, 13):
                ema_chN_path = ema_path[ch-2]
                ema_chN_data = pd.read_csv(ema_chN_path, header=None, encoding='cp932')

                # 新しいフォルダの作成
                cutema_path = FILE_PLACE('ema_hf_chcsv_cut', data_date, 10, speech_num)[ch-2]
                MAKE_OUTPUT_DIR(cutema_path)

                # emaデータの分割
                cutema_chN_data = ema_chN_data.iloc[sample_250_B-1:sample_250_E]

                # 分割したデータをCSVファイルとして保存
                cutema_chN_data.to_csv(cutema_path, index=False, header=False, encoding='cp932')

                print(f"Processed file saved to: {cutema_path}")
        except Exception as e:
            print(f"Error processing EMA file for speech_num {speech_num}: {e}")
            skipped_files.append(speech_num)
            continue

# スキップしたファイル番号を表示
if skipped_files:
    print("\nSkipped files:")
    print(", ".join(map(str, skipped_files)))
else:
    print("\nNo files were skipped.")