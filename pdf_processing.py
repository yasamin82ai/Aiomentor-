import fitz  # PyMuPDF
import numpy as np
from langchain_openai import OpenAIEmbeddings  # استفاده از langchain-openai به‌جای langchain_community

def extract_text_from_pdf(pdf_path):
    """ استخراج متن از فایل PDF """
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error: {e}")
        return ""

def get_pdf_embedding(text, embedding_model):
    """ استخراج وکتور از متن با استفاده از مدل OpenAI Embeddings """
    # استفاده از embed_documents به‌جای embed
    embedding = embedding_model.embed_documents([text])  # توجه به اینکه ورودی یک لیست از اسناد است
    return np.array(embedding[0]).tobytes()  # تبدیل وکتور به بایت‌ها برای ذخیره در دیتابیس
