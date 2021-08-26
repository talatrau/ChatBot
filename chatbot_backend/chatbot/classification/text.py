import re
import os
import abc
import pickle
from underthesea import word_tokenize
from django.conf import settings


class Text(abc.ABC):
    TARGET_NAME = None
    STOP_WORD = None


    @abc.abstractmethod
    def getInstance():
        pass
    

    def __init__(self):
        self.vect = None
        self.model = None
        file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\teencode.txt')
        with open(file, 'r', encoding='UTF8') as f:
            self.teencodes = f.read().split('\n')


    def _preprocess(self, sentence):
        sentence = sentence.lower()
        sentence = "  " + sentence + " !"
        sentence = re.sub('24/24', ' ', sentence)
        sentence = re.sub(r'[!?@#$%^&*():.,;\'"+<>=|\\]+', ' ', sentence)
        sentence = re.sub(r'\b(t|thu|thứ) *(\d|hai|ba|tư|tu|nam|năm|sau|sáu|bay|bảy)\b', ' stime ', sentence)
        sentence = re.sub(r'\bchủ *nhật   \b', ' stime ', sentence)
        sentence = re.sub(r'\b\d+(-\d+)+/\d+\b', ' stime ', sentence)
        sentence = re.sub(r'\b\d+/\d+/\d\d\d\d\b', ' stime ', sentence)
        sentence = re.sub(r'\b\d+/\d+\b', ' stimeadd ', sentence)
        sentence = re.sub(r'\b(\w+/)+\w+\b', ' sadd ', sentence)
        sentence = re.sub(r'\b1* *m\d+\b', ' sheight ', sentence)
        sentence = re.sub(r'\b\d\d\d *(cm|m)\b', ' sheight ', sentence)
        sentence = re.sub(r' cao ', ' sheight ', sentence)
        sentence = re.sub(r'\b\d+ *(kg|ki|kí|ký|ky)\b', ' sweight ', sentence)
        sentence = re.sub(r' (nặng|ký|ky|ki|kí) ', ' sweight ', sentence)
        sentence = re.sub(r'\bsai +[xmls]\b', ' size m ', sentence)
        sentence = re.sub(r'\bp\d+\b', ' sadd ', sentence)
        sentence = re.sub(r'\bq\d+\b', ' sadd ', sentence)
        sentence = re.sub(r'\b\d+ \d\d\d\d+( \d+)*\b', ' sphone ', sentence)
        sentence = re.sub(r'\b(bông|bong|jean|rin|ren|len|thun|thung|gấm|gam|gâm)\b', ' smat ', sentence)
        sentence = re.sub(r'\b(chất +liệu|chất +vải|chất)\b', ' smat ', sentence)
        sentence = re.sub(r'\b\d+ *(k|m|tr|triệu|trăm|trieu|tram)\d*\b', ' scost ', sentence)
        sentence = re.sub(r'\b\d+ *(c|cai|cái|set|bộ|bo|bô|mẫu|mâu|s)\b', ' samount ', sentence)
        sentence = re.sub(r'\d+', ' number ', sentence)
        sentence = re.sub(r'sz', ' size ', sentence)
        sentence = re.sub(r'[-/]+', ' ', sentence)

        for teencode in self.teencodes:
            code = teencode.split('\t')
            sentence = re.sub(r' {} '.format(code[0]), ' {} '.format(code[1]), sentence)

        sentence = re.sub(r'\b(bao *nhiêu|tiền|giá|nhiêu|bill)\b', ' scost ', sentence)

        for word in self.STOP_WORD:
            sentence = sentence.replace(' {} '.format(word), ' ')
        
        return word_tokenize(sentence, 'text')


    @abc.abstractmethod
    def _predict(self, sentence):
        pass


    @abc.abstractmethod
    def _label2class(self, label):
        pass


    def getClass(self, sentence):
        if sentence:
            sentence = self._preprocess(sentence)
            label = self._predict(sentence)
            return self._label2class(label)
        else:
            return None



class Intent(Text):
    __instance = None
    TARGET_NAME = ['Changing', 'Connect', 'Done', 'Hello', 'Inform', 'Order', 'Other', 'Request', 'return', 'feedback']

    STOP_WORD = ['em', 'không', 'chị', 'này', 'shop', 'ạ', 'mình', 'cho', 'nha', 'nhé', 'được', 'lắm', 'thôi', 'nhưng', 'ok', 'vẫn', 'bị', 'hi', 'của', 'cua',
                'chiếc', 'chiec', 'anh', 'rồi', 'đã', 'á', 'đi', 'hả', 'ha', 'hết', 'hix', 'để', 'mà', 'hoài', 'nữa', 'ai', 'quá', 'chưa', 'lại', 'với', 'nhiều',
                'à', 'lai', 'tại', 'tai', 'nên', 'nen', 'nhiều', 'là', 'hay', 'hoặc', 'ủa', 'ua', 'thì', 'về', 'nè', 'luôn', 'luon', 'nhỉ', 'gì', 'đó', 'ơi']


    @staticmethod
    def getInstance():
        if Intent.__instance == None:
            Intent()
        return Intent.__instance


    def __init__(self):
        if Intent.__instance != None:
            raise Exception("This is a singleton")
        else:
            super().__init__()
            
            file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_tf')
            with open(file, 'rb') as f:
                self.vect = pickle.load(f)
            
            file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_svm')
            with open(file, 'rb') as f:
                self.model = pickle.load(f)

            Intent.__instance = self


    def _predict(self, sentence):
        sentence = self.vect.transform([sentence])
        label = self.model.predict(sentence)[0]
        return label


    def _label2class(self, label):
        return self.TARGET_NAME[label]



class Entity(Text):
    __instance = None
    TARGET_NAME = ['ID_product', 'color_product', 'material_product', 'cost_product', 'amount_product', 'Id_member', 'shiping_fee', 
                    'height_customer', 'weight_customer', 'phone', 'address', 'size', 'time', 'product_image']
    
    STOP_WORD = ['em', 'không', 'chị', 'này', 'shop', 'ạ', 'mình', 'cho', 'có', 'nha', 'nhé', 'được', 'lắm', 'thôi', 'nhưng', 'ok', 'vẫn', 'ơi', 'bị', 'hi', 'của', 'cua',
                'chiếc', 'chiec', 'anh', 'rồi', 'đã', 'á', 'đi', 'hả', 'ha', 'hết', 'hix', 'để', 'mà', 'hoài', 'nữa', 'ai', 'quá', 'chưa', 'lại', 'với', 'nhiều', 'à',
                'lai', 'tại', 'tai', 'nên', 'nen', 'nhiều', 'là', 'hay', 'hoặc', 'ủa', 'ua', 'thì', 'về', 'nè', 'luôn', 'luon', 'gì', 'đó']


    @staticmethod
    def getInstance():
        if Entity.__instance == None:
            Entity()
        return Entity.__instance


    def __init__(self):
        if Entity.__instance != None:
            raise Exception("This is a singleton")
        else:
            super().__init__()

            file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\entity_bow')
            with open(file, 'rb') as f:
                self.vect = pickle.load(f)
            
            file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\entity_rf')
            with open(file, 'rb') as f:
                self.model = pickle.load(f)

            Entity.__instance = self


    def _predict(self, sentence):
        sentence = self.vect.transform([sentence])
        label = self.model.predict(sentence).toarray()[0]
        return label


    def _label2class(self, label):
        return [self.TARGET_NAME[i] for i in range(len(label)) if label[i] == 1]