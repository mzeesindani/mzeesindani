theshold = 0.5
net = cv2.dnn.readNetFromDarknet('My_yolov3.cfg', 'My_yolov3_final.weights')

layer_names = net.getLayerNames()
layer_names = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

with open('classes.names', 'r') as f :
labels = f.read().splitlines()

image = cv2.imread('C:\\Users\\badji\\Desktop\\project\\frame\\mydatas\\mydatas\\20220602_130139.jpg')
image = cv2.imread(path)
#plt.imshow(image)   



#cv2.namedWindow('image_plate', cv2.WINDOW_NORMAL)
#cv2.imshow('image_plate', image)
height, width, deep = image.shape

blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), (0, 0, 0), swapRB = True, crop = False)
net.setInput(blob)
layerOutPuts = net.forward(layer_names)

boxes = []
confidences = []
classIDs = []

for output in layerOutPuts :
for detection in output :
    scores = detection[5:]
    classID = np.argmax(scores)
    confidence = scores[classID]
    if confidence > defaut_confiance :
        box = detection[0:4]*np.array([width, height, width, height])
        (centerX, centerY, W, H) = box.astype('int')
        x = int(centerX - (W/2))
        y = int(centerY - (H/2))
        boxes.append([x, y, int(W), int(H)])
        confidences.append(float(confidence))
        classIDs.append(classID)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, defaut_confiance, theshold)
colors = np.random.uniform(0, 255, size = (len(boxes), 3))
#print(len(indexes), len(classIDs))
if len(indexes) > 0 :
for i in indexes.flatten() :
    (x, y, w, h) = boxes[i]
    color = colors[i]
    text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
    image_plat = cv2.rectangle(image,(x,y),(x+w+60,y+h+30),color,3)
    cv2.putText(image,text, (x, y+20), cv2.FONT_HERSHEY_PLAIN, 2, color, 5)
    image_ = image_plat[y:y+h+30, x:x+w+60]
    plat.append(cv2.resize(image_, (800, 400)))


cv2.imshow('image_plate', image)
cv2.waitKey(0)
