import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR

# 手順：2番目(1番目はmatlabでフィルタリング)
# spを取得して50kHzのwavに変換、ラベリング用の16kHzのwavも作成

# data_date,first_file,last_file,keta_45を設定してから実行する
# {data_date}editはedit内に作っておく

# 処理する観測日
data_date = 20181115
# ループ回数                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
first_file = 1
last_file = 503
# sampling Fs
fs = 50000
fs_resampled = 16000

for file_num in range(first_file, last_file + 1):
    print(f"{file_num}")

    # keta_45の設定
    if file_num <= 50:
        keta_45 = 10
    elif file_num <= 100:
        keta_45 = 10
    elif file_num <= 150:
        keta_45 = 10
    elif file_num <= 200:
        keta_45 = 10
    elif file_num <= 250:
        keta_45 = 10
    elif file_num <= 300:
        keta_45 = 10
    elif file_num <= 350:
        keta_45 = 10
    elif file_num <= 400:
        keta_45 = 10
    elif file_num <= 450:
        keta_45 = 10
    else:
        keta_45 = 10

    # spファイル場所とファイル名
    input_fullpath = FILE_PLACE('sp', data_date, keta_45, file_num)

    # 出力ファイルの場所とファイル名 (50k)
    output_fullpath_50k = FILE_PLACE('wav50k', data_date, keta_45, file_num)
    MAKE_OUTPUT_DIR(output_fullpath_50k)

    # 出力ファイルの場所とファイル名 (16k)
    output_fullpath_16k = FILE_PLACE('wav16k', data_date, keta_45, file_num)
    MAKE_OUTPUT_DIR(output_fullpath_16k)

    # ファイルの読み込み
    inputfile = np.loadtxt(input_fullpath)

    # データの正規化
    inputfile = inputfile / np.max(np.abs(inputfile))

    # ファイルの書き込み (50k)
    wavfile.write(output_fullpath_50k, fs, inputfile.astype(np.float32))

    # データのリサンプリング (16k)
    num_samples = int(len(inputfile) * fs_resampled / fs)
    resampled_data = resample(inputfile, num_samples)

    # ファイルの書き込み (16k)
    wavfile.write(output_fullpath_16k, fs_resampled, resampled_data.astype(np.float32))
