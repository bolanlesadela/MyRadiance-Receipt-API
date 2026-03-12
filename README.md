# MyRadiance Receipt API

A REST API that generates PDF receipts for cosmetics orders. Built with Python and Flask.

![Sample Receipt](sample-receipt.png)

## What it does

Send order data as JSON, get a downloadable PDF receipt back. Designed to simulate how receipt generation works in real e-commerce backends.

## Tech Stack

- Python 3
- Flask — REST API framework
- FPDF2 — PDF generation

## API Usage

**POST** `/generate-receipt`

Request body:
```json
{
  "customer": "Bolzy",
  "items": [
    {"name": "Glow Serum", "qty": 2, "price": 8500},
    {"name": "Lip Gloss", "qty": 1, "price": 3200}
  ]
}
```

Returns a downloadable PDF receipt.

## How to Run

1. Clone the repo
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
```
3. Install dependencies:
```bash
   pip install flask fpdf2
```
4. Run the server:
```bash
   python app.py
```
5. Test with Postman or any HTTP client at `http://127.0.0.1:5000`

## Author

**Omobolanle Sadela**  
[GitHub](https://github.com/bolanlesadela) · [LinkedIn](https://www.linkedin.com/in/omobolanle-sadela-7a486a1b4/)