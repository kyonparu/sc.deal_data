%close all
%手順：1番目（音声とemaは別ファイル）eggデータのハイパスフィルタ処理

% dataとsc.deal_dataが見えてる状態で実行

% START_IDは処理始めの発話番号(5桁)
% END_IDは処理終わりの発話番号(5桁)START_IDから連番でファイルが存在しないとできない

header1='sc.deal_data/../..';
header2='/data/';
d_date='20250304';
 START_ID=10001;
 END_ID=10050;

for ID=START_ID:END_ID
    now_ID = sprintf('%d',ID)

    date_dir = [d_date, '/'];
    date_id_format = [d_date, '%05d'];
    date_id=sprintf(date_id_format, ID);
    mov_dir = [date_id, 'mov/'];
    c_mov_dir = [header1, header2, date_dir, mov_dir];

    fileegg=[c_mov_dir, 'AD', date_id, '_0.egg'];
    x=importdata(fileegg);
    x=double(x)/32678;
    bhpf=fir1(2048, 0.002,'high', 'scale');
    xegg = filtfilt(bhpf,1,x);

    fileegf=[fileegg, '_hpf'];
    fileegf_ID=fopen(fileegf, 'w');

    fprintf(fileegf_ID,'%f\n', double(round(xegg*32678.0)));
    blpf=fir1(48,0.1,'low','scale');

    fclose(fileegf_ID);
end
%Nsp=length(xsp)

