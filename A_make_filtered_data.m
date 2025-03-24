%close all
% EMA_obsevation ディレクトリを現在のフォルダにして実行
% 音声とEMAデータのふぃるたをかける
%dataフォルダの場所
header1 ='sc.deal_data/..';
%dataフォルダ
header2='/data/';
%処理するデータの日付
d_date='20250304';
START_ID= 20002;
END_ID= 20003;
s_date=d_date;
start_ch = 1;
end_ch = 12;
without_ch = 2;
f_ema = 250;

%M3-1:501-503ふぁいるさいずがいじょうにでかい
for ID=START_ID:END_ID
    now_deal = sprintf('%d',ID)
    %ファイル名
    date_dir = [d_date, '/'];
    date_id_format = [d_date, '%05d'];
    date_id=sprintf(date_id_format, ID);
    mov_dir = [date_id, 'mov/'];
    c_mov_dir = [header1, header2, date_dir, mov_dir];
    SD_dir_s = ['hfS', s_date, '_D', date_id, 'mov'];
    SD_dir = ['S', s_date, '_D', mov_dir];

    %データのインポート
    filesp=[c_mov_dir, 'AD', date_id, '_0.sp'];
    x=importdata(filesp);
    x=double(x)/32678; %これ何してるの
    %ハイパスフィルタの設計(フィルタ次数,カットオフ周波数,ハイパス,フィルターの振幅応答が1)
    bhpf=fir1(2048, 0.002,'high', 'scale');
    %信号のフィルタリングfiltfilt→位相遅れの補償
    xsp = filtfilt(bhpf,1,x);

    filespf=[filesp, '_hpf'];
    filespf_ID=fopen(filespf, 'w');

    fprintf(filespf_ID,'%f\n', double(round(xsp*32678.0)));
    blpf=fir1(48,0.1,'low','scale');

    fclose(filespf_ID);
    
    for k=start_ch:end_ch
        if k==without_ch
            continue;
        else
            fileema_fm=[c_mov_dir, SD_dir, SD_dir_s,...
                '_0_ch%d_POS_angle.data'];
            fileema_filtered=[c_mov_dir, SD_dir, SD_dir_s,...
                '_0_ch%d_POS_angle_lpf.data'];
            fileema_name = sprintf(fileema_fm, k);
            fileema_name_filtered = sprintf(fileema_filtered, k);
            M = readmatrix(fileema_name, 'FileType','text');
            O_M = M;
            a=mean(M);
            for l=1:3
                M_a = M(:,l) - a(l);
                O_M(:,l) = filtfilt(blpf,1,M_a)+a(l);
            end
            figure(4)
            [nraw, ncol]=size(O_M);
            writematrix(fileema_name_filtered, O_M, 'delimiter', '\t');
            time=(1:nraw)/f_ema;
            plot(time, M(:,3));
            hold on
            plot(time, O_M(:,3));
            hold off
        end
    end
end
%Nsp=length(xsp)