from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

#Реализация модели машинного обучения для определения тональности текста
def func(text):
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    messages=[]
    messages.append(text)
    results = model.predict(messages, k=2)
    print(results[0])
    try:
        if 'neutral' in list(results[0].keys()) and 'negative' in list(results[0].keys()):
            return 'negative'
        elif 'neutral' in list(results[0].keys()) and 'positive' in list(results[0].keys()):
            return 'positive'
        elif results[0][list(results[0].keys())[0]]>results[0][list(results[0].keys())[1]]:
            return list(results[0].keys())[0]
        elif results[0][list(results[0].keys())[0]]<results[0][list(results[0].keys())[1]]:
            return list(results[0].keys())[1]
        else:
            return 'negative'
    except:
        return 'neutral'


#print(func(134,"Я понял материал. Всё хорошо изложено"))
