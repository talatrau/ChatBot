import re
import random
import threading
from chatbot.models import Company, Fashion, FashionDetail

# class Scenario:
#     def __init__(self):
#         self.productId = None
#         self.product = None
#         self.state = None
#         self.event = None
#         self.amount = False
#         self.size = False
#         self.cost = False
#         self.height = False
#         self.weight = False
#         self.requestEvent = None
#         self.time = None
#         self.address = ""
#         self.material = ""
#         self.color = ""
#         self.requestFlag = False
#         self.response = []


#     def genResponse(self, intent, entities, text):
#         if self.requestFlag and self.event.is_alive():
#             self.event.cancel()

#         if intent == "Hello":
#             self.response.append("Chào bạn bạn cần tư vấn vấn đề gì ạ")
#         elif intent == "Request":
#             if len(entities) == 0:
#                 self.response.append("Mình không hiểu ý bạn")
#             else:
#                 self.requestFlag = True
#                 for entity in entities:
#                     if entity == "amount_product":
#                         self.amount = True
#                     elif entity == "size":
#                         self.size = re.findall(r'\b(size|sz)? *(s|m|l|xl|xxl)\b', text.lower())[0][1]
#                     elif entity == "cost_product":
#                         self.cost = True
#                     elif entity == "color_product":
#                         self.color = True
#                     elif entity == "material_product":
#                         self.material = True
                    
        # elif intent == "Inform":
        #     if self.requestFlag:
        #         self.event.cancel()

        #     for entity in entities:
        #         if entity == "height_customer":
        #             self.height = re.findall(r'\b(1)? *(m)?(\d)+\b', text.lower())[0]
        #             self.height = ''.join(i for i in self.height)
        #         elif entity == "weight_customer":
        #             self.weight = re.findall(r'\b(\d+) *(kg|kí|ki|ký|ky|k)\b', text.lower())[0]
        #             self.weight = ''.join(i for i in self.weight)
        #         elif entity == "size":
        #             self.size = re.findall(r'\b(size|sz)? *(s|m|l|xl|xxl)\b', text.lower())[0][1]
        #         elif entity == "time":
        #             self.time = True

#         elif intent == "Done":
#             self.response.append("Cảm ơn bạn đã quan tâm và ủng hộ")

#         elif intent == "Other":
#             self.response.append("Xin lỗi mình không hiểu ý bạn")

#         if self.requestFlag:
#             self.event = threading.Timer(10, self.requestScienario, ())
#             self.event.start()

#     def getResponse(self):
#         res = self.response
#         self.response = []
#         return res


#     def setProductID(self, productID):
#         self.productId = productID
#         self.state = [True] * 14
#         self.product = Fashion.objects.get(pk=self.productId).__dict__
        
#         if self.requestFlag and self.event.is_alive():
#             self.event.cancel()

#         if self.requestFlag:
#             self.event = threading.Timer(10, self.requestScienario, ())
#             self.event.start()

    
#     def requestScienario(self):
#         if self.requestFlag:
#             if not self.productId:
#                 self.response.append("Bạn quan tâm sản phẩm nào ạ?")
#             else:
#                 if self.state[1] and self.color:
#                     self.state[1] = False
#                     self.response.append("mẫu này có màu {} ạ".format(self.product['color']))

#                 if self.state[2] and self.material:
#                     self.state[2] = False
#                     self.response.append("làm từ {} nha ban".format(self.product['material']))

#                 if self.state[11] and self.state[4] and self.size:
#                     self.state[11], self.state[4] = False, False
#                     detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
#                     amount = int(detail['amount'])
#                     if amount > 0:
#                         self.response.append("mẫu {} này còn size {} nha bạn giá là {}k".format(self.product['name'], self.size, detail['cost']))
#                     else:
#                         self.response.append("mẫu này bên mình hết hàng rồi ạ")
#                 elif self.state[11] and self.state[4] and not self.size:
#                     if not self.height and not self.weight:
#                         self.response.append("Bạn cho mình xin chiều cao cân nặng được không ạ để mình lấy size")
#                     elif not self.height:
#                         self.response.append("Bạn cho mình xin số đo chiều cao được không ạ")
#                     elif not self.weight:
#                         self.response.append("Bạn cho mình xin cân nặng được không ạ")
#                     else:
#                         self.state[11], self.state[4] = False, False
#                         self.size = random.choice(['s', 'm', 'l'])
#                         detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
#                         amount = int(detail['amount'])
#                         if amount > 0:
#                             self.response.append("cao {} {} mặc size {} nha bạn".format(self.height, self.weight, self.size))
#                             self.response.append("mẫu {} này size {} giá là {}k".format(self.product['name'], self.size, detail['cost']))
#                         else:
#                             self.response.append("Bạn mặc size {} nhưng size này bên mình hết hàng rồi ạ".format(self.size))


def lcs(X, Y):
    m = len(X)
    n = len(Y)
  
    L = [[None]*(n + 1) for i in range(m + 1)]
  
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    return L[m][n]



class Scenario:
    def __init__(self):
        self.productId = None
        self.product = None
        self.state = None
        self.event = None
        self.amount = 0
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
        self.state = 0
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
                self.state = 1 if self.state == 0 else self.state
                for entity in entities:
                    if entity == "amount_product":
                        num = re.findall(r'\b(\d+) *(c|cái|cai|chiếc)\b', text.lower())
                        self.amount = int(num[0][0]) if num else 1
                    elif entity == "size":
                        self.size = re.findall(r'\b(size|sz)? *(s|m|l|xl|xxl)\b', text.lower())[0][1]
                    elif entity == "cost_product":
                        self.cost = True
                    elif entity == "color_product":
                        self.color = re.findall(r'(vàng|đỏ|xanh|tím|da|nâu|cam|lục|lam|đen)', text.lower())
                    elif entity == "material_product":
                        self.material = True
                    elif entity == "product_image":
                        pass
        
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

        if self.state != 3:
            if "đầm" in text.lower() or "áo" in text.lower() or "quần" in text.lower():
                products = Fashion.objects.all()
                names = [product.__dict__['name'] for product in products]
                score = [lcs(text, name) for name in names]
                best = max(score)
                index = [i for i in range(len(names)) if score[i] == best]
                if len(index) == 1:
                    self.product = products[index[0]].__dict__
                    self.productId = self.product['id']
                    self.state = 3
                else:
                    self.state = 2
                    self.product = [names[i] for i in index]

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
        self.state = 3

        if self.requestFlag and self.event.is_alive():
            self.event.cancel()

        if self.requestFlag:
            self.event = threading.Timer(10, self.requestScienario, ())
            self.event.start()

    
    def requestScienario(self):
        if self.state == 1:
            self.response.append("Bạn quan tâm sản phẩm nào ạ?")
        elif self.state == 2:
            mess = "Bên mình có " + ','.join(self.product)
            self.response.append(mess)
            self.response.append("Bạn muốn chính xác mẫu nào?")
        elif self.state == 3:
            if self.amount > 0:
                if self.size:
                    detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
                    amount = int(detail['amount'])
                    if amount > self.amount:
                        self.response.append("còn nha bạn".format(self.size, detail['cost']))
                    else:
                        if amount > 0:
                            self.response.append("Bên mình chỉ còn {} cái size {} thôi".format(amount, self.size))
                        else:
                            self.response.append("Bên mình hết size {} rồi bạn".format(self.size))
                    self.amount = 0
                else:
                    self.response.append("Bạn muốn lấy size nào ạ")
            
            if self.cost:
                if self.size:
                    detail = FashionDetail.objects.filter(fashionid=self.productId).filter(size=self.size.upper())[0].__dict__
                    self.response.append("size {} giá {}k nha bạn".format(self.size, detail['cost']))
                else:
                    details = FashionDetail.objects.filter(fashionid=self.productId)
                    res = ["size {} là {}k".format(detail.__dict__['size'], detail.__dict__['cost']) for detail in details]
                    self.response.append(' '.join(r for r in res))
                self.cost = False

            if self.color:
                not_exist_color = []
                for color in self.color:
                    if color not in self.product['color']:
                        not_exist_color.append(color)

                if not_exist_color:
                    self.response.append("không có màu " + ",".join(not_exist_color))
                self.response.append("màu {} nha bạn".format(self.product['color']))
                self.color = ""

            if self.material:
                self.material = False
                self.response.append("làm từ {} nha ban".format(self.product['material']))