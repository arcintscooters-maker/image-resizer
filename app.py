from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image
import io
import os
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

TARGET = 800
QUALITY = 82

def process_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = img.size

    scale_h = TARGET / h
    new_w_by_h = int(w * scale_h)

    scale_w = TARGET / w
    new_h_by_w = int(h * scale_w)

    if new_w_by_h <= TARGET:
        new_w, new_h = new_w_by_h, TARGET
    else:
        new_w, new_h = TARGET, new_h_by_w

    img = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (TARGET, TARGET), (255, 255, 255))
    left = (TARGET - new_w) // 2
    top = (TARGET - new_h) // 2
    canvas.paste(img, (left, top))

    out = io.BytesIO()
    canvas.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    out.seek(0)
    return out

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    files = request.files.getlist("images")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    if len(files) == 1:
        f = files[0]
        result = process_image(f.read())
        name = os.path.splitext(f.filename)[0] + ".jpg"
        return send_file(result, mimetype="image/jpeg",
                         as_attachment=True, download_name=name)

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            result = process_image(f.read())
            name = os.path.splitext(f.filename)[0] + ".jpg"
            zf.writestr(name, result.read())
    zip_buf.seek(0)
    return send_file(zip_buf, mimetype="application/zip",
                     as_attachment=True, download_name="resized_images.zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
