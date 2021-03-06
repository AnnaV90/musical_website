FROM python:3.8.6-buster
COPY vinyl-records_istock.png /image_interface/vinyl-records_istock.png
#COPY Tests_music/i-do-like-to-be-beside-the-seaside.mid /Tests_music/i-do-like-to-be-beside-the-seaside.mid
COPY Tests_music/. Tests_music/
COPY app.py /app.py
COPY songConverter.py /songConverter.py
COPY Prediction_music /Prediction_music

COPY requirements.txt /requirements.txt
EXPOSE 5801
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["sh", "-c", "streamlit run --server.port $PORT app.py"]

CMD streamlit run --server.port $PORT app.py
