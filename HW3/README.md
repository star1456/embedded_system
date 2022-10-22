於手機裝ble scanner之類的App
設service <fff0>，characteristic <fff1>，properties為notify、read
跑ble scanner，並記下裝置名
跑ble_scan_connect.py，尋找列表中是否有裝置，輸入編號
程式會修改CCCD，使能夠接收notification，若實驗成功，會印出<fff1>的read value，若失敗則會印出失敗訊息
