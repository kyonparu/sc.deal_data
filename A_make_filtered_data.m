%close all
% EMA_obsevation �f�B���N�g�������݂̃t�H���_�ɂ��Ď��s
% ������EMA�f�[�^�̂ӂ��邽��������
%data�t�H���_�̏ꏊ
header1 ='sc.deal_data/..';
%data�t�H���_
header2='/data/';
%��������f�[�^�̓��t
d_date='20250304';
START_ID= 20002;
END_ID= 20003;
s_date=d_date;
start_ch = 1;
end_ch = 12;
without_ch = 2;
f_ema = 250;

%M3-1:501-503�ӂ����邳�����������傤�ɂł���
for ID=START_ID:END_ID
    now_deal = sprintf('%d',ID)
    %�t�@�C����
    date_dir = [d_date, '/'];
    date_id_format = [d_date, '%05d'];
    date_id=sprintf(date_id_format, ID);
    mov_dir = [date_id, 'mov/'];
    c_mov_dir = [header1, header2, date_dir, mov_dir];
    SD_dir_s = ['hfS', s_date, '_D', date_id, 'mov'];
    SD_dir = ['S', s_date, '_D', mov_dir];

    %�f�[�^�̃C���|�[�g
    filesp=[c_mov_dir, 'AD', date_id, '_0.sp'];
    x=importdata(filesp);
    x=double(x)/32678; %���ꉽ���Ă��
    %�n�C�p�X�t�B���^�̐݌v(�t�B���^����,�J�b�g�I�t���g��,�n�C�p�X,�t�B���^�[�̐U��������1)
    bhpf=fir1(2048, 0.002,'high', 'scale');
    %�M���̃t�B���^�����Ofiltfilt���ʑ��x��̕⏞
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