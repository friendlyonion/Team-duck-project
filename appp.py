# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, jsonify, request

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.tt
@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'GET':
        return render_template('index.html')  # Render the form template
    else:
        data = request.form['translate-one']  # Access form data
        api_response = translate(data)  # Await the API call
        return jsonify({"data":api_response})  # Return JSON response for AJAX

from openai import OpenAI
import csv
def translate(x):
    client = OpenAI()
    translation_string = ''
    with open('mexican.csv') as f:
        translations = csv.reader(f)
        for row in translations:
            translation_string = translation_string + str(row)
    statement = "Translate this statement {translate_this} using this dictionary formatted in ['spanish word', 'slang translation'] make sure the final result is in english. Account for Mexican slang{dictionary}. Use common sense in the translation. Things that dont sound right are probably not right. Such as passing an animal to another person".format(translate_this=x, dictionary = translation_string)
    print(statement)
    completion =  client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a professional translater"},
        {"role": "user", "content": statement+". Make sure that you only reply with the translation, nothing extra."}
      ]
    )
    return completion.choices[0].message.content
# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
