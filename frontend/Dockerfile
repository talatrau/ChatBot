FROM node

WORKDIR /reactjs

RUN npm install -g npm

# cài đặt các dependencies
COPY package.json .
COPY package-lock.json .

RUN npm install 
RUN npm install axios

# copy toàn bộ project vào WORKDIR
COPY . .

# chỉ định port mặc định của ReactJs
EXPOSE 3000

CMD ["npm", "start"]
