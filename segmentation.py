total_air_chars_sorted = []
dilation_ = []
tree_rect =[]
images= []
u=0
cutOutImg= []

#image_plaque = cv2.imread('C:\\Users\\badji\\Desktop\\project\\good project\\essaieyoloV3\\Modules_YOLOv3\\to_transform6.jpg')
img_lp = plt.imread('C:\\Users\\badji\\Desktop\\mydatas\\mydatas\\20220527_120911.jpg')
img_lp = cv2.resize(img_lp, (800, 400))
#img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
#plt.imshow(img_lp)
rows, cols, a = img_lp.shape

gray = cv2.cvtColor(img_lp, cv2.COLOR_RGB2GRAY)
# resize image to three times as large as original for better readability
gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
gray1 = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)

# perform gaussian blur to smoothen image
blur = cv2.GaussianBlur(gray, (5,5), 0)
#cv2.imshow("Gray", gray)
#cv2.waitKey(0)
# threshold the image using Otsus method to preprocess for tesseract
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#cv2.imshow("Otsu Threshold", thresh)
#cv2.waitKey(0)
# create rectangular kernel for dilation
rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# apply dilation to make regions more clear
dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
#cv2.imshow("Dilation", dilation)
#cv2.waitKey(0)
# find contours of regions of interest within license plate
try:
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
except:
    ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# sort contours left-to-right
sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

# create copy of gray image
im2 = gray.copy()
# create blank string to hold license plate number
plate_num = ""
# loop through contours and find individual letters and numbers in license plate
air_chars_sorted = []
i= 0
for cnt in sorted_contours:
    air_chars_sorte = x,y,w,h = cv2.boundingRect(cnt)
    height, width = im2.shape
    # if height of box is not tall enough relative to total height then skip
    #if height / float(h) > 6: continue

    ratio = h / float(w)
    # if height to width ratio is less than 1.5 skip
    if ratio < 0.6: continue
    hauteur_img, largeur_img, profondeur = (img_lp.shape)
    #if y > int(hauteur_img*1.2) : continue

    # if width is not wide enough relative to total width then skip
    #if width / float(w) > 15: continue

    area = h * w
    # if area is less than 100 pixels skip
    if area < 14000: continue

    if area > 220000 : continue
    # draw the rectangle
    tree_rect.append(air_chars_sorte)
    # grab character region of image

    #plt.imshow(roi)
    air_chars_sorted.append(air_chars_sorte)
print(len(tree_rect))
tree_index = []
for i in range(len(tree_rect)):
    x,y,w,h = tree_rect[i]
    for j in range(len(tree_rect)):
        x_af,y_af,w_af, h_af = tree_rect[j] 
        if (x<x_af)and((x+w)>(x_af+w_af))and(y<y_af):
            tree_index.append(j)
print(len(tree_index))

for i,j in zip(tree_index, range(len(tree_index))):
    i = i-j
    tree_rect.pop(i)
print(len(tree_rect))
for i in range(len(tree_rect)):
    x,y,w,h = tree_rect[i]
    rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),5)
if len(air_chars_sorted) != 0 :
    total_air_chars_sorted.append(air_chars_sorted)

rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),5)

roi = thresh[y-5:y+h+5, x-5:x+w+5]

# perfrom bitwise not to flip image to black text on white background
roi = cv2.bitwise_not(roi)
# perform another blur on character region
roi = cv2.medianBlur(roi, 5)
#images.append(roi)
air_chars_sorted = 0
#plt.subplot(1, len(img_founded), i+1)
#plt.imshow(dilation, cmap='gray')
cutOutImg.append(roi)
plt.imshow(rect)
#cv2.imshow("Otsu Threshold", thresh)
i += 1
images.append(cutOutImg)
