from cProfile import label
from ntpath import join
from operator import le
import re
import sys
import unicodedata as ud
import streamlit as st
from spellcheck_words import is_spelled_correctly
from spellcheck_words_vi import is_spelled_correctly_vi
from textblob import TextBlob
from gingerit.gingerit import GingerIt
warning = '\033[91m'
unwarning = '\033[m'
from load_css import local_css
local_css("style.css")
x = '\n' + "<span class='highlight green'>"
y = "</span>"
x1 = '\n' + "<span class='highlight green1'>"
y1 = "</span>"
h1 = '\n' + "<span class='highlight hd'>"
h2 = "</span>"

hide_menu = """
<style>
footer{
  visibility:visible;  
}

footer:after{
   content: 'Nguyen Quang Nhat from Information of technology - Quy Nhon University';
   display:block;
   position:relative;
   color:tomato;
   padding:5px;
   top:3px;
   backgroundColor= red;
   secondaryBackgroundColor="#e0e0ef";
   textColor="#262730";
}
</style>
"""
def header(url):
    st.markdown(f'<p style="background-color:#00004d;text-align:center;color:#ff0066;font-size:40px;text-align=center;border-radius:10%;font-family: "Times New Roman", Times, serif;"><marquee direction="right">{url}</marquee></p>', unsafe_allow_html=True)
st.header('NLP - SPELLING CORRECTION - NGUYEN QUANG NHAT')

menu = ["1. Introduction", "2. Check spelling Words", "3. Correct spelling words"]
choice = st.sidebar.selectbox("OPTIONS", menu)
def so_Luong_Amtiet(text):
    # TODO: Fix bug on datetime, E.g. 2013/10/20 09:20:30
    text = ud.normalize('NFC', text)
    sign = ["==>", "->", "\.\.\.", ">>"]
    digits = "\d+([\.,_]\d+)+"
    email = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    web = "^(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
    datetime = [
        "\d{1,2}\/\d{1,2}(\/\d+)?",
        "\d{1,2}-\d{1,2}(-\d+)?",
    ]
    word = "\w+"
    non_word = "[^\w\s]"
    abbreviations = [
        "[A-ZĐ]+\.",
        "Tp\.",
        "Mr\.", "Mrs\.", "Ms\.",
        "Dr\.", "ThS\."
    ]
    patterns = []
    patterns.extend(abbreviations)
    patterns.extend(sign)
    patterns.extend([web, email])
    patterns.extend(datetime)
    patterns.extend([digits, non_word, word])
    patterns = "(" + "|".join(patterns) + ")"
    if sys.version_info < (3, 0):
        patterns = patterns.decode('utf-8')
    tokens = re.findall(patterns, text, re.UNICODE)
    return [token[0] for token in tokens]

import spacy    
nlp = spacy.load('en_core_web_sm')

def NER(text):
    x = nlp(text)
    ten_rieng = []
    label = []
    for i in x.ents:
        ten_rieng.append(i.text)
        label.append(i.label_)
    return {"ten_rieng": ten_rieng, "label": label}
import numpy as np


def check_words(data_check):
    data_check.replace(".", "")
    data_check.replace("I", "")
    data = so_Luong_Amtiet(data_check)
    data1 = " ".join(data)

    x = NER(data1)['ten_rieng']
    ner_arr = np.array(x)

    y = NER(data1)['label']
    label_arr = np.array(y)

    dem = 0
    for i in range(len(data)):
        if not is_spelled_correctly(data[i]):
            dem += 1
            str = "".join(data[i])
            a = "<span class='highlight blue'>"
            # a1 = "<span class='highlight blue1'>"
            b = "</span>"
            # for j in range(len(ner_arr)):
            v = ner_arr
            v = np.array(v)

            v1 = label_arr
            v1 = np.array(v1)
            j = 0
            exp = ''
            str1 = ''
            count = 0
            for j in range(len(v)):
                if str == v[j]:
                    count = dem - 1
                    str1 = str + ' {' + v1[j] + '}'
                    exp = v1[j] + ' (explain: ' + spacy.explain(v1[j]) + ')'
                else:
                    str1 = a + str + b
                    exp = ' Null'
            data[i] = str1

    return {"result": data, "false_number": count, "explain": exp}
#EN
def correct_words(data_input):
    data_input = so_Luong_Amtiet(data_input)
    data_input1 = " ".join(data_input)
    text = TextBlob(data_input1)
    kq = text.correct()
    return kq
#EN
def Check_grammar(data_input):
    dem = 0
    data_input = so_Luong_Amtiet(data_input)
    data_input = " ".join(data_input)
    dip = data_input.split(' ')
    parse = GingerIt()
    correct = parse.parse(data_input)["result"]
    correct_i = correct.split(' ')
    for i in range(len(dip)):
        if dip[i] != correct_i[i]:
            dem +=1
            a = "<span class='highlight blue'>"
            b = "</span>"
            # str1 = a + str + b
    return {"result": correct, "false_number": dem}
#EN
def Correct_grammar(data_input):
    data_input = so_Luong_Amtiet(data_input)
    data_input = " ".join(data_input)
    dip = data_input.split('.')
    parse = GingerIt()
    for i in range(len(dip)):
        correct_i = parse.parse(dip[i])["result"]
        if dip[i] not in correct_i:
            dip[i] = parse.parse(dip[i])["result"]
    # rt = "\r\n".join(dip)
    rt = ".".join(dip)
    return rt
if choice == "1. Introduction":
    a = "<span class='highlight blue'>"
    b = "</span>"
    sai = x+'correction'+y
    t1 = x+'website' +y
    t = x + 'Welcome to the spelling '+ y
    ok  = t + sai + t1
    st.markdown(ok, unsafe_allow_html=True)
    st.markdown(hide_menu, unsafe_allow_html = True)
    new_title = '<p style="font-family:sans-serif; color:#baf605; font-size: 42px;">&#10004; A dog</p>'
    new_title1 = '<p style="font-family:sans-serif; color:red; font-size: 42px;"> &#10005; Ann owll</p>'
    new_title2 = '<p style="font-family:sans-serif; color:#fff; font-size: 42px;">Author</p>'
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(new_title, unsafe_allow_html=True)
        st.image("https://static.streamlit.io/examples/dog.jpg")
    with col2:
        st.markdown(new_title1, unsafe_allow_html=True)
        st.image("https://static.streamlit.io/examples/owl.jpg")
if choice == "2. Check spelling Words":
    c = h1 + 'Check spelling Words'+ h2
    st.markdown(c, unsafe_allow_html=True)
    st.subheader = "Check spelling Words"
    input_type = st.text_input(
        "SELECT A LANGUAGE TO CHECK WORDS",
        ("English"),
    )
    Enter_text = st.text_input("\nEnter your text:")
    data = Enter_text
    if st.button("View this text:", key=1, on_click=None):
        st.text_area("CONTENTS: ", value=data, height=None, max_chars=None, key=10)
    if st.button("CHECK", key=2):
                st.markdown(data)
                check = " ".join(check_words(data)["result"])
                # check = check_words(data)["result"]
                fal = check_words(data)["false_number"]
                c = "RESULT CHECKING: "
                c = x+c+y
                st.markdown(c, unsafe_allow_html=True)
                st.markdown(check, unsafe_allow_html=True)
                #st.markdown(x1 + "Detected error is: " + y1 + x+ str(fal)+y, unsafe_allow_html=True)

if choice == "3. Correct spelling words":
    c = h1 + 'Correct spelling Words' + h2
    st.markdown(c, unsafe_allow_html=True)
    st.subheader = "Correct spelling Words"
    input_type = st.text_input(
        "SELECT A LANGUAGE TO CORRECT WORDS",
        ("English"),
    )
    Enter_text = st.text_input("Enter your text:")
    data = Enter_text
    if st.button("View this text:", key=1, on_click=None):
        st.text_area("CONTENTS: ", value=data, height=None, max_chars=None, key=10)
    if st.button("CORRECT", key=2):
                st.markdown(data)
                check = "".join(correct_words(data))
                st.text_area("\nRESULT CORRECT: ", value=check, height=None, max_chars=None, key=10)
                new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">&#10004;</p>'
                st.markdown(new_title, unsafe_allow_html=True)