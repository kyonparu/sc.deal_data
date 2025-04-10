import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import speedx
from def_file_place import FILE_PLACE, MAKE_OUTPUT_DIR
from def_code_date import code

# 手順：9番目
# UIをxyz=0にして各座標を調整する

# sc.deal_dataディレクトリを開いて実行する
# data_dateを設定してから実行する

data_date = 20250304


# 動画を処理するフォルダと出力先フォルダを指定
input_folder = os.path.dirname(FILE_PLACE('video', data_date, 10, 1))  # 元動画が入っているフォルダ（例としてspeech_num=1を指定）
output_folder = os.path.dirname(FILE_PLACE('speed_video', data_date, 10, 1))  # 処理結果を保存するフォルダ
MAKE_OUTPUT_DIR(output_folder)  # 出力先のディレクトリを作成

# 動画ファイルを連番でグループ化
files = sorted([f for f in os.listdir(input_folder) if f.endswith(".mp4")])
group_size = 50

for i in range(0, len(files), group_size):
    group_files = files[i:i + group_size]
    group_number = i // group_size + 1

    # グループごとに動画を高速化して結合
    clips = []
    for filename in group_files:
        filepath = os.path.join(input_folder, filename)

        clip = VideoFileClip(filepath)
        clip = speedx.speedx(clip, 4)  # 動画を4倍速に高速化

        clips.append(clip)

    # 動画を結合
    concatenated_clip = concatenate_videoclips(clips, method="compose")

    # フォルダ名 (A, B, ..., J)
    folder_label = chr(ord('A') + (group_number - 1))

    # 出力ファイル名を変更
    speaker_code = code.get(str(data_date))  # 話者コードを取得
    if not speaker_code:
        raise ValueError(f"No speaker code found for {data_date}")
    output_file = os.path.join(output_folder, f"{speaker_code}_{folder_label}.mp4")
    concatenated_clip.write_videofile(output_file, codec="libx264")

    # リソースを解放
    concatenated_clip.close()
    for clip in clips:
        clip.close()

print("すべての動画処理が完了しました！")
