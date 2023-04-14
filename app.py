from flask import Flask, request, render_template,jsonify
import os
import openai

app = Flask(__name__,template_folder='templates')
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chatai():
    if request.method == "POST":
        message = request.form.get("message")

        # Call OpenAI API to generate response
        completion = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Conversation with ChatGPT:\nUser: {message}\nChatGPT:",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        response = completion.choices[0].text.strip()

        return response

    return render_template("chat.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Get text from user input
        input_text = request.form.get("input_text")

        # Call OpenAI Edit API
        edit = openai.Edit.create(
            model="text-davinci-edit-001",
            input=input_text,
            instruction="Fix the spelling mistakes"
        )

        # Get corrected text from API response
        corrected_text = edit.choices[0].text

        # Render template with corrected text
        return render_template("edit.html", corrected_text=corrected_text)

    return render_template("edit.html")

@app.route("/completions", methods=["GET", "POST"])
def completions():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        max_tokens = int(request.form.get("max_tokens"))
        temperature = float(request.form.get("temperature"))

        # Call OpenAI Completions API
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Get text from API response
        text = completion.choices[0].text

        return render_template("completions.html", text=text)

    return render_template("completions.html")


@app.route('/image', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return jsonify(image.data)
    return render_template('images.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
