# Portfolio AWS CDK Stack

This repository contains the infrastructure and application code for deploying a serverless professional portfolio website using AWS CDK, Lambda, API Gateway, Route 53, and ACM.

---

## Stack Overview

- **AWS Lambda**: Runs the Flask application.
- **API Gateway**: Serves as the HTTP endpoint for the Lambda function.
- **Route 53**: Manages DNS records for custom domains.
- **ACM (AWS Certificate Manager)**: Provides SSL certificates for HTTPS.
- **S3**: (Optional) Hosts large static files like videos or PDFs.

---

## Deployment Process

### 1. Prerequisites

- AWS CLI configured with appropriate permissions
- AWS CDK installed (`npm install -g aws-cdk`)
- Python 3.11+ and `pip` installed
- Your domain managed in Route 53

### 2. Clone the Repository

```sh
git clone https://github.com/lucas-gutknecht/portfolio.git
cd portfolio
```

### 3. Set Up Python Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment

Update your configuration (e.g., `prod.ini` or environment variables) with:
- `domain_name=www.xxxxx.com`
- `zone_name=www.xxxxx.com`
- `certificate=arn:aws:acm:us-east-1:YOUR_CERTIFICATE_ARN`

### 5. Bootstrap CDK (first time only)

```sh
cdk bootstrap
```

### 6. Deploy the Stack

```sh
cdk deploy
```

### 7. DNS Setup

- Ensure your Route 53 hosted zone is for your domain name.
- The stack creates an **A (Alias)** record for `www` pointing to your API Gateway custom domain.

### 8. ACM Certificate

- Request a certificate for both `www.xxxx.com` in ACM.
- Use DNS validation and ensure the certificate is **issued** before deploying.

---

## Serving Static Files

- Small static files (images, CSS, JS) are served by Flask from the `/static` directory.
- For large files (videos, PDFs), upload to S3 and reference the S3 URL in your HTML.

---

## Google Search Console

- Add the verification HTML file or meta tag to your Flask app/templates.
- After verification, submit your sitemap and request indexing in Search Console.

---

## Troubleshooting

- **Forbidden/Error:** Check API Gateway custom domain and base path mapping.
- **Static files not loading:** Ensure files are included in the Lambda package and correct binary media types are set in API Gateway.
- **PDF/video not displaying:** Serve large files from S3 for best results.

---

## License

MIT License

---

**Questions?**  
Open an issue or contact [lucas-gutknecht](https://github.com/lucas-gutknecht).