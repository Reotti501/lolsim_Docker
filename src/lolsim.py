import os
import json
import tkinter as tk
from tkinter import ttk
from decimal import Decimal, ROUND_HALF_UP
import requests
import tarfile


def get_latest_version():
    response = requests.get(
        "https://ddragon.leagueoflegends.com/api/versions.json")
    if response.status_code == 200:
        versions = response.json()
        return versions[0]  # 最新のバージョンを取得
    else:
        raise Exception("Failed to get the latest version")


def download_and_extract_data(url, download_path, extract_path):
    if not os.path.exists(download_path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(download_path, 'wb') as file:
                file.write(response.raw.read())

            if download_path.endswith("tgz"):
                with tarfile.open(download_path, "r:gz") as tar:
                    tar.extractall(path=extract_path)
                print("Data extracted successfully.")
            else:
                print("The file is not a tar.gz file.")
        else:
            print(f"Failed to download the file. Status code: {
                  response.status_code}")
    else:
        print("The latest version is already downloaded.")
        # チェックしてディレクトリが存在しない場合再度展開
        if not os.path.exists(extract_path):
            with tarfile.open(download_path, "r:gz") as tar:
                tar.extractall(path=extract_path)
            print("Data re-extracted successfully.")


def get_champion_names(directory_path):
    champion_names = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            champion_name = os.path.splitext(filename)[0]
            champion_names.append(champion_name)
    return champion_names


def load_champion_data(directory_path):
    champion_data = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                json_content = json.load(file)
                champion_name = os.path.splitext(filename)[0]
                champion_data[champion_name] = json_content['data'][champion_name]
    return champion_data


def calculate_attackspeed():
    player1_champion_name = player1_combobox.get()
    player2_champion_name = player2_combobox.get()

    player1_level = int(player1_level_combobox.get())
    player2_level = int(player2_level_combobox.get())

    battle_duration = Decimal(battle_duration_combobox.get())

    if player1_champion_name not in champion_data or player2_champion_name not in champion_data:
        result_label["text"] = "チャンピオンが選択されていません"
        return

    player1_data = champion_data[player1_champion_name]
    player2_data = champion_data[player2_champion_name]

    player1_base_attackspeed = Decimal(player1_data['stats']['attackspeed'])
    player1_attackspeed_growth = Decimal(
        player1_data['stats']['attackspeedperlevel'])
    player1_attackspeed = player1_base_attackspeed + \
        player1_attackspeed_growth * (player1_level - 1)

    player2_base_attackspeed = Decimal(player2_data['stats']['attackspeed'])
    player2_attackspeed_growth = Decimal(
        player2_data['stats']['attackspeedperlevel'])
    player2_attackspeed = player2_base_attackspeed + \
        player2_attackspeed_growth * (player2_level - 1)

    player1_aa_count = (
        player1_attackspeed * battle_duration).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    player2_aa_count = (
        player2_attackspeed * battle_duration).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

    result_text = f"プレイヤー1チャンピオン名: {player1_data['name']}\n"
    result_text += f"  AA回数: {player1_aa_count}\n"
    result_text += f"  ステータス:\n"
    for key, value in player1_data['stats'].items():
        result_text += f"    {key}: {value}\n"

    result_text += f"\nプレイヤー2チャンピオン名: {player2_data['name']}\n"
    result_text += f"  AA回数: {player2_aa_count}\n"
    result_text += f"  ステータス:\n"
    for key, value in player2_data['stats'].items():
        result_text += f"    {key}: {value}\n"

    result_label["text"] = result_text


# 最新バージョンを取得
version = get_latest_version()

# URLとパスの設定
url = f"https://ddragon.leagueoflegends.com/cdn/dragontail-{version}.tgz"
download_path = f"D:\Desktop\LoL_1v1sim\Data_Dragon\dragontail-{version}.tgz"
extract_path = f"D:\Desktop\LoL_1v1sim\Data_Dragon"

# データのダウンロードと展開
download_and_extract_data(url, download_path, extract_path)

# チャンピオンデータのロード
directory_path = os.path.join(
    extract_path, version, "data", "ja_JP", "champion")
if not os.path.exists(directory_path):
    # ディレクトリが存在しない場合、データを再度展開
    with tarfile.open(download_path, "r:gz") as tar:
        tar.extractall(path=extract_path)

champion_data = load_champion_data(directory_path)
champion_names = list(champion_data.keys())

# ウィンドウの作成
root = tk.Tk()
root.title("1v1 Simulator")

# プレイヤー1と2のチャンピオン名のドロップダウンリスト
player1_label = ttk.Label(root, text="プレイヤー1のチャンピオン名:")
player1_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
player1_combobox = ttk.Combobox(root, values=champion_names, state="readonly")
player1_combobox.grid(row=0, column=1, padx=5, pady=5)

player2_label = ttk.Label(root, text="プレイヤー2のチャンピオン名:")
player2_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
player2_combobox = ttk.Combobox(root, values=champion_names, state="readonly")
player2_combobox.grid(row=1, column=1, padx=5, pady=5)

# プレイヤー1と2のレベルのドロップダウンリスト
level_values = list(range(1, 19))
level_label = ttk.Label(root, text="プレイヤー1のレベル:")
level_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
player1_level_combobox = ttk.Combobox(
    root, values=level_values, state="readonly")
player1_level_combobox.current(0)  # 初期値を1に設定
player1_level_combobox.grid(row=2, column=1, padx=5, pady=5)

level_label = ttk.Label(root, text="プレイヤー2のレベル:")
level_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
player2_level_combobox = ttk.Combobox(
    root, values=level_values, state="readonly")
player2_level_combobox.current(0)  # 初期値を1に設定
player2_level_combobox.grid(row=3, column=1, padx=5, pady=5)

# 戦闘時間の選択
battle_duration_label = ttk.Label(root, text="戦闘時間:")
battle_duration_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
battle_duration_combobox = ttk.Combobox(
    root, values=list(range(1, 61)), state="readonly")
battle_duration_combobox.current(0)  # 初期値を1に設定
battle_duration_combobox.grid(row=4, column=1, padx=5, pady=5)

# 計算ボタン
calculate_button = ttk.Button(root, text="計算", command=calculate_attackspeed)
calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# 結果表示ラベル
result_label = ttk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# ウィンドウの表示
root.mainloop()
