%25/1/9~
clear
%dataもeditも見えてる状態で使う
%対象データの日付
data_date = 20181115;
%基準データの日付
target_date = 20180911;
%基準データの発話番号

% ループ回数
%first→変換する初めの発話番号、last→変換する最後の発話番号
first_file = 1;
last_file = 503; 

% 各部位の平均値を保存する変数の初期化
mean_target_T1 = zeros(last_file, 2);
mean_target_T2 = zeros(last_file, 2);
mean_target_T3 = zeros(last_file, 2);
mean_target_UL = zeros(last_file, 2);
mean_target_LL = zeros(last_file, 2);
mean_target_LJ = zeros(last_file, 2);

mean_original_T1 = zeros(last_file, 2);
mean_original_T2 = zeros(last_file, 2);
mean_original_T3 = zeros(last_file, 2);
mean_original_UL = zeros(last_file, 2);
mean_original_LL = zeros(last_file, 2);
mean_original_LJ = zeros(last_file, 2);

all_target_T1_mean = zeros(1,2);
all_target_T2_mean = zeros(1,2);
all_target_T3_mean = zeros(1,2);
all_target_UL_mean = zeros(1,2);
all_target_LL_mean = zeros(1,2);
all_target_LJ_mean = zeros(1,2);

pos_list = {'UL','LL','JL','T1','T2','T3'};
%------------------------

for file_num = first_file : last_file

    % if file_num == 143
    %     continue; % 数字が143の場合はスキップ
    % end

    now_deal = sprintf('%d',file_num)

    %入力データの場所
    %editデータフォルダ
    edit_data_folder = sprintf('%dedit',data_date);
    target_data_folder = sprintf('%dedit',target_date);


    %EMA
    ema_root_folder = sprintf('%dhf_poscsv_cut_0',data_date);
    ema_folder = sprintf('%03d',file_num);
        %相対パス
        chT1_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T1.csv', file_num));
        chT2_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T2.csv', file_num));
        chT3_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T3.csv', file_num));
        chUL_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_UL.csv', file_num));
        chLL_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_LL.csv', file_num));
        chLJ_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_LJ.csv', file_num));



% 基準データの場所
    target_root_folder = sprintf('%dlpf_hf_poscsv_cut_sp_0',target_date);
    target_folder = sprintf('%03d',file_num);

    target_chT1_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_T1.csv', file_num));
    target_chT2_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_T2.csv', file_num));
    target_chT3_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_T3.csv', file_num));
    target_chUL_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_UL.csv', file_num));
    target_chLL_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_LL.csv', file_num));
    target_chLJ_fullpath = fullfile('sc.deal_data','..','..','edit',target_data_folder,target_root_folder,target_folder, sprintf('%d_LJ.csv', file_num));


%-------------------------------------------------------------

    %基準データ読み込み
    target_T1 = readmatrix(target_chT1_fullpath);
    target_T2 = readmatrix(target_chT2_fullpath);
    target_T3 = readmatrix(target_chT3_fullpath);
    target_UL = readmatrix(target_chUL_fullpath);
    target_LL = readmatrix(target_chLL_fullpath);
    target_LJ = readmatrix(target_chLJ_fullpath);

    %分析データ読み込み
    original_T1 = readmatrix(chT1_fullpath);
    original_T2 = readmatrix(chT2_fullpath);
    original_T3 = readmatrix(chT3_fullpath);
    original_UL = readmatrix(chUL_fullpath);
    original_LL = readmatrix(chLL_fullpath);
    original_LJ = readmatrix(chLJ_fullpath);
    
    
    %平均値の計算と格納
    %1発話ごとに格納していく
    mean_target_T1(file_num,:) = [mean(target_T1(:,2)) ,mean(target_T1(:,3))];
    mean_target_T2(file_num,:) = [mean(target_T2(:,2)) ,mean(target_T2(:,3))];
    mean_target_T3(file_num,:) = [mean(target_T3(:,2)) ,mean(target_T3(:,3))];
    mean_target_UL(file_num,:) = [mean(target_UL(:,2)) ,mean(target_UL(:,3))];
    mean_target_LL(file_num,:) = [mean(target_LL(:,2)) ,mean(target_LL(:,3))];
    mean_target_LJ(file_num,:) = [mean(target_LJ(:,2)) ,mean(target_LJ(:,3))];

    mean_original_T1(file_num,:) = [mean(original_T1(:,2)) ,mean(original_T1(:,3))];
    mean_original_T2(file_num,:) = [mean(original_T2(:,2)) ,mean(original_T2(:,3))];
    mean_original_T3(file_num,:) = [mean(original_T3(:,2)) ,mean(original_T3(:,3))];
    mean_original_UL(file_num,:) = [mean(original_UL(:,2)) ,mean(original_UL(:,3))];
    mean_original_LL(file_num,:) = [mean(original_LL(:,2)) ,mean(original_LL(:,3))];
    mean_original_LJ(file_num,:) = [mean(original_LJ(:,2)) ,mean(original_LJ(:,3))];

    %全発話
    % すべてのファイルの平均値を計算
    all_target_T1_mean = [mean(mean_target_T1(:,1)),mean(mean_target_T1(:,2))];
    all_target_T2_mean = [mean(mean_target_T2(:,1)),mean(mean_target_T2(:,2))];
    all_target_T3_mean = [mean(mean_target_T3(:,1)),mean(mean_target_T3(:,2))];
    all_target_UL_mean = [mean(mean_target_UL(:,1)),mean(mean_target_UL(:,2))];
    all_target_LL_mean = [mean(mean_target_LL(:,1)),mean(mean_target_LL(:,2))];
    all_target_LJ_mean = [mean(mean_target_LJ(:,1)),mean(mean_target_LJ(:,2))];

    all_original_T1_mean = [mean(mean_original_T1(:,1)),mean(mean_original_T1(:,2))];
    all_original_T2_mean = [mean(mean_original_T2(:,1)),mean(mean_original_T2(:,2))];
    all_original_T3_mean = [mean(mean_original_T3(:,1)),mean(mean_original_T3(:,2))];
    all_original_UL_mean = [mean(mean_original_UL(:,1)),mean(mean_original_UL(:,2))];
    all_original_LL_mean = [mean(mean_original_LL(:,1)),mean(mean_original_LL(:,2))];
    all_original_LJ_mean = [mean(mean_original_LJ(:,1)),mean(mean_original_LJ(:,2))];

end

    % figure(1)
    % plot(all_target_T1_mean(1),all_target_T1_mean(2),'x')
    % hold on
    % plot(all_target_T2_mean(1),all_target_T2_mean(2),'x')
    % plot(all_target_T3_mean(1),all_target_T3_mean(2),'x')
    % plot(all_target_UL_mean(1),all_target_UL_mean(2),'x')
    % plot(all_target_LL_mean(1),all_target_LL_mean(2),'x')
    % plot(all_target_LJ_mean(1),all_target_LJ_mean(2),'x')
    % title('target')
    % 
    % figure(2)
    % plot(all_original_T1_mean(1),all_original_T1_mean(2),'o')
    % hold on
    % plot(all_original_T2_mean(1),all_original_T2_mean(2),'o')
    % plot(all_original_T3_mean(1),all_original_T3_mean(2),'o')
    % plot(all_original_UL_mean(1),all_original_UL_mean(2),'o')
    % plot(all_original_LL_mean(1),all_original_LL_mean(2),'o')
    % plot(all_original_LJ_mean(1),all_original_LJ_mean(2),'o')
    % title('original')

    all_target_mean = [all_target_T1_mean; all_target_T2_mean;
                       all_target_T3_mean; all_target_UL_mean
                       all_target_LL_mean; all_target_LJ_mean];
    all_original_mean = [all_original_T1_mean; all_original_T2_mean;
                         all_original_T3_mean; all_original_UL_mean
                         all_original_LL_mean; all_original_LJ_mean];
    
    % transform-T,b,c　T：回転行列、b：スケーリング因子、c：並行移動因子
    % [d,opa,transform] = procrustes(all_target_mean,all_original_mean);
    [d2,opa2,transform2] = procrustes(all_target_mean, all_original_mean,'scaling',false);

    % figure(3)
    % plot(opa2(:,1), opa2(:,2))
    % title('procrustes-scale"off"')
    
    for file_num = first_file : last_file

        % if file_num == 143
        % continue; % 数字が143の場合はスキップ
        % end

    now_deal = sprintf('%d',file_num)

    ema_folder = sprintf('%03d',file_num);
        %相対パス
        chT1_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T1.csv', file_num));
        chT2_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T2.csv', file_num));
        chT3_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_T3.csv', file_num));
        chUL_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_UL.csv', file_num));
        chLL_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_LL.csv', file_num));
        chLJ_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,ema_root_folder,ema_folder, sprintf('%d_LJ.csv', file_num));
    
    %出力場所
    output_root_folder = sprintf('%hf_poscsv_cut_0_opa',data_date);
    output_folder = sprintf('target_%d',target_date);
        %絶対パス
        %output_fullpath = fullfile('/Users','ikedaeri','MATLAB','dataset_deal',output_double_folder,output_root_folder,output_filename)
        %相対パス
        chT1_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_T1.csv', file_num));
        chT2_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_T2.csv', file_num));
        chT3_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_T3.csv', file_num));
        chUL_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_UL.csv', file_num));
        chLL_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_LL.csv', file_num));
        chLJ_out_fullpath = fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder, output_folder, ema_folder, sprintf('%d_LJ.csv', file_num));

   %ないときは出力フォルダを作る
    if ~exist(fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder,output_folder, ema_folder), 'dir')
        mkdir(fullfile('sc.deal_data','..','..','edit',edit_data_folder,output_root_folder,output_folder, ema_folder));
    end   
     
    %分析データ読み込み
    original_T1 = readmatrix(chT1_fullpath);
    original_T2 = readmatrix(chT2_fullpath);
    original_T3 = readmatrix(chT3_fullpath);
    original_UL = readmatrix(chUL_fullpath);
    original_LL = readmatrix(chLL_fullpath);
    original_LJ = readmatrix(chLJ_fullpath);

    %サンプルごとのセットにして処理
    for i = 1 : length(original_T1)
        
        sample_shape = [original_T1(i,2), original_T1(i,3);
                        original_T2(i,2), original_T2(i,3);
                        original_T3(i,2), original_T3(i,3);
                        original_UL(i,2), original_UL(i,3);
                        original_LL(i,2), original_LL(i,3);
                        original_LJ(i,2), original_LJ(i,3);];
        
        %さっき平均したopaで変換　Z = bYT + c
        opa_trans = sample_shape * transform2.T + transform2.c;

        %opaした値に更新する
        original_T1(i,2:3) = opa_trans(1,:);
        original_T2(i,2:3) = opa_trans(2,:);
        original_T3(i,2:3) = opa_trans(3,:);
        original_UL(i,2:3) = opa_trans(4,:);
        original_LL(i,2:3) = opa_trans(5,:);
        original_LJ(i,2:3) = opa_trans(6,:);

    end

        %更新した値で保存する
        writematrix(original_T1, chT1_out_fullpath);
        writematrix(original_T2, chT2_out_fullpath);
        writematrix(original_T3, chT3_out_fullpath);
        writematrix(original_UL, chUL_out_fullpath);
        writematrix(original_LL, chLL_out_fullpath);
        writematrix(original_LJ, chLJ_out_fullpath);
  

    end
