import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR
from def_code_date import code

# 収録日
data_date = 20180911

# 発話者コードの取得
speaker_code = code.get(data_date, 'Unknown')

start_num = 100
end_num = 150

# 出力フォルダの指定
output_folder = 'output_videos'
output_fullpath = os.path.join(output_folder, speaker_code)
os.makedirs(output_fullpath, exist_ok=True)

for file_num in range(start_num, end_num + 1):
    now_deal = str(file_num)

    # 入力ファイルの場所
    input_paths = FILE_PLACE('ema_hf_poscsv_cut_sp_0_opa', data_date, 10, file_num)
    if not input_paths:
        continue

    UL_file = input_paths[0]
    LL_file = input_paths[1]
    LJ_file = input_paths[2]
    T1_file = input_paths[3]
    T2_file = input_paths[4]
    T3_file = input_paths[5]
    # UI_file = input_paths[6]

    # EMAデータの読み込み
    UL = pd.read_csv(UL_file, header=None).values
    LL = pd.read_csv(LL_file, header=None).values
    T1 = pd.read_csv(T1_file, header=None).values
    T2 = pd.read_csv(T2_file, header=None).values
    T3 = pd.read_csv(T3_file, header=None).values
    LJ = pd.read_csv(LJ_file, header=None).values
    # UI = pd.read_csv(UI_file, header=None).values

    # ビデオライターのセットアップ
    video_filename = os.path.join(output_fullpath, f'{speaker_code}_{file_num:03d}.mp4')
    writer = FFMpegWriter(fps=30)

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    plotUL, = ax.plot([], [], 'o-')
    plotLL, = ax.plot([], [], 'o-')
    plotT1, = ax.plot([], [], 'o-')
    plotT2, = ax.plot([], [], 'o-')
    plotT3, = ax.plot([], [], 'o-')
    plotLJ, = ax.plot([], [], 'o-')

    current_pointUL, = ax.plot([], [], 'o')
    current_pointLL, = ax.plot([], [], 'o')
    current_pointT1, = ax.plot([], [], 'o')
    current_pointT2, = ax.plot([], [], 'o')
    current_pointT3, = ax.plot([], [], 'o')
    current_pointLJ, = ax.plot([], [], 'o')

    line_handle_12, = ax.plot([], [], 'k-')
    line_handle_23, = ax.plot([], [], 'k-')

    if UI_disp == 1:
        plotUI, = ax.plot(UI[:, 1], UI[:, 2], 'o', markersize=10, markerfacecolor='r')

    file_num_text = ax.text(0.5, 0.5, f'File Num: {file_num}', transform=ax.transAxes, fontsize=14, color='red')

    def update(k):
        plotUL.set_data(UL[:k, 1], UL[:k, 2])
        plotLL.set_data(LL[:k, 1], LL[:k, 2])
        plotT1.set_data(T1[:k, 1], T1[:k, 2])
        plotT2.set_data(T2[:k, 1], T2[:k, 2])
        plotT3.set_data(T3[:k, 1], T3[:k, 2])
        plotLJ.set_data(LJ[:k, 1], LJ[:k, 2])

        current_pointUL.set_data(UL[k, 1], UL[k, 2])
        current_pointLL.set_data(LL[k, 1], LL[k, 2])
        current_pointT1.set_data(T1[k, 1], T1[k, 2])
        current_pointT2.set_data(T2[k, 1], T2[k, 2])
        current_pointT3.set_data(T3[k, 1], T3[k, 2])
        current_pointLJ.set_data(LJ[k, 1], LJ[k, 2])

        line_handle_12.set_data([T1[k, 1], T2[k, 1]], [T1[k, 2], T2[k, 2]])
        line_handle_23.set_data([T2[k, 1], T3[k, 1]], [T2[k, 2], T3[k, 2]])

        file_num_text.set_text(f'File Num: {file_num}')

        return plotUL, plotLL, plotT1, plotT2, plotT3, plotLJ, current_pointUL, current_pointLL, current_pointT1, current_pointT2, current_pointT3, current_pointLJ, line_handle_12, line_handle_23, file_num_text

    ani = plt.FuncAnimation(fig, update, frames=len(UL), blit=True)

    ani.save(video_filename, writer=writer)
    plt.clf()
    plt.close(fig)

    print(f"{file_num}：すべてのファイルを処理しました。")