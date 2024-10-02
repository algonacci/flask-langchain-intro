from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()


@app.route("/")
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the Flask Langchain API"
        },
        "data": None,
    }), 200
    

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        input_data = request.get_json()
        language = input_data["language"]
        text = input_data["text"]
        
        system_template = "Translate the following into {language}:"

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                ("user", "{text}")
            ]
        )
        
        chain = prompt_template | model | parser
        
        result = chain.invoke({
            "language": language,
            "text": text,
        })
        
        return jsonify({
            "status": {
                "code": 200,
                "message": "Success translating",
            },
            "data": {
                "translation_result": result,
            }
        }), 200

        
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed!",
            },
            "data": None,
        }), 405
    
if __name__ == "__main__":
    app.run()