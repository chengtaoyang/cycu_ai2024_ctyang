from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 加載數據集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 切分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 特徵標準化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 創建SVM分類器實例，這裡使用預設的核函數（RBF核）
model = SVC(kernel='rbf', decision_function_shape='ovo')

# 訓練模型
model.fit(X_train, y_train)

# 進行預測
y_pred = model.predict(X_test)

# 計算準確率
accuracy = accuracy_score(y_test, y_pred)

print(f"預測準確率為: {accuracy:.2f}")
