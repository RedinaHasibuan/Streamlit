import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator, MyMemoryTranslator

# Function terjemahan dengan Cache
@st.cache_data
def translate_text(text):
    if not text.strip():
        return ""
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception:
        try:
            return MyMemoryTranslator(source='id-ID', target='en-US').translate(text)
        except Exception:
            return text

def convert_to_df(sentiment):
    sentiment_dict = {'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity}
    sentiment_df = pd.DataFrame(sentiment_dict.items(), columns=['metric', 'value'])
    return sentiment_df

# Function analisis token khusus Bahasa Indonesia
def analyze_token_sentiment_indo(docx_indo):
    analyzer = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []
    
    # Memecah kata-kata asli Bahasa Indonesia
    words = docx_indo.split()
    
    for word in words:
        clean_word = word.strip(".,!?\"'()")
        # Dapatkan nilai sentimen berdasarkan arti terjemahan kata tersebut
        word_en = translate_text(clean_word)
        res = analyzer.polarity_scores(word_en)['compound']
        
        if res > 0.1:
            pos_list.append(clean_word)
            pos_list.append(res)
        elif res <= -0.1:
            neg_list.append(clean_word)
            neg_list.append(res)
        else:
            neu_list.append(clean_word)
            
    result = {'positif': pos_list, 'negatif': neg_list, 'netral': neu_list}
    return result

def main():
    st.title("Indonesian Sentiment Analysis NLP App")
    st.subheader("Streamlit Projects")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home (Bahasa Indonesia)")
        with st.form("nlpFormIndo"):
            raw_text = st.text_area("Masukkan Teks Bahasa Indonesia di Sini")
            submit_button = st.form_submit_button(label='Analisis Sentimen')

        col1, col2 = st.columns(2)
        
        if submit_button and raw_text.strip():
            translated_text = translate_text(raw_text)
            
            with col1:
                st.info("Hasil Analisis Sentimen")
                
                sentiment = TextBlob(translated_text).sentiment
                st.write(sentiment)

                if sentiment.polarity > 0:
                    st.markdown("Sentimen:: Positif :smiley:")
                elif sentiment.polarity < 0:
                    st.markdown("Sentimen:: Negatif :angry:")
                else:
                    st.markdown("Sentimen:: Netral :neutral_face:")

                result_df = convert_to_df(sentiment)
                st.dataframe(result_df)

                c = alt.Chart(result_df).mark_bar().encode(
                    x='metric',
                    y='value',
                    color='metric'
                )
                st.altair_chart(c, use_container_width=True)

            with col2:
                st.info("Analisis Sentimen Per Kata (Token)")
                # Memanggil fungsi token khusus teks Bahasa Indonesia
                token_sentiments = analyze_token_sentiment_indo(raw_text)
                st.write(token_sentiments)

    else:
        st.subheader("About")
        st.write("Aplikasi analisis sentimen Bahasa Indonesia berbasis Translation + TextBlob & VADER.")

if __name__ == '__main__':
    main()