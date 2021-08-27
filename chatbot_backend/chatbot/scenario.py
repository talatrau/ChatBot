import re
import random
import threading
from chatbot.models import Company, Fashion, FashionDetail

class Scenario:
    def __init__(self):
        self.productId = None
        self.product = None
        self.state = None
        self.event = None
        self.amount = False
        self.size = False
        self.cost = False
        self.height = False
        self.weight = False
        self.requestEvent = None
        self.time = None
        self.address = ""
        self.material = ""
        self.color = ""
        self.requestFlag = False
        self.response = []


    def genResponse(self, intent, entities, text):
        if self.requestFlag and self.event.is_alive():
            self.event.cancel()

        if intent == "Hello":
            self.response.append("Chào bạn bạn cần tư vấn vấn đề gì ạ")
        elif intent == "Request":
            if len(entities) == 0:
                self.response.append("Mình không hiểu ý bạn")
            else:
                self.requestFlag = True
                for entity in entities:
                    if entity == "amount_product":
                        self.amount = True
                    elif entity == "size":
                        self.size = re.findall(r'\b(size|sz)? *(s|m|l|xl|xxl)\b', text.lower())[0][1]
                    elif entity == "cost_product":
                        self.cost = True
                    elif entity == "color_product":
                        self.color = True
                    elif entity == "material_product":
                        self.material = True
                    
        elif intent == "Inform":
            if self.requestFlag:
                self.event.cancel()

            for entity in entities:
                if entity == "height_customer":
                    self.height = re.findall(r'\b(1)? *(m)?(\d)+\b', text.lower())[0]
                    self.height = ''.join(i for i in self.height)
                elif entity == "weight_customer":
                    self.weight = re.findall(r'\b(\d+) *(kg|kí|ki|ký|ky|k)\b', text.lower())[0]
                    self.weight = ''.join(i for i in self.weight)
                elif entity == "size":
                    self.size = re.findall(r'\b(size|sz)? *(s|m|l|xl|xxl)\b', text.lower())[0][1]
                elif entity == "time":
                    self.time = True

        elif intent == "Done":
            self.response.append("Cảm ơn bạn đã quan tâm và ủng hộ")

        elif intent == "Other":
            self.response.append("Xin lỗi mình không hiểu ý bạn")

        if self.requestFlag:
            self.event = threading.Timer(10, self.requestScienario, ())
            self.event.start()

    def getResponse(self):
        res = self.response
        self.response = []
        return res


    def setProductID(self, productID):
        self.productId = productID
        self.state = [True] * 14
        self.product = Fashion.objects.get(pk=self.productId).__dict__
        
        if self.requestFlag and self.event.is_alive():
            self.event.cancel()

        if self.requestFlag:
            self.event = threading.Timer(10, self.requestScienario, ())
            self.event.start()

    
    def requestScienario(self):
        if self.requestFlag:
            if not self.productId:
                self.response.append("Bạn quan tâm sản phẩm nào ạ?")
            else:
                if self.state[1] and self.color:
                    self.state[1] = False
                    self.response.append("mẫu này có màu {} ạ".format(self.product['color']))

                if self.state[2] and self.material:
                    self.state[2] = False
                    self.response.append("làm từ {} nha ban".format(self.product['material']))

                if self.state[11] and self.state[4] and self.size:
                    self.state[11], self.state[4] = False, False
                    detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
                    amount = int(detail['amount'])
                    if amount > 0:
                        self.response.append("mẫu {} này còn size {} nha bạn giá là {}k".format(self.product['name'], self.size, detail['cost']))
                    else:
                        self.response.append("mẫu này bên mình hết hàng rồi ạ")
                elif self.state[11] and self.state[4] and not self.size:
                    if not self.height and not self.weight:
                        self.response.append("Bạn cho mình xin chiều cao cân nặng được không ạ để mình lấy size")
                    elif not self.height:
                        self.response.append("Bạn cho mình xin số đo chiều cao được không ạ")
                    elif not self.weight:
                        self.response.append("Bạn cho mình xin cân nặng được không ạ")
                    else:
                        self.state[11], self.state[4] = False, False
                        self.size = random.choice(['s', 'm', 'l'])
                        detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
                        amount = int(detail['amount'])
                        if amount > 0:
                            self.response.append("cao {} {} mặc size {} nha bạn".format(self.height, self.weight, self.size))
                            self.response.append("mẫu {} này size {} giá là {}k".format(self.product['name'], self.size, detail['cost']))
                        else:
                            self.response.append("Bạn mặc size {} nhưng size này bên mình hết hàng rồi ạ".format(self.size))