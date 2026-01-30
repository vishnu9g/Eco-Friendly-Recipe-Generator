from flask import Flask, render_template, request
import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("models/gemini-flash-latest")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/generate", methods=["POST"])
def generate():
    ingredients = request.form.get("user_input")

    prompt = f"""
    You are an eco-friendly chef.

    Using these ingredients: {ingredients}

    1. Generate a healthy, eco-friendly recipe.
    2. Provide cooking steps.
    3. Include 1–2 sustainability tips.
    4. Estimate approximate carbon footprint.

    IMPORTANT: 
    - Format the output in **HTML tables and lists** exactly like this example:

    SECTION A: Recipe
    - Recipe title (h2)
    - Ingredients in table
    - Cooking steps in ordered list
    - Sustainability tips in <ul>

    SECTION B: Carbon Footprint
    - Use a table with columns: Component, Estimated CO₂e (kg)
    """

    response = model.generate_content(prompt)
    full_text = response.text

    try:
        recipe_html = full_text.split("SECTION B:")[0].replace("SECTION A:", "").strip()
        carbon_html = full_text.split("SECTION B:")[1].strip()
    except:
        recipe_html = full_text
        carbon_html = "<p>Carbon footprint data not available.</p>"

    return render_template(
        "final.html",
        recipe=recipe_html,
        carbon=carbon_html
    )

if __name__ == "__main__":
    app.run(debug=True)

