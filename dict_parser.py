import re,itertools,time
# import stanza # if you want to use the stanza tokenizer

# split a text into paragraphs based on double line breaks
def graph_tokenizer(text):
    return text.split("\n\n")

# break into sentences 
def sent_tokenizer(text):
    return re.split(r'[。？！\．]', text)

# break into phrases (there is some duplication)
def phrase_tokenizer(text):
    return re.split(r'[。？！；：；、，「」『』《》 *  ()○]', text)

# flatten a two-layer list into a single layer list
def flatten(input_list):
    new_list = list(itertools.chain(*input_list))
    return [l for l in new_list if l != ""]

# remove unnecessary content. This is based on texts found in the kanseki 
# repository
def clean_up(text):
    # remove structural markup
    text = re.sub(r'<.+?>', '', text)
    # remove commented lines
    text = re.sub(r'#.+', '', text)
    # remove other characters
    rem = ["\u3000", '\n', '¶']
    for r in rem:
        text = text.replace(r, '')
    return text

# provide a filename for the input text:
filename = 'KR6a0001.txt'

# provide a filename for the dictionary (code assumes one chinese term per line)
vocabulary_file = 'dictionary_terms.txt'

# instantiate tokenzier if using stanz. if you prefer you can just assume 
# characters not in your dictionary are single words, as I have done here
# nlp = stanza.Pipeline('zh-hant', processors='tokenize', use_gpu=True)

# open your dictionary (in my case this is just a plain text)
with open(vocabulary_file, 'r', encoding='utf8') as rf:
    vocab = list(set(rf.read().split("\n")))

# sort the vocabulary by length, to prioritize long terms
vocab = sorted(vocab, key=len, reverse=True)
# filter out any blank entries
vocab = [v for v in vocab if v != ""]

# compile the regular expression to match any given vocabulary word, capturing 
# the result
my_regex = re.compile("("+("|").join(vocab)+")")

# start a timer (not necessary, just for curiosity's sake)
st=time.time()

# open the file to tokenize
with open(filename) as rf:
    text = rf.read()

# Here I reduce the document into individual paragraphs. this is not necessary
# stricktly speaking, but helps when working with long texts
paragraphs = graph_tokenizer(text)

# Clean the paragraphs and then find the dictionary words, marking up with <w>
# tags
paragraphs = [my_regex.sub(r'<w>\1</w>', clean_up(p)) for p in paragraphs]

# Break into sentences. Another step that is not super necessary, but results
# in a nice output (sentences divided into words)
sentences = [sent_tokenizer(p) for p in paragraphs]

# flatten the list from a list of paragraphs, each of which is a list of sentences
# to just a list of sentences
sentences = flatten(sentences)

# remove any sentence that has no words in it
sentences = [s for s in sentences if s != ""]

# create an empty list to contianed the parsed output
parsed = []

# iterate through each sentence and parse it as necessary
for sentence in sentences:

    # keep track of words in the current sentence
    temp_parse = []

    # futher reduce the text into phrases, as words will not cross phrase boundaries
    for phrase in phrase_tokenizer(sentence):

        # keep track of the words in the current phrase
        temp_words = []
        
        # find the first marked up word
        word_start = phrase.find("<w>")

        # as long as there are still marked up words, keep searching
        while word_start != -1:
            # if an identified word is at the beginning of the paragraph then append it to
            # the parsed list
            if word_start == 0:
                word_end = phrase.find("</w>")
                temp_words.append(phrase[word_start+3:word_end])
                # move the text forward past the marked-up word
                phrase =phrase[word_end+4:]
            else:
                # specify the chunk up to the next identified word
                chunk = phrase[:word_start]
                # if the chunk is just one character, then append it to the list
                if len(chunk) == 1:
                    temp_words.append(chunk)
                # otherwise, use the alternative parser method and EXTEND the list 
                # assuming the alternative parser returns a list of words
                else:
                    temp_words.extend(list(chunk))
                    # alternatively you could switch this for:
                    #temp_words.extend([w.text for w in nlp(chunk).sentences[0].words])
                    
                # move the text up to the next identified word
                phrase = phrase[word_start:]
            # search for the next identified word. Once there are no more words,
            # you will exit out of the while loop.
            word_start = phrase.find("<w>")

        # there is a possiblity that there are no more marked up words, but still 
        # untokenized text!

        # check if there is remaining text
        remaining = len(phrase)

        # if there is remaining text, then parse it
        if remaining > 0:
            # if it is just one character save it
            if remaining == 1:
                temp_words.append(phrase)
            # otherwise, use a parser to extend the list
            else:
                temp_words.extend(list(phrase))
                # alternatively you could switch this for:
                #temp_words.extend([w.text for w in nlp(phrase).sentences[0].words])
        temp_parse.extend(temp_words)
    
    # as long as there are words in the temp_parse list, then append it to the
    # parsed list
    if len(temp_parse) > 0:
        parsed.append(temp_parse)    

# print the first ten sentences
print(parsed[:10])

# finish the timer:
et = time.time()
print(f"This operation took {et-st:.2f} seconds")