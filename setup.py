from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
import os

app = Flask(__name__)

# Ensure the output directory exists within the static folder
output_dir = os.path.join(app.static_folder, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        language = request.form.get('language')

        # Generate speech if text is available
        if text:
            gtts_object = gTTS(text=text, lang=language, slow=False)
            filename = "output.mp3"
            filepath = os.path.join(output_dir, filename)
            gtts_object.save(filepath)

            # Redirect to result page after processing
            return redirect(url_for('result'))

    # Render initial form page
    return render_template('index.html')

@app.route('/result')
def result():
    # Render the result page where you display the generated audio or other results
    audio_url = url_for('static', filename=f'output/output.mp3')
    return render_template('result.html', audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True)
