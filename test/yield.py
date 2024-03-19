import whisper

model = whisper.load_model("large")
result = model.transcribe("D:/Video/真正的人生攻略，這一期也許你會看了又看 - 老高與小茉 Mr & Mrs Gao.mkv")
print(result['text'])