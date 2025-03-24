# spファイルの場所
# EMA_observationを開くなら一つ上、sc.deal_data/を開くなら二つ上
# sc.deal_data/を開くつもりで作る

import os

# 入力、出力に必要なファイルの場所
def FILE_PLACE(file_type, data_date, keta_45, speech_num):
    date_dir = f'{data_date}'
    root_dir = f'{data_date}{keta_45:02d}{speech_num:03d}mov'
    edit_dir = f'{data_date}edit'
    
    if file_type == 'sp':
        filename = f'AD{data_date}{keta_45:02d}{speech_num:03d}_0.sp_hpf'
        fullpath = os.path.join('sc.deal_data','..','..','data', date_dir, root_dir, filename)

    elif file_type == 'wav50k':
        # 旧版
        # root_dir = f'{data_date}hpf_wav_50k'
        root_dir = f'{data_date}wav_50k'
        filename = f'{speech_num:03d}.wav'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'wav50k_cut':
        # 旧版
        # root_dir = f'{data_date}hpf_wav_50k'
        root_dir = f'{data_date}wav_50k_cut'
        filename = f'{speech_num:03d}.wav'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'wav16k':
        # 旧版
        # root_dir = f'{data_date}hpf_wav_16k'
        root_dir = f'{data_date}wav_16k'
        filename = f'{speech_num:03d}.wav'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'wav16k_cut':
        # 旧版
        # root_dir = f'{data_date}hpf_wav_16k_cut'
        root_dir = f'{data_date}wav_16k_cut'
        filename = f'{speech_num:03d}.wav'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'egg':
        filename = f'AD{data_date}{keta_45:02d}{speech_num:03d}_0.egg_hpf'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'data', date_dir, root_dir, filename)

    elif file_type == 'egg_csv':
        root_dir = f'{data_date}hpf_egg_csv'
        filename = f'{speech_num:03d}.csv'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'egg_csv_cut':
        root_dir = f'{data_date}hpf_egg_csv_cut'
        filename = f'{speech_num:03d}.csv'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'ema':
        ema_root_dir = f'S{data_date}_D{data_date}{keta_45:02d}{speech_num:03d}mov'
        fullpaths = []
        for ch in range(1, 13):
            if ch == 2:
                continue
            filename = f'hfS{data_date}_D{data_date}{keta_45:02d}{speech_num:03d}mov_0_ch{ch}_POS_angle_lpf.data'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'data', date_dir, root_dir, ema_root_dir, filename)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths
    
    elif file_type == 'ema_hf_chcsv':
        # 旧版
        # root_dir = f'{data_date}lpf_hf_csv'
        root_dir = f'{data_date}hf_chcsv'
        ema_root_dir = f'{speech_num:03d}'
        fullpaths = []
        for ch in range(1, 13):
            if ch == 2:
                continue
            filename = f'{speech_num}_ch{ch}.csv'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, ema_root_dir, filename)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths
    
    elif file_type == 'ema_hf_chcsv_cut':
        # 旧版
        # root_dir = f'{data_date}lpf_hf_csv_cut_sp'
        root_dir = f'{data_date}hf_chcsv_cut'
        ema_root_dir = f'{speech_num:03d}'
        fullpaths = []
        for ch in range(1, 13):
            if ch == 2:
                continue
            filename = f'{speech_num}_ch{ch}.csv'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, ema_root_dir, filename)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths
    
    elif file_type == 'ema_hf_poscsv':
        # 旧版
        #root_dir = f'{data_date}lpf_hf_poscsv'
        root_dir = f'{data_date}hf_poscsv'
        ema_root_dir = f'{speech_num:03d}'
        pos_list = ['NA', 'ND', 'UI', 'UL', 'LL', 'LJ', 'T1', 'T2', 'T3']
        fullpaths = []
        for pos in pos_list:
            #filename = f'{speech_num}_{pos}.csv'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, ema_root_dir)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths
    
    elif file_type == 'ema_hf_poscsv_cut':
        # 旧版
        #root_dir = f'{data_date}lpf_hf_poscsv_cut_sp'
        root_dir = f'{data_date}hf_poscsv_cut'
        ema_root_dir = f'{speech_num:03d}'
        pos_list = ['NA', 'ND', 'UI', 'UL', 'LL', 'LJ', 'T1', 'T2', 'T3']
        fullpaths = []
        for pos in pos_list:
            #filename = f'{speech_num}_{pos}.csv'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, ema_root_dir)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths
    
    elif file_type == 'ema_hf_poscsv_cut_0':
        # 旧版
        #root_dir = f'{data_date}lpf_hf_poscsv_cut_sp'
        root_dir = f'{data_date}hf_poscsv_cut_0'
        ema_root_dir = f'{speech_num:03d}'
        pos_list = ['NA', 'ND', 'UI', 'UL', 'LL', 'LJ', 'T1', 'T2', 'T3']
        fullpaths = []
        for pos in pos_list:
            #filename = f'{speech_num}_{pos}.csv'
            fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, ema_root_dir)
            if os.path.exists(fullpath):
                print(f"File exists: {fullpath}")
            else:
                print(f"File does not exist: {fullpath}")
            fullpaths.append(fullpath)
        return fullpaths

    elif file_type == 'seg':
        root_dir = f'{data_date}seg'
        filename = f'{speech_num:03d}.lab'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    elif file_type == 'seg_cut':
        root_dir = f'{data_date}seg_cut'
        filename = f'{speech_num:03d}.lab'
        fullpath = os.path.join('sc.deal_data', '..', '..', 'edit', edit_dir, root_dir, filename)

    if os.path.exists(fullpath):
        print(f"File exists: {fullpath}")
    else:
        print(f"File does not exist: {fullpath}")

    return fullpath

# 出力ディレクトリを作る
def MAKE_OUTPUT_DIR(output_fullpath):
    output_dir = os.path.dirname(output_fullpath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory created: {output_dir}")
    else:
        print(f"Directory already exists: {output_dir}")
