
# from PIL import Image
import json
# filepath = r"D:\garuda\test\yolo\yolov5\person_b.jpg"
# img = Image.open(filepath)

# # get width and height
# width = img.width
# height = img.height

# # display width and height
# print("The height of the image is: ", height)
# print("The width of the image is: ", width)

# def Convert_str(string):
#     li = list(string.split(" "))
#     return li
  
# Driver code    
# str1 = "Geeks for Geeks"
# print(Convert(str1))


# height = 339
# [305.2707862854, 26.572601318400018, 272.1104354858, 175.979019165, 145.37109375, 22.375793456999986, 60.247192382799994, 10.817962646500007, 170.059173584, 79.38995361330001, 203.9614257812, 174.1854095459, 203.4375915527, 174.4037780762]

# data = [{"xmin":51.7944984436,"ymin":33.7292137146,"xmax":322.1586914062,"ymax":312.4273986816,"confidence":0.8167709112,"class":0,"name":"person"},{"xmin":32.7019729614,"ymin":66.8895645142,"xmax":87.2102508545,"ymax":163.020980835,"confidence":0.7874139547,"class":58,"name":"potted plant"},{"xmin":247.1911773682,"ymin":193.62890625,"xmax":483.178894043,"ymax":316.624206543,"confidence":0.7104922533,"class":63,"name":"laptop"},{"xmin":0.0,"ymin":278.7528076172,"xmax":57.5508041382,"ymax":328.1820373535,"confidence":0.7055265307,"class":56,"name":"chair"},{"xmin":347.8956604004,"ymin":168.940826416,"xmax":432.9873352051,"ymax":259.6100463867,"confidence":0.3027570248,"class":58,"name":"potted plant"},{"xmin":45.8608322144,"ymin":135.0385742188,"xmax":77.8886947632,"ymax":164.8145904541,"confidence":0.286930263,"class":75,"name":"vase"},{"xmin":47.0410690308,"ymin":135.5624084473,"xmax":77.5586090088,"ymax":164.5962219238,"confidence":0.252784878,"class":41,"name":"cup"}]

def convert(data,height):

    data = data
    print(type(data))
    data = json.loads(data)
    # data = Convert_str(data)
    height = height
    a = 0
    b = 0
    c = 0
    d = 0

    temp = []
    i = 0
    for x in data:
        for key , value in x.items():
            if key == "ymin":
                a = value
            if key == "ymax":
                b = value
        c = height - b
        d = height - a
        temp.append(c)
        temp.append(d)

    # print(temp)


    k =  len(data)

    z = 0
    for x in range(k):
        data[x]['ymin'] = temp[z]
        z = z+2
        

    z = 1
    k =  len(data)
    for y in range(k):
        data[y]['ymax'] = temp[z]
        z = z+2

    return(data)

# res = convert(data,height)
# print(res)
