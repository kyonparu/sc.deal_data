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

% スキップしたファイル番号と存在しなかったファイルを記録するリスト
skipped_files = [];
missing_files = {}; % {file_num, 部位名}の形式で記録

% 各部位の平均値を保存する変数の初期化
mean_target = initialize_mean_matrix(last_file, pos_list);
mean_original = initialize_mean_matrix(last_file, pos_list);

% ファイルごとの処理
for file_num = first_file:last_file
    fprintf('Processing file: %d\n', file_num);

    % 入力データのパスを生成
    [input_paths, target_paths] = generate_input_paths(data_date, target_date, file_num, pos_list);

    % 出力データのパスを生成
    output_paths = generate_output_paths(data_date, target_date, file_num, pos_list);

    % 出力ディレクトリの作成（ここに残す）
    output_dir = fileparts(output_paths.T1); % 任意の部位のパスからディレクトリを取得
    if ~exist(output_dir, 'dir')
        mkdir(output_dir);
        fprintf('Created output directory: %s\n', output_dir);
    end

    % ファイルの存在確認
    file_exists = true;
    for i = 1:length(pos_list)
        if ~exist(input_paths.(pos_list{i}), 'file')
            fprintf('File not found: %s\n', input_paths.(pos_list{i}));
            missing_files{end+1} = {file_num, pos_list{i}}; % 存在しないファイルを記録
            file_exists = false;
        end
    end

    % ファイルが存在しない場合はスキップ
    if ~file_exists
        fprintf('Skipping file_num: %d due to missing files.\n', file_num);
        skipped_files = [skipped_files, file_num];
        continue;
    end

    % データの読み込みと平均値の計算
    try
        [original_data, target_data] = read_data(input_paths, target_paths, pos_list);
        mean_target = calculate_mean(target_data, mean_target, file_num, pos_list);
        mean_original = calculate_mean(original_data, mean_original, file_num, pos_list);
    catch ME
        fprintf('Error processing file_num: %d. Skipping...\n', file_num);
        disp(ME.message);
        skipped_files = [skipped_files, file_num];
        continue;
    end
end

% 全体の平均値を計算
all_target_mean = calculate_overall_mean(mean_target, pos_list);
all_original_mean = calculate_overall_mean(mean_original, pos_list);

% プロクルステス変換の計算
[d2, opa2, transform2] = procrustes(all_target_mean, all_original_mean, 'scaling', false);
fprintf('Procrustes transformation parameters calculated.\n');

% 変換後のデータを保存
for file_num = first_file:last_file
    fprintf('Applying transformation for file: %d\n', file_num);

    % 入力データのパスを生成
    [input_paths, ~] = generate_input_paths(data_date, target_date, file_num, pos_list);

    % 出力データのパスを生成
    output_paths = generate_output_paths(data_date, target_date, file_num, pos_list);

    % データの変換
    try
        % データを再読み込み
        original_data = read_data_single(input_paths, pos_list);

        % サンプルごとのセットにして処理
        for i = 1:size(original_data.T1, 1)
            sample_shape = [
                original_data.T1(i, 2:3);
                original_data.T2(i, 2:3);
                original_data.T3(i, 2:3);
                original_data.UL(i, 2:3);
                original_data.LL(i, 2:3);
                original_data.LJ(i, 2:3)
            ];

            % Procrustes変換を適用
            opa_trans = sample_shape * transform2.T + transform2.c;

            % 変換後の値を更新
            original_data.T1(i, 2:3) = opa_trans(1, :);
            original_data.T2(i, 2:3) = opa_trans(2, :);
            original_data.T3(i, 2:3) = opa_trans(3, :);
            original_data.UL(i, 2:3) = opa_trans(4, :);
            original_data.LL(i, 2:3) = opa_trans(5, :);
            original_data.LJ(i, 2:3) = opa_trans(6, :);
        end

        % 変換後のデータを保存
        save_transformed_data(original_data, output_paths, pos_list);
    catch ME
        fprintf('Error transforming file_num: %d. Skipping...\n', file_num);
        disp(ME.message);
        skipped_files = [skipped_files, file_num];
        continue;
    end
end

% スキップしたファイル番号と存在しなかったファイルを表示
if ~isempty(skipped_files)
    fprintf('Skipped file numbers: %s\n', num2str(skipped_files));
end

if ~isempty(missing_files)
    fprintf('Missing files:\n');
    for i = 1:length(missing_files)
        fprintf('File_num: %d, Part: %s\n', missing_files{i}{1}, missing_files{i}{2});
    end
else
    fprintf('No missing files.\n');
end

fprintf('Processing completed.\n');

% 関数: 平均値を保存する行列を初期化
function mean_matrix = initialize_mean_matrix(num_files, pos_list)
    mean_matrix = struct();
    for i = 1:length(pos_list)
        mean_matrix.(pos_list{i}) = zeros(num_files, 2);
    end
end

% 関数: 入力データのパスを生成
function [input_paths, target_paths] = generate_input_paths(data_date, target_date, file_num, pos_list)
    edit_data_folder = sprintf('%dedit', data_date);
    ema_root_folder = sprintf('%dhf_poscsv_cut_0', data_date);
    ema_folder = sprintf('%03d', file_num);

    target_data_folder = sprintf('%dedit', target_date);
    target_root_folder = sprintf('%dlpf_hf_poscsv_cut_sp_0', target_date);
    target_folder = sprintf('%03d', file_num);

    input_paths = struct();
    target_paths = struct();
    for i = 1:length(pos_list)
        input_paths.(pos_list{i}) = fullfile('sc.deal_data', '..', 'edit', edit_data_folder, ema_root_folder, ema_folder, sprintf('%d_%s.csv', file_num, pos_list{i}));
        target_paths.(pos_list{i}) = fullfile('sc.deal_data', '..', 'edit', target_data_folder, target_root_folder, target_folder, sprintf('%d_%s.csv', file_num, pos_list{i}));
    end
end

% 関数: 出力データのパスを生成
function output_paths = generate_output_paths(data_date, target_date, file_num, pos_list)
    edit_data_folder = sprintf('%dedit', data_date);
    output_root_folder = sprintf('%dhf_poscsv_cut_0_opa', data_date);
    output_folder = sprintf('target_%d', target_date);
    ema_folder = sprintf('%03d', file_num);

    output_paths = struct();
    for i = 1:length(pos_list)
        output_paths.(pos_list{i}) = fullfile('D:\ikeda_data\DNN_exp\edit', edit_data_folder, output_root_folder, output_folder, ema_folder, sprintf('%d_%s.csv', file_num, pos_list{i}));
    end
end

% 関数: データを読み込む
function [original_data, target_data] = read_data(input_paths, target_paths, pos_list)
    original_data = struct();
    target_data = struct();
    for i = 1:length(pos_list)
        original_data.(pos_list{i}) = readmatrix(input_paths.(pos_list{i}));
        target_data.(pos_list{i}) = readmatrix(target_paths.(pos_list{i}));
    end
end

% 関数: 平均値を計算
function mean_matrix = calculate_mean(data, mean_matrix, file_num, pos_list)
    for i = 1:length(pos_list)
        mean_matrix.(pos_list{i})(file_num, :) = mean(data.(pos_list{i})(:, 2:3), 1);
    end
end

% 関数: 全体の平均値を計算
function overall_mean = calculate_overall_mean(mean_matrix, pos_list)
    overall_mean = zeros(length(pos_list), 2);
    for i = 1:length(pos_list)
        overall_mean(i, :) = mean(mean_matrix.(pos_list{i}), 1);
    end
end

% 関数: データを1回読み込む
function data = read_data_single(input_paths, pos_list)
    data = struct();
    for i = 1:length(pos_list)
        data.(pos_list{i}) = readmatrix(input_paths.(pos_list{i}));
    end
end

% 関数: 変換を適用
function transformed_data = apply_transformation(data, transform, pos_list)
    transformed_data = struct();
    for i = 1:length(pos_list)
        transformed_data.(pos_list{i}) = data.(pos_list{i});
        for j = 1:size(data.(pos_list{i}), 1)
            sample_shape = data.(pos_list{i})(j, 2:3);
            transformed_shape = sample_shape * transform.T + transform.c;
            transformed_data.(pos_list{i})(j, 2:3) = transformed_shape;
        end
    end
end

% 関数: 変換後のデータを保存
function save_transformed_data(data, output_paths, pos_list)
    for i = 1:length(pos_list)
        writematrix(data.(pos_list{i}), output_paths.(pos_list{i}));
    end
end
