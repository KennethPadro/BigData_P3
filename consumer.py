import pandas
from sklearn.preprocessing import LabelEncoder
from pyspark.sql import SparkSession
from keras.models import Sequential
from keras.preprocessing import text
from keras.layers import Activation, Dense, Dropout
from keras import utils
import csv
import numpy as np

#TRAIN#
training_data = pandas.read_csv("/cleantextlabels7.csv")
train_size = int(len(training_data) * .75)

train_text = training_data['tweet'][:train_size]
train_tags = training_data['label'][:train_size]
test_text = training_data['tweet'][train_size:]
test_tags = training_data['label'][train_size:]

tokenize = text.Tokenizer(num_words=2500)
tokenize.fit_on_texts(train_text)

x_train = tokenize.texts_to_matrix(train_text)
x_test = tokenize.texts_to_matrix(test_text)

encoder = LabelEncoder()
encoder.fit(train_tags)

y_train = encoder.transform(train_tags)
y_test = encoder.transform(test_tags)

num_classes = np.max(y_train) + 1
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(700))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(700))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(3))
model.add(Activation('softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.fit(x_train, y_train, epochs=3)
score = model.evaluate(x_test, y_test)

print('Score:', score[0])
print('Accuracy:', score[1])

model2 = Sequential()
model2.add(Dense(512))
model2.add(Dropout(0.5))
model2.add(Dense(256, activation='tanh'))
model2.add(Dropout(0.5))
model2.add(Dense(3, activation='softmax'))

model2.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model2.fit(x_train, y_train,batch_size=32,epochs=5,verbose=1,validation_split=0.1,shuffle=True)

score2 = model2.evaluate(x_test, y_test,batch_size=50, verbose=1)

print('Score:', score2[0])
print('Accuracy:', score2[1])

#PREDICT#
testing = pandas.read_csv("result.csv")

tweet = tokenize.texts_to_matrix(testing['tweet'])

text_labels = encoder.classes_


with open('/model1.csv', 'w') as m1:
    with open('/model2.csv','w') as m2:
        for i in range(len(tweet)):
            prediction = model.predict(np.array([tweet[i]]))
            predicted_label = text_labels[np.argmax(prediction)]
            prediction2 = model2.predict(np.array([tweet[i]]))
            predicted_label2 = text_labels[np.argmax(prediction2[0])]
            m1.write("%s,%s\n"%(str(tweet[i]), str(predicted_label)))
            m2.write("%s,%s\n" % (str(tweet[i]), str(predicted_label2)))

spark = SparkSession.builder.getOrCreate()
df = spark.read.csv("keywords.csv", header=True, inferSchema=True)
df.createOrReplaceTempView("neural")
sqlResult = spark.sql("select Keyword, Label as label, count(*) as value from neural group by Keyword, label order by Keyword, label")
sqlResult.show()
print(sqlResult.toJSON().collect())

