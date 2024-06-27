import cv2
import pandas as pd

image_path = 'download.jfif'
csv_file = 'colors.csv'

columns = ['color', 'color_name', 'hex', 'R', 'G', 'B']
data = pd.read_csv(csv_file, names=columns, header=None)

image = cv2.imread(image_path)
image = cv2.resize(image, (800, 600))

is_clicked = False
red = green = blue = x_coord = y_coord = 0

def get_color_name(R, G, B):
    min_distance = 1000
    for i in range(len(data)):
        distance = abs(R - int(data.loc[i, 'R'])) + abs(G - int(data.loc[i, 'G'])) + abs(B - int(data.loc[i, 'B']))
        if distance <= min_distance:
            min_distance = distance
            color_name = data.loc[i, 'color_name']
    return color_name

def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue, green, red, x_coord, y_coord, is_clicked
        is_clicked = True
        x_coord = x
        y_coord = y
        blue, green, red = image[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', image)
    if is_clicked:
        cv2.rectangle(image, (20, 20), (600, 60), (blue, green, red), -1)
        text = get_color_name(red, green, blue) + ' R=' + str(red) + ' G=' + str(green) + ' B=' + str(blue)
        cv2.putText(image, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if red + green + blue >= 600:
            cv2.putText(image, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
