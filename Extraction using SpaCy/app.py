#import keyword
import spacy
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from string import punctuation

#from keyword import *
import subprocess
#subprocess.call("python -m spacy download en_core_web_sm",shell=True)

app = Flask(__name__, template_folder="template")
CORS(app)
nlp = spacy.load("en_core_web_sm")
print("Loaded language model")
def extraction(nlp, sequence, special_tags : list = None):
    
## Takes the input sequence with Spacy pretrained model.

## If any of the words are in special tags, the are added to the results.



    result = []

    ## We concentrate on pronoun, noun, adjective
    pos_tag = ['PROPN','NOUN','ADJ']

    ## object is created for the input
    doc = nlp(sequence.lower())


    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)
    
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))



@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route('/api/keywords', methods=['GET', 'POST'])
def get_keywords():

    if request.method == "POST":
        original_text = (request.form['taname'])
        tags = []        
        keywords = extraction(nlp,original_text,tags)

        keywordlisttostr = '\n'.join([keywords[0]] + ['{'+item+'}' for item in keywords[1:]])
        
        # keywordlisttostr = ' '.join(map(str, keywords))
        return keywordlisttostr
        

        # if 5<9:
        #     return render_template("results.html", keywordlisttostr= keywordlisttostr  )
        # else:
        #     return render_template("index.html")
    return render_template("results.html",keywordlisttostr= keywordlisttostr)


if __name__=='__main__':
	app.run(debug=True)