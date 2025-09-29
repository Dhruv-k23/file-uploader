# Simple File Uploader with AWS S3 Integration

A small web app that allows users to upload files (images or text) to AWS S3 cloud storage, built with Flask and deployed on Vercel.

---

## Live Demo

Check out the live app here:  
https://file-uploader-peach.vercel.app/

---

## Project Overview

This project demonstrates building a serverless-friendly file uploader with cloud storage integration using:

- **Frontend:** A basic HTML upload form (served by Flask).
- **Backend:** Flask API handling file uploads.
- **Cloud Storage:** AWS S3 for storing uploaded files.
- **Deployment:** Vercel for serverless hosting.

The app securely uploads files to an S3 bucket and returns a public URL for access.

---

## Features

- File upload via simple HTML form.
- Backend file processing with Flask.
- Stores files in AWS S3 bucket.
- Returns a public URL to the uploaded file.
- Supports file size limits (up to 5 MB).
- Accepts only specific file types (PNG, JPEG, plain text).
- Secure file name handling.
- Easy deployment on Vercel with appropriate build and routing config.
- Environment variables securely manage AWS credentials.

---

## How It Works

### Frontend

- User selects a file through the HTML input form.
- The form submits the file via POST to the `/upload` endpoint.

### Backend

- Flask receives the file and validates:
  - File presence.
  - File size (<= 5MB).
  - File MIME type (PNG, JPEG, plain text).
- The file name is sanitized using `secure_filename`.
- File is streamed and uploaded to AWS S3 using `boto3`.
- A public URL to the uploaded file in the S3 bucket is returned as JSON.

---

## Deployment on Vercel

- Uses `@vercel/python` builder for serverless Python functions.
- Routing configured in `vercel.json` to direct requests to `api/app.py`.
- AWS credentials and bucket details are stored securely as environment variables in Vercel project settings.

---

## Project Structure

-/api
-└── app.py # Flask backend API
-/index.html # Simple file upload HTML form
-/vercel.json # Vercel build and route config
-/assets # (Optional) Folder to store screenshots and images for README
-README.md # This README file


---

## Environment Variables

Set the following environment variables in your Vercel project settings:

- `AWS_ACCESS_KEY_ID` - Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret access key.
- `S3_BUCKET_NAME` - Your AWS S3 bucket name.
- `S3_REGION` - (Optional) AWS region, defaults to `us-east-1` if not set.

---

## Screenshots

_Add screenshots of the app and deployment here._  
![Upload Form](./assets/upload-form.png)  
![Successful Upload](./assets/upload-success.png)

---

## Usage

1. Navigate to the live app URL.
2. Choose a file (PNG, JPEG, or TXT).
3. Click upload.
4. Receive the URL to access your file in S3.

---

## Notes

- Make sure your S3 bucket has proper CORS and public-read policies set for accessing uploaded files.
- File size and type restrictions are configurable in the backend.
