# InlineX Image Resizer

A simple web tool to batch-resize product images to **800×800px JPEG** for fast web loading.

## Resize Logic
- Scale by **height** first → fills top & bottom edges, white bars on sides if needed
- If image would overflow sides → scale by **width** instead → fills sides, white bars top/bottom
- **Nothing is ever cropped.** White background padding fills any gaps.

## Local Dev

```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

## Deploy to Railway

1. Push this repo to GitHub under `arcintscooters-maker/image-resizer`
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select the repo — Railway auto-detects Python and deploys
4. Your app will be live at a `*.railway.app` URL

No environment variables needed.
