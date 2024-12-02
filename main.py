from langchain_openai import OpenAIEmbeddings  # استفاده از langchain-openai به‌جای langchain_community
from langchain_community.vectorstores import FAISS  # تغییر به langchain_community
from langchain_community.llms import OpenAI  # تغییر به langchain_community
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from sqlite_database import create_connection, create_table, insert_document, fetch_all_documents
from pdf_processing import extract_text_from_pdf, get_pdf_embedding

# کلید API OpenAI
API_KEY = "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"  # کلید API خود را وارد کنید

# ایجاد اتصال به دیتابیس SQLite
db_file = "documents.db"
conn = create_connection(db_file)
create_table(conn)

# مسیر فایل PDF
pdf_path = "aio.pdf"  # مسیر فایل PDF خود را وارد کنید

# پردازش و استخراج محتوا از فایل PDF
pdf_text = extract_text_from_pdf(pdf_path)

# ایجاد مدل Embedding برای تبدیل متن به وکتور
embedding_model = OpenAIEmbeddings(openai_api_key=API_KEY)

# استخراج وکتور متن از محتوای PDF
pdf_embedding = get_pdf_embedding(pdf_text, embedding_model)

# ذخیره محتوای PDF به همراه وکتور آن در دیتابیس
insert_document(conn, "Sample Document", pdf_text, pdf_embedding)

# ایجاد مدل LLM و پرامپت برای پردازش متن
llm = OpenAI(openai_api_key=API_KEY)  # استفاده از مدل OpenAI برای پردازش

# تعریف پرامپت به‌گونه‌ای که از مدل خواسته شود به زبان فارسی پاسخ دهد
prompt_template = "لطفاً به زبان فارسی به سوال زیر پاسخ دهید: {question}"  # تعریف پرامپت
prompt = PromptTemplate(input_variables=["question"], template=prompt_template)  # ایجاد پرامپت
chain = LLMChain(llm=llm, prompt=prompt)  # ترکیب مدل و پرامپت

# پرسش از مدل LLM
response = chain.invoke({"question": "آیولرن چیه؟", "chat_history": []})

# نمایش پاسخ مدل
print("LLM Response:", response)

# دریافت تمام اسناد از دیتابیس
documents = fetch_all_documents(conn)
print("Stored documents:")
for doc in documents:
    print(f"ID: {doc[0]}, Title: {doc[1]}, Content: {doc[2][:100]}...")  # نمایش اولین 100 کاراکتر از محتویات

# بستن اتصال به دیتابیس
conn.close()
