# PFoE_CartPole
Particle Filter on Episode で倒立振子を制御するための実験・評価用ROSパッケージ


## Requirement
このパッケージの動作には[OpenAI/Gym](https://github.com/openai/gym)とROSを必要とします。

## Installation
`catkin_ws/src`内にclone

## Usage
このパッケージ単独で実行する場合、以下のlaunchファイルを実行
```
$ roslaunch pfoe_cartpole pfoe_cartpole.launch
```
[MasakazuTamura/raspimouse_gamepad_teach_and_replay(Branch:cartpole)](https://github.com/MasakazuTamura/raspimouse_gamepad_teach_and_replay/tree/cartpole)と併用する場合、以下のlaunchファイルを実行
```
$ roslaunch raspimouse_gamepad_teach_and_replay teach_and_replay.launch
```

### 操作方法
`pfoe_cartpole.launch`を実行したターミナルで矢印キー等を用いて操作する
|入力|効果|
|→|右にCartを押す(1)|
|←|左にCartを押す(0)|
|ctrl+c|強制終了|
|ctrl+r|キーログ`key_cmd_list.txt`を再生|
|ctrl+s|操作履歴を`key_cmd_list.txt`として保存|
|ctrl+x|操作履歴をクリア|
- ただし、`key_cmd_list.txt`の保存場所は要編集

### モード変更
[MasakazuTamura/raspimouse_gamepad_teach_and_replay](https://github.com/MasakazuTamura/raspimouse_gamepad_teach_and_replay/tree/cartpole)との併用前提だが、本パッケージのみでも作動する  
以下のように、`/console`にいずれかの状態を送信することでモードを制御する
```
$ rosparam set /console teach
```
|入力|概要|
|wait|初期及び中継用の状態|
|teach|教示用の状態|
|replay|再生用の状態|
- `teach`から`replay`に変えるときは、`wait`を中継すること

### 特記事項
失敗条件はCartPole-v0準拠  
終了条件は、teachモード中は1000step超過または失敗条件を満たす、他は200step超過または失敗条件を満たす
