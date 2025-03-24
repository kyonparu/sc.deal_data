% filepath: d:\ikeda_data\DNN_exp\sc.deal_data\H_ema_procrustes.m
clear

% 対象データの日付
data_date = 20181115;
% 基準データの日付
target_date = 20180911;

% ループ回数
first_file = 1;
last_file = 503;

% 各部位のリスト
pos_list = {'T1', 'T2', 'T3', 'UL', 'LL', 'LJ'};

% スキップしたファイル番号を記録するリスト
skipped_files = [];

% 平均値を保存する変数の初期化
mean_target = zeros(last_file, 6, 2);
mean_original = zeros(last_file, 6, 2);

% 全体の平均値を保存する変数
all_target_mean = zeros(6, 2);
all_original_mean = zeros(6, 2);

% ファイルごとの処理
for file_num = first_file:last_file
    fprintf('Processing file: %d\n', file_num);

    % 入力データのフォルダとファイルパス
    edit_data_folder = sprintf('%dedit', data_date);
    target_data_folder = sprintf('%dedit', target_date);
    ema_root_folder = sprintf('%dlpf_hf_poscsv_cut_0', data_date);
    target_root_folder = sprintf('%dlpf_hf_poscsv_cut_sp_0', target_date);

    % 出力フォルダ
    output_root_folder = sprintf('%dhf_poscsv_cut_0_opa', data_date);
    output_folder = sprintf('target_%d', target_date);
    output_dir = fullfile('sc.deal_data','..','edit', edit_data_folder, output_root_folder, output_folder, sprintf('%03d', file_num));

    % 出力フォルダが存在しない場合は作成
    if ~exist(output_dir, 'dir')
        mkdir(output_dir);
    end

    % 各部位のファイルパスを生成
    try
        target_files = generate_file_paths('sc.deal_data','..','..','edit',target_data_folder, target_root_folder, sprintf('%03d', file_num), pos_list, file_num);
        original_files = generate_file_paths('sc.deal_data','..','..','edit',edit_data_folder, ema_root_folder, sprintf('%03d', file_num), pos_list, file_num);
        output_files = generate_file_paths('sc.deal_data','..','..','edit',edit_data_folder, output_root_folder, fullfile(output_folder, sprintf('%03d', file_num)), pos_list, file_num);
    catch
        fprintf('Error generating file paths for file_num: %d. Skipping...\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % 基準データと分析データの読み込み
    try
        [target_data, original_data] = load_data(target_files, original_files, pos_list);
    catch
        fprintf('Error loading data for file_num: %d. Skipping...\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % 平均値の計算
    for i = 1:length(pos_list)
        mean_target(file_num, i, :) = mean(target_data{i}(:, 2:3), 1);
        mean_original(file_num, i, :) = mean(original_data{i}(:, 2:3), 1);
    end
end

% 全体の平均値を計算
all_target_mean = squeeze(mean(mean_target, 1));
all_original_mean = squeeze(mean(mean_original, 1));

% プロクルステス変換
[d, opa, transform] = procrustes(all_target_mean, all_original_mean, 'scaling', false);

% ファイルごとの変換と保存
for file_num = first_file:last_file
    fprintf('Applying Procrustes transformation for file: %d\n', file_num);

    % 各部位のファイルパスを生成
    try
        original_files = generate_file_paths(edit_data_folder, ema_root_folder, sprintf('%03d', file_num), pos_list, file_num);
        output_files = generate_file_paths(edit_data_folder, output_root_folder, fullfile(output_folder, sprintf('%03d', file_num)), pos_list, file_num);
    catch
        fprintf('Error generating file paths for file_num: %d. Skipping...\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % 分析データの読み込み
    try
        original_data = load_data(original_files, {}, pos_list);
    catch
        fprintf('Error loading data for file_num: %d. Skipping...\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % プロクルステス変換を適用
    for i = 1:length(pos_list)
        for j = 1:size(original_data{i}, 1)
            sample_shape = original_data{i}(j, 2:3);
            transformed_shape = sample_shape * transform.T + transform.c;
            original_data{i}(j, 2:3) = transformed_shape;
        end
    end

    % 変換後のデータを保存
    try
        save_data(output_files, original_data, pos_list);
    catch
        fprintf('Error saving data for file_num: %d. Skipping...\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end
end

% スキップしたファイル番号を表示
if ~isempty(skipped_files)
    fprintf('Skipped files: %s\n', num2str(skipped_files));
else
    fprintf('No files were skipped.\n');
end

% 関数: ファイルパスを生成
function file_paths = generate_file_paths(root_folder, sub_folder, ema_folder, pos_list, file_num)
    file_paths = cell(1, length(pos_list));
    for i = 1:length(pos_list)
        file_paths{i} = fullfile('edit', root_folder, sub_folder, ema_folder, sprintf('%d_%s.csv', file_num, pos_list{i}));
    end
end

% 関数: データを読み込む
function [target_data, original_data] = load_data(target_files, original_files, pos_list)
    target_data = cell(1, length(pos_list));
    original_data = cell(1, length(pos_list));
    for i = 1:length(pos_list)
        if ~isempty(target_files)
            target_data{i} = readmatrix(target_files{i});
        end
        if ~isempty(original_files)
            original_data{i} = readmatrix(original_files{i});
        end
    end
end

% 関数: データを保存する
function save_data(output_files, data, pos_list)
    for i = 1:length(pos_list)
        writematrix(data{i}, output_files{i});
    end
end

% filepath: d:\ikeda_data\DNN_exp\sc.deal_data\H_traial.m
clear

% 対象データの日付
data_date = 20181115;
% 基準データの日付
target_date = 20180911;

% ループ回数
first_file = 1;
last_file = 503;

% 各部位のリスト
pos_list = {'T1', 'T2', 'T3', 'UL', 'LL', 'LJ'};

% スキップしたファイル番号を記録するリスト
skipped_files = [];

% ファイルごとの処理
for file_num = first_file:last_file
    fprintf('Processing file: %d\n', file_num);

    % 入力データのフォルダとファイルパス
    edit_data_folder = sprintf('%dedit', data_date);
    ema_root_folder = sprintf('%dhf_poscsv_cut_0', data_date);
    ema_folder = sprintf('%03d', file_num);

    % 各部位のファイルパスを直接指定
    input_files = cellfun(@(pos) fullfile('sc.deal_data','..','..','edit', edit_data_folder, ema_root_folder, ema_folder, sprintf('%d_%s.csv', file_num, pos)), pos_list, 'UniformOutput', false);

    % 出力フォルダとファイルパス
    output_root_folder = sprintf('%dhf_poscsv_cut_0_opa', data_date);
    output_folder = sprintf('target_%d', target_date);
    output_dir = fullfile('sc.deal_data','..','..','edit', edit_data_folder, output_root_folder, output_folder, ema_folder);

    % 出力フォルダが存在しない場合は作成
    if ~exist(output_dir, 'dir')
        mkdir(output_dir);
    end

    % 各部位の出力ファイルパスを直接指定
    output_files = cellfun(@(pos) fullfile(output_dir, sprintf('%d_%s.csv', file_num, pos)), pos_list, 'UniformOutput', false);

    % 分析データ読み込み
    try
        original_data = cellfun(@readmatrix, input_files, 'UniformOutput', false);
    catch ME
        fprintf('Error reading input files for file_num: %d. Skipping...\n', file_num);
        disp(ME.message);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % サンプルごとのセットにして処理
    for i = 1:size(original_data{1}, 1)
        sample_shape = cell2mat(cellfun(@(data) data(i, 2:3), original_data, 'UniformOutput', false)');

        % Procrustes変換を適用
        opa_trans = sample_shape * transform2.T + transform2.c;

        % 変換後の値を更新
        for j = 1:length(pos_list)
            original_data{j}(i, 2:3) = opa_trans(j, :);
        end
    end

    % 更新した値を保存
    try
        cellfun(@writematrix, original_data, output_files);
    catch ME
        fprintf('Error writing output files for file_num: %d. Skipping...\n', file_num);
        disp(ME.message);
        skipped_files = [skipped_files, file_num];
        continue;
    end
end

% スキップしたファイル番号を表示
if ~isempty(skipped_files)
    fprintf('Skipped files: %s\n', num2str(skipped_files));
else
    fprintf('No files were skipped.\n');
end