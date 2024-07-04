from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from gtts import gTTS
import os
import mysql.connector

app = Flask(__name__)

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhara77@9504",
    database="Texttoaudio"
)
cursor = db.cursor()

# Ensure the output directory exists within the static folder
output_dir = os.path.join(app.static_folder, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        language = request.form.get('language')

        # Check if a file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                text = file.read().decode('utf-8')

        # Generate speech if text is available
        if text:
            gtts_object = gTTS(text=text, lang=language, slow=False)
            filename = "output.mp3"
            filepath = os.path.join(output_dir, filename)
            gtts_object.save(filepath)

            # Save to MySQL
            cursor.execute("INSERT INTO text (text, language) VALUES (%s, %s)", (text, language))
            db.commit()

            # Redirect to result page
            return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    # Render the result page where you display the generated audio or other results
    audio_url = url_for('static', filename='output/output.mp3')
    return render_template('result.html', audio_url=audio_url)

if __name__ == "__main__":
    app.run(debug=True)
