# Titanic SVC Analysis (Hands-on Exercise 2)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df = pd.read_csv('titanic.csv')
print("Total Rows and Columns:", df.shape)
print("\nFirst 7 rows of the dataset:")
print(df.head(7))

print("\n--- Descriptive Statistics (Numerical Variables) ---")
print(df.describe())

num_vars = df.select_dtypes(include=[np.number]).columns.tolist()
cat_vars = df.select_dtypes(include=['object', 'string']).columns.tolist()

print("\nNumerical Variables:", num_vars)
print("Categorical Variables:", cat_vars)
print("\n--- Sex: Unique Values ---")
print(df['Sex'].unique())
print("\n--- Sex: Frequency Distribution ---")
print(df['Sex'].value_counts())
print("\n--- Pclass: Unique Values ---")
print(df['Pclass'].unique())
print("\n--- Pclass: Frequency Distribution ---")
print(df['Pclass'].value_counts())

print("\n--- Missing Values Count (Before Cleaning) ---")
print(df.isnull().sum())

df['Age'] = df['Age'].fillna(df['Age'].median())
df['Fare'] = df['Fare'].fillna(df['Fare'].median())

if 'Cabin' in df.columns:
    df['Cabin'] = df['Cabin'].fillna('Unknown')
if 'Embarked' in df.columns:
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

print("\n--- Missing Values Count (After Cleaning) ---")
print(df.isnull().sum())
print("\nAll missing values have been successfully handled.")

print("\nTarget (Dependent) Variable: Survived")
print("Independent Features: Pclass, Sex, Age, Fare")

le = LabelEncoder()
df['Sex_encoded'] = le.fit_transform(df['Sex'])
X = df[['Pclass', 'Sex_encoded', 'Age', 'Fare']]
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n--- Train-Test Split ---")
print("X_train shape:", X_train.shape)
print("X_test shape :", X_test.shape)

model = SVC(kernel='linear', random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

print("\n--- Model Evaluation ---")
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report (Precision, Recall, F1-Score):")
print(classification_report(y_test, y_pred))

plt.figure(figsize=(9, 4.5))
sns.countplot(data=df, x='Pclass', hue='Sex', palette='Set2')
plt.title('Passenger Count by Class and Gender')
plt.xlabel('Passenger Class')
plt.ylabel('Count')
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

g = sns.catplot(
    data=df, x='Pclass', hue='Sex', col='Survived',
    kind='count', height=4, aspect=0.9, palette='Set2'
)
g.fig.suptitle('Survival by Passenger Class and Gender', y=1.05)
plt.tight_layout()
plt.show()
plt.figure(figsize=(11, 4))
plt.subplot(1, 2, 1)
sns.histplot(df['Fare'], kde=True, color='steelblue')
plt.title('Fare Distribution (Histogram)')
plt.xlabel('Fare')
plt.subplot(1, 2, 2)
sns.boxplot(y=df['Fare'], color='orange')
plt.title('Fare Distribution (Boxplot)')
plt.ylabel('Fare')
plt.tight_layout()
plt.show()
plt.figure(figsize=(8, 4.5))
sns.countplot(data=df, x='Sex', hue='Survived', palette=['#4C72B0', '#DD8452'])
plt.title('Survival vs Non-Survival by Gender')
plt.xlabel('Gender')
plt.ylabel('Passenger Count')
plt.legend(title='Survived', labels=['No (0)', 'Yes (1)'])
plt.tight_layout()
plt.show()
print("Observation: Fare is highly right-skewed with many extreme high values (outliers).")
print("Observation: Female passengers had a clearly higher survival rate than male passengers.")