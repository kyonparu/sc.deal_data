import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from def_file_place import FILE_PLACE, OPA_FILE_PLACE ,MAKE_OUTPUT_DIR
from def_code_date import code

# 収録日
data_date = 20181115
target_date = 20180911

# 発話者コードの取得
speaker_code = code.get(str(data_date))  # def_code_date.pyの辞書から取得

if not speaker_code:
    raise ValueError(f"No speaker code found for {data_date}")

start_num = 1
end_num = 1

for file_num in range(start_num, end_num + 1):
    now_deal = str(file_num)

    # 入力ファイルの場所
    input_paths = OPA_FILE_PLACE(data_date, target_date, speech_num=file_num)
    if not input_paths:
        print(f"Skipping file_num: {file_num} due to missing input paths.")
        continue
    print(f"file_num {file_num}: {input_paths}")

    #出力ファイルの場所
    output_paths = FILE_PLACE('video', data_date, 10,file_num)
    MAKE_OUTPUT_DIR(output_paths)  # 出力先のディレクトリを作成

    UL_file = os.path.join(input_paths[0], f"{file_num}_UL.csv")
    LL_file = os.path.join(input_paths[1], f"{file_num}_LL.csv")
    LJ_file = os.path.join(input_paths[2], f"{file_num}_LJ.csv")
    T1_file = os.path.join(input_paths[3], f"{file_num}_T1.csv")
    T2_file = os.path.join(input_paths[4], f"{file_num}_T2.csv")
    T3_file = os.path.join(input_paths[5], f"{file_num}_T3.csv")

    # EMAデータの読み込み
    try:
        UL = pd.read_csv(UL_file, header=None).values
        LL = pd.read_csv(LL_file, header=None).values
        T1 = pd.read_csv(T1_file, header=None).values
        T2 = pd.read_csv(T2_file, header=None).values
        T3 = pd.read_csv(T3_file, header=None).values
        LJ = pd.read_csv(LJ_file, header=None).values
    except FileNotFoundError as e:
        print(f"Error reading files for file_num: {file_num}. Skipping...")
        print(e)
        continue

    print("UL sample:\n", UL[:5])
    print("T1 sample:\n", T1[:5])
    
    # ビデオライターのセットアップ
    video_filename = output_paths  # 出力ファイル名を取得
    writer = FFMpegWriter(fps=30)

    fig, ax = plt.subplots()

    x_min = min(UL[:, 1].min(), LL[:, 1].min(), LJ[:, 1].min())
    x_max = max(T1[:, 1].max(), T2[:, 1].max(), T3[:, 1].max())
    y_min = min(LJ[:, 2].min(), LL[:, 2].min())
    y_max = max(UL[:, 2].max(), T2[:, 2].max(), T3[:, 2].max())

    ax.set_xlim(x_min - 20, x_max + 20)
    ax.set_ylim(y_min - 20, y_max + 20)

    # カラーとラベルの設定
    colors = ['r', 'g', 'b', 'c', 'm', 'orange']
    points = ['UL', 'LL', 'LJ', 'T1', 'T2', 'T3']
    lines = []

    # 各ポイントのプロットを作成（過去の軌跡を細く設定）
    for i in range(6):
        (line,) = ax.plot([], [], 'o-', color=colors[i], label=points[i], linewidth=0.01)  # 軌跡の線を細くする
        lines.append(line)

    # 現在のポイントをプロットするための設定（今の点を太く設定）
    current_points = []
    for i in range(6):
        (current_point,) = ax.plot([], [], 'o', color=colors[i], markersize=10)#在のポイントのサイズを大きく設定
        current_points.append(current_point)

    # 線のプロット（T1-T2, T2-T3）
    line_handle_12, = ax.plot([], [], 'k-', linewidth=1.0)  # 線の太さを調整
    line_handle_23, = ax.plot([], [], 'k-', linewidth=1.0)  # 線の太さを調整

    file_num_text = ax.text(0.5, 0.5, f'File Num: {file_num}', transform=ax.transAxes, fontsize=14, color='red')

    def update(k):
        # 過去のデータをプロット
        lines[0].set_data(UL[:k, 1], UL[:k, 2])
        lines[1].set_data(LL[:k, 1], LL[:k, 2])
        lines[2].set_data(LJ[:k, 1], LJ[:k, 2])
        lines[3].set_data(T1[:k, 1], T1[:k, 2])
        lines[4].set_data(T2[:k, 1], T2[:k, 2])
        lines[5].set_data(T3[:k, 1], T3[:k, 2])

        # 現在のポイントをプロット
        current_points[0].set_data([UL[k, 1]], [UL[k, 2]])
        current_points[1].set_data([LL[k, 1]], [LL[k, 2]])
        current_points[2].set_data([LJ[k, 1]], [LJ[k, 2]])
        current_points[3].set_data([T1[k, 1]], [T1[k, 2]])
        current_points[4].set_data([T2[k, 1]], [T2[k, 2]])
        current_points[5].set_data([T3[k, 1]], [T3[k, 2]])

        # 線を更新
        line_handle_12.set_data([T1[k, 1], T2[k, 1]], [T1[k, 2], T2[k, 2]])
        line_handle_23.set_data([T2[k, 1], T3[k, 1]], [T2[k, 2], T3[k, 2]])

        # テキストを更新
        file_num_text.set_text(f'File Num: {file_num}')

        return (
            *lines,
            *current_points,
            line_handle_12,
            line_handle_23,
            file_num_text
        )

    # アニメーションのフレーム数を確認
    print(f"Number of frames: {len(UL)}")

    ani = FuncAnimation(fig, update, frames=len(UL), blit=True)
    ani.save(output_paths, writer=writer)
    plt.clf()
    plt.close(fig)

    print(f"{file_num}: Video saved to {output_paths}")