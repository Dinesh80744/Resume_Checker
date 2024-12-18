import streamlit as st
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text  
from docx import Document
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#import path1 as p1
resume_extension = ''
resume_text = ''   



st.title("Compare Resume With Job Description")

resume_files = st.file_uploader('Choose Resume File', type=["pdf","docx"],accept_multiple_files=True)




job_description = st.text_area("Enter Job Decription:")

stop_words = set(stopwords.words('english'))
custom_stop_words = ['looking','like','strong','methods']
# Update the stopwords set with custom words
stop_words.update(custom_stop_words)

# To Determine the type of file
def determine_file_format(file):
    _, file_extension = os.path.splitext(file)
    #print(file_extension)
    return _

    
# To convert pdf to Text
def pdf_to_text(file):
    text = extract_text(file)
    #print(text)
    return text

    
# To convert doc to text
def docx_to_text(file_path):
    text = Document(file_path)
    text = ''.join([para.text for para in text.paragraphs])
    return text

#Replacing with single spaces for both tabspace and symbols
def regular_expression(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = text.split(' ')
    #print(text)
    return text

# To Remove StopWords
def remove_stopwords(words):       
    filtered_words = [word for word in words if word.lower() not in stop_words]
    #print(filtered_words)
    return filtered_words


#Similarity between lists
def cosine_similarity_Lists(list1, list2):
    vectorizer = TfidfVectorizer().fit_transform([' '.join(list1), ' '.join(list2)])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

def c_similarity():
            # Finding Similarity
            similarity = cosine_similarity_Lists(job_text_withoutSW,resume_text_withoutSW)
            print('cosine_similarity:',similarity)
            return similarity
            
def missing_words():
    # Finding missing words in resume
    missing_words = list(set(job_text_withoutSW)-set(resume_text_withoutSW))
    print("Missing Words in Resume:",missing_words)
    return missing_words

percentage = st.button("Match percentage")
missinwords = st.button("Missing Words in Resume")
rank_button = st.button("Rank")
rank_dict = {}

if resume_files and len(resume_files)>=1:
    for i,resume_file in enumerate(resume_files):
        if resume_file is not None:
        # Get the file name
            file_name = resume_file.name
            # Extract the file extension
            resume_extension = file_name.split(".")[-1].lower()
            #print(resume_extension)

        if resume_extension  == 'pdf':
            resume_text = pdf_to_text(resume_file)
        elif resume_extension == 'docx':
            resume_text = docx_to_text(resume_file)



            
        resume_text_withSW = regular_expression(resume_text)
        resume_text_withoutSW = remove_stopwords(resume_text_withSW)

            
        job_text_withSW = regular_expression(job_description)
        job_text_withoutSW = remove_stopwords(job_text_withSW)

        for i in range (len(resume_files)):
            key = f'{resume_file.name}'
            value = c_similarity()*100
            rank_dict[key] = "{:.2f}%".format(value)
            sorted_dict = dict(sorted(rank_dict.items(), key=lambda item: (item[1], item[0])))



        
        #st.button("Match Resume",on_click=p1.determine_file_format(resume_file))
        if percentage:
            value = c_similarity()*100
            f_value = "{:.2f}%".format(value)
            st.write(f"Match Percentage of {resume_file.name}:\t",f_value)
        if missinwords:
            value = missing_words()
            st.title(f"Missing Skills of {resume_file.name}:")
            for i in value:
                st.write(i)
if rank_button:
    st.title("Ranking the Resumes:")
    for key,value in sorted_dict.items():
        st.write(key,":",value)