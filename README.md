#  Project for the ML course (A.Y. 2021/2022)

## Objective
Build a complete ML-based Android malware detection system, that: 
- Takes as input a training set of apks
- Extracts features from them
- Trains and saves a classifier and the selected features
- Extracts features from test apks, load the saved model and classifies them
- Finally, report metrics (e.g. accuracy, ROC curve) to evaluate the performance of the system.

### Dataset 
You can download some apks from [here](https://drive.google.com/drive/folders/1-Lc3_8w6KDLPEK4Tuv1kXIKVAfn8P0lf?usp=sharing)

### Feature extraction
You can use the provided tool to extract DREBIN features.

Ensure your environment includes dependencies for the tool, in particular that you have a copy of the AAPT (Android Asset Packaging Tool) and that everything is set up correctly in the tool's settings.py file.

The main code is contained in staticAnalyzer.py and can also be launched from drebin.py file. Note that you also have to create a file containing the labels of apks (0 for goodware, 1 for malware).

Example of features and labels files (in json format):
```json
[{"app_permissions::name='android_permission_WRITE_MEDIA_STORAGE'":1,"urls::http:\/\/openmobile_qq_com\/api\/check2?":1, "api_calls::android\/bluetooth\/BluetoothAdapter;->getAddress":1},{"api_calls::android\/content\/ContentResolver;->openInputStream":1,"api_permissions::android_permission_INTERNET":1,"interesting_calls::Obfuscation(Base64)":1,"app_permissions::name='android_permission_WRITE_EXTERNAL_STORAGE'":1},{"urls::http:\/\/oc_umeng_co\/check_config_update":1,"app_permissions::name='com_android_launcher_permission_INSTALL_SHORTCUT'":1,"interesting_calls::getNetworkCountryIso":1,"api_permissions::android_permission_INTERNET":1,"intents::android_intent_action_MAIN":1}]
[0,1,0]
```

### Training and Classification

Refer to DREBIN paper [1] for the implementation of the linear classifier.
You can split the dataset in two parts (e.g. 80/20%) to obtain training and test set.
Note that you can also reduce the number of features by performing L1 or L2 penalty feature selection.

[1] Arp, D., Spreitzenbarth, M., Hubner, M., Gascon, H., & Rieck, K. (2014). DREBIN: Effective and Explainable Detection of Android Malware in Your Pocket. NDSS.
