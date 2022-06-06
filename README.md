# DSAI-HW3-2022
##  Execution
```
$ pipenv install
$ pipenv run python main.py
```
## Introduction
### input data 
- consumption.csv: 過去七天歷史用電資料
- generation.csv: 過去七天產電資料
- bidresult.csv: 過去七天自己的投標資料
### output data 
- output.csv: 未來一天投標資訊### Workflow
### Workflow
![](https://i.imgur.com/Ng0gG6U.png)
1. 平台會指定過去七天資料做為參數放進 Agents 程式中
2. Agents 產出未來一天投標資訊（以小時為單位），並可透過參數指定輸出路徑
3. 平台取得所有 Agents 的投標資訊，並進行媒合
4. 平台公告結果並將競標結果寫到各個 Agents 的目錄
### Matching Mechanism
![](https://i.imgur.com/2PWfZ2K.png)
![](https://i.imgur.com/FUpUqch.png)
### 電費計算方式
![](https://i.imgur.com/ZrcQF7D.png)
## Strategy
### Model
- Multilayer Perceptron (MLP) Model
- 分為預測 consumption 及預測 generation 兩個 model
### Bidding
- 買入價設 2.47（低於台電定價 2.52，可買進）
- 賣出價設 2.57（高於台電定價 2.52，可賣出）
## 補充
- 在 ftp 上無法上傳檔案，故在此進行記錄
## Others
### Source
  - [Slide](https://docs.google.com/presentation/d/1ZwXe4xMflCxiDQ7RK6z_LH88r0Dp38sQ/edit#slide=id.gd2c4f7e262_1_24)
  - [Dashboard](https://docs.google.com/spreadsheets/d/1hqoxG48A159buQ-GuoU7Fo-QrGKYmE1DFgPckJR0dFI/edit#gid=0)
### Rules

- SFTP

```

┣━ upload/
┗━ download/
   ┣━ information/
   ┃  ┗━ info-{mid}.csv
   ┣━ student/
   ┃  ┗━ {student_id}/
   ┃     ┣━ bill-{mid}.csv
   ┃     ┗━ bidresult-{mid}.csv
   ┗━ training_data/
      ┗━ target{household}.csv  
      
```

1. `mid` 為每次媒合編號
2. `household` 為住戶編號，共 50 組
3. 請使用發給組長的帳號密碼，將檔案上傳至 `upload/`
4. 相關媒合及投標資訊皆在 `download/` 下可以找到，可自行下載使用


- File

```

┗━ {student_id}-{version}.zip
   ┗━ {student_id}-{version}/
      ┣━ Pipfile
      ┣━ Pipfile.lock
      ┣━ main.py
      ┗━ {model_name}.hdf5

```

1. 請務必遵守上述的架構進行上傳 (model 不一定要有)
2. 檔案壓縮請使用 `zip`，套件管理請使用 `pipenv`，python 版本請使用 `3.8`
3. 檔名：{學號}-{版本號}.zip，例：`E11111111-v1.zip`
4. 兩人一組請以組長學號上傳
5. 傳新檔案時請往上加版本號，程式會自動讀取最大版本
6. 請儲存您的模型，不要重新訓練

- Bidding

1. 所有輸入輸出的 csv 皆包含 header
2. 請注意輸入的 `bidresult` 資料初始值為空
3. 輸出時間格式為 `%Y-%m-%d %H:%M:%S` ，請利用三份輸入的 data 自行選一份，往後加一天即為輸出時間  
   例如: 輸入 `2018-08-25 00:00:00 ~ 2018-08-31 23:00:00` 的資料，請輸出 `2018-09-01 00:00:00 ~ 2018-09-01 23:00:00` 的資料(一次輸出`一天`，每筆單位`一小時`)
4. 程式每次執行只有 `120 秒`，請控制好您的檔案執行時間
5. 每天的交易量限制 `100 筆`，只要有超出會全部交易失敗，請控制輸出數量
