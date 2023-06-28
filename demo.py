import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, request, jsonify

def main_function(lyrics):
    # dividing to each sentence
    print("lyrics", lyrics)
    paragraphs = lyrics.split("\n")
    
    # dividing to each individual words in sentence
    store_2 = []
    for paragraph in paragraphs:
        divided_words = word_tokenize(paragraph)
        store_2.append(divided_words)

    # tagging each word with their respective POS
    store_3 = []
    for list_a in store_2:
        pos_words = nltk.pos_tag(list_a)
        store_3.append(pos_words)

    # extracting the line which has more nouns
    def count_nouns(sublist):
        noun_count = 0
        for word, pos in sublist:
            if pos.startswith('NN'):
                noun_count += 1
        return noun_count

    def extract_sublist_with_most_nouns(list_of_lists):
        max_noun_count = 0
        sublist_with_most_nouns = []
        for i, sublist in enumerate(list_of_lists):
            noun_count = count_nouns(sublist)
            if noun_count > max_noun_count:
                max_noun_count = noun_count
                sublist_with_most_nouns = sublist
                index = i
        return sublist_with_most_nouns, index

    paragraph_with_more_nouns, index = extract_sublist_with_most_nouns(store_3)
    sentence_from_lyrics_which_has_more_nouns = paragraphs[index]

    replaced_sentence = ""
    for word, pos in paragraph_with_more_nouns:
        if pos.startswith('NN'):
            replaced_sentence = sentence_from_lyrics_which_has_more_nouns.replace(word, "________")
    print("Replaced Sentence:", replaced_sentence)
    return replaced_sentence


app = Flask(__name__)



@app.route('/lyrics', methods=['POST'])
def process_lyrics():
    data = request.get_json()

    lyrics = data.get('lyrics')  # Corrected: Access 'lyrics' as a string
    
    replaced_sentence = main_function(lyrics)

    response = {
        'replaced_sentence': replaced_sentence
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run()
