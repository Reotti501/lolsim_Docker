# [League of Legends (LoL)](https://www.leagueoflegends.com/ja-jp/) の1v1シミュレータ
## はじめに
LoLで1v1をしたとき理論的に最強チャンピオンを知りたくて作り始めました。

まだまだ作りかけなので、まったく使い物になりません。(´・ω・`)
詳しい方や何か情報やアイディアがある方は是非教えてください。

## 開発環境や実行環境など
### 開発環境
* windows 11
* Docker
* python3.12.4

### 実行環境
* windows側に`lolsim_Docker`を置いておいてください

## ファイル説明
 | /.devcontainer      |                          |
 |---------------------|--------------------------|
 | [devcontainer.json](/.devcontainer/devcontainer.json) | dockerの環境ファイル      |
 | [Dockerfile](/.devcontainer/Dockerfile)        | dockerファイル      |
 | [requirements.txt](/.devcontainer/requirements.txt)  | pipインストールするライブラリを書くと、docker起動時にインストールしてくれます      |


 | /other      |                          |
 |---------------------|--------------------------|
 | [LoL1v1sim レイアウト.png](/other/LoL1v1sim%20レイアウト.png) | レイアウトの予定です（確定ではないです）      |
 | [ver 14.9.1 - シート1.csv](/other/ver%2014.9.1%20-%20シート1.csv)        | 1Lv毎のHP増加量を調べるために集めたデータです      |

 | /src         |                      |
 |--------------|----------------------|
 | [lolsim.py](/src/lolsim.py)  | ソースファイルです     |      


実行すると`lolsim_Docker`内に現在のライブ環境バージョンの[Data Dragon](https://developer.riotgames.com/docs/lol)がダウンロードされます。

初回起動時や最新バージョンの[Data Dragon](https://developer.riotgames.com/docs/lol)がダウンロードされていない場合、非常に時間がかかります。（SSD環境でも10分くらいかかります。）

Data Dragonを削除しなければダウンロードしたファイルから読み出すだけなので短時間で起動できます。

## 現状と実装予定
ルーンやアイテムなどゲームを同じ状態で計算ができるようにしていきたいと考えています。

1Lv毎のHP増加量がわからないため、現状まったく役に立ちません。

理解しにくいと思うのでリポジトリに[ver 14.9.1 - シート1.csv](/other/ver%2014.9.1%20-%20シート1.csv)としてデータを載せておきます。

ただ、バージョン`14.9`時点のデータなので細かく確認したい方は[__Data Dragon ver 14.9__](https://ddragon.leagueoflegends.com/cdn/dragontail-14.12.1.tgz)ここからダウンロードして確認してください。
