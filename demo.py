import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, request, jsonify



import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify

app = Flask(__name__)

def main_function(lyrics):
    paragraphs = lyrics.split("\n")
    replaced_sentences = []
    non_replaced_sentences= []
    
    # dividing each sentence into individual words
    store_2 = []
    for paragraph in paragraphs:
        divided_words = word_tokenize(paragraph)
        store_2.append(divided_words)

    # tagging each word with their respective POS
    store_3 = []
    for list_a in store_2:
        pos_words = nltk.pos_tag(list_a)
        store_3.append(pos_words)
    print(store_3)

    # extracting the lines which have more nouns
    def count_nouns(sublist):
        noun_count = 0
        for word, pos in sublist:
            if pos.startswith('NN'):
                noun_count += 1
        return noun_count
    
    def extract_sublist_with_most_nouns(list_of_lists):
        for i, sublist in enumerate(list_of_lists):
            noun_count = count_nouns(sublist)
            replaced_sentence = ''
            if noun_count >= 2:
                sentence_from_lyrics_which_has_more_nouns = paragraphs[i]
                non_replaced_sentences.append(sentence_from_lyrics_which_has_more_nouns)
                for word, pos in sublist:
                    if pos.startswith('NN'):
                        replaced_sentence = sentence_from_lyrics_which_has_more_nouns.replace(word, "________")
                        replaced_sentences.append(replaced_sentence)
                        break
        
    extract_sublist_with_most_nouns(store_3)
    print(replaced_sentences)
    return replaced_sentences, non_replaced_sentences


@app.route('/lyrics', methods=['POST'])
def process_lyrics():
    data = request.get_json()
    lyrics = data.get('lyrics')
    
    result1, result2 = main_function(lyrics)

    response = {
        'replaced_sentences': result1,
        "non_replaced_sentences":result2
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)



