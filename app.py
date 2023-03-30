# Module imported here...
import tensorflow as tf
import numpy as np
import pandas as pd
from pathlib import Path
import os.path
from flask import Flask , render_template
from sklearn.model_selection import train_test_split
xyz="Hello meow"
# Flask integration 
app = Flask(__name__)
# Routing here
@app.route("/")
def main():
    return render_template('index.html')
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/test")
def test():
    return render_template('test.html')
@app.route("/blog")
def blog():
    def model():
        image_dir = Path('../../../Downloads/Fish_Dataset-20230329T114610Z-002/Fish_Dataset')
        # Get filepaths and labels
        filepaths = list(image_dir.glob(r'**/*.png'))
        labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))

        filepaths = pd.Series(filepaths, name='Filepath').astype(str)
        labels = pd.Series(labels, name='Label')

        # Concatenate filepaths and labels
        image_df = pd.concat([filepaths, labels], axis=1)

        # Drop GT images
        image_df['Label'] = image_df['Label'].apply(lambda x: np.NaN if x[-2:] == 'GT' else x)
        image_df = image_df.dropna(axis=0)

        # Sample 200 images from each class
        samples = []

        for category in image_df['Label'].unique():
            category_slice = image_df.query("Label == @category")
            samples.append(category_slice.sample(200, random_state=1))

        image_df = pd.concat(samples, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)
        image_df
        return render_template('blog.html',
                                    model=image_df,
                                )
if __name__ == "__main__":
    app.run(debug=True)