from flask import Flask,render_template,request,redirect
import joblib,cv2,base64,numpy as np

model = joblib.load("captcha_model.pk1")

def b64_to_image(b64):
    b64_data = b64.split(',')[1]
    image = np.frombuffer(base64.b64decode(b64_data), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    return image

def get_captcha(base64_url):
    result = ""
    test_image = b64_to_image(base64_url)
    threshold, test_image = cv2.threshold(test_image,0.001,10**9,cv2.THRESH_BINARY)
    iterator = [0,30,60,90,120,150]
    for i in iterator:
        temp_img = test_image[10:,i:i+25]
        temp_img = temp_img.reshape(1,(temp_img.shape[0]*temp_img.shape[1]))
        prediction = model.predict(temp_img)[0]
        if prediction >= 10:
            result += chr(prediction)
        else:
            result += str(prediction)
    return result

app = Flask(__name__)

@app.route("/")
def main():
    return redirect("/VTOP/")

@app.route("/VTOP",methods=["POST","GET"])
def reddit():
    if request.method == "POST":
        sr = str(request.form["b64_url"])
        result = get_captcha(sr)
        return render_template("captcha.html",inp=sr,result = result)
    else:
        return render_template("captcha.html")

if __name__ == "__main__":
    app.run()
