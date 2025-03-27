import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load data from CSV file
file_path = "/Users/yoshiyukiiguchi/Desktop/mads_semestre1/nosql/project/proteins_with_go_annotations.csv"  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Ensure the go_annotations column is properly formatted as lists
df["go_annotations"] = df["go_annotations"].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Convert go_annotations list into a single string for vectorization
df["go_annotations_str"] = df["go_annotations"].apply(lambda x: " ".join(x))

# Prepare features (GO annotations) and labels (EC numbers)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["go_annotations_str"])
y = df["ec"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# Optional: Feature importance
feature_importances = model.feature_importances_
feature_names = vectorizer.get_feature_names_out()
important_features = sorted(zip(feature_importances, feature_names), reverse=True)[:10]
print("Top 10 important features:")
for score, feature in important_features:
    print(f"{feature}: {score:.4f}")
