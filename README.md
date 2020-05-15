# A Simple Dictionary-Based Tokenizer for Classical Chinese Text
This repository contains a python script that uses a dictionary to create a regular expression that identify words within a document, giving preference to longer terms. Any set of characters within the document not within the dictionary can be segmented however you choose: you can simply treat each character as a word, or you can use one of the many word segmenters available. I have set this up to use Stanford's stanza library, but you could also use Jieba or something similar.

## Instructions for use
This script depends on a dictionary file (which I've included here as "dictionary_terms.txt"), which is simply a plain-text file with a single term on a line by itself. CAUTION: Be absolutely sure your dictionary does not contain any terms that might be interpreted as a regular expression! If it does, the script will break.

Place the file you want to tokenize in the same folder as the script and the dictionary file. Specify the appropriate filenames within the script and then you ready to go! Simply navigate to the folder in your terminal and run the code.

If you want to take advantage of the stanza parser, you will need to install it via pip and then download the Chinese tokenization module (stanza.download('zh-hant')). Note that Stanza does have a classical Chinese segementer, but it is trained on extremely old texts and tends to tokenize into individual characters (as one might expect on a model trained early Chinese writing). But you can simply switch ot "zh-hant" here (and in the nlp object instantiation) with "lzh". You will need to uncomment the import statement, the line instantiating the model, and then uncomment 

temp_words.extend([w.text for w in nlp(chunk).sentences[0].words]) and

temp_words.extend([w.text for w in nlp(phrase).sentences[0].words])

and comment out

temp_words.extend(list(chunk)) and

temp_words.extend(list(phrase))

This duplication will be refactored out later, but I just hacked this together, so apologies for that!


## A few quick notes
The bigger your dictionary, the slower the code will run, but the more accurate it will be! The demo setup I have here contains a relatively small dictionary of about 1400 terms. Parsing the sample text (which is around 300,000 characters, or about half the length of the Romance of the Three Kingdoms) into individual characters takes around .45 seconds on my (relatively fast) computer. When using the stanza parser this shoots up to about 175 seconds. 

With a much more extensive dictionary of around 90k, parsing the same text (and turning unknown sequences into individual characters) takes about 28 seconds. Using the stanza parser, however, only increases the time to 30 seconds (resulting in a pretty good final product) as there is much less text to chew through.

Some of the behavior in this script is based on the format of Kanseki Repository documents and may need some editing to completely work with your input texts.

## Input data info
The demo text comes from Christian Wittern's Kanskei Repository, and is the first text in the Buddhist text section:
https://www.kanripo.org/text/KR6a0001/
This is available via a [CC BY SA](http://creativecommons.org/licenses/by-sa/4.0/) License.

The demo dictionary is adapted from William Edward Soothill and Lewis Hodous's "Dictionary of Chinese Buddhist Terms.": http://mahajana.net/texts/soothill-hodous.html
This is available via a [CC BY NC SA](http://new.creativecommons.org/licenses/by-nc-sa/1.0) License.