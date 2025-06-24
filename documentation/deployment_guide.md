# 🚀 Medical AI Scheduler — EC2 Deployment Guide

This guide explains how to deploy your Streamlit-based Medical Appointment Scheduler to an Amazon EC2 instance.

---

## ✅ Prerequisites

- An AWS account
- EC2 instance (Amazon Linux 2 recommended)
- Your project files copied to EC2
- A `.pem` SSH key to access EC2

---

## 🖥️ 1. Connect to EC2

```bash
ssh -i medical-key.pem ec2-user@<your-ec2-public-ip>
```

---

## 🧱 2. Install System Dependencies

```bash
sudo yum update -y
sudo yum install git unzip gcc openssl-devel bzip2-devel libffi-devel -y
```

---

## 🐍 3. Install Python 3.10

```bash
cd /usr/src
sudo curl -O https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
sudo tar xzf Python-3.10.12.tgz
cd Python-3.10.12
sudo ./configure --enable-optimizations
sudo make altinstall
python3.10 --version
```

---

## 🧪 4. Create Virtual Environment

```bash
cd ~/Medical-Ai-Scheduler
python3.10 -m venv venv
source venv/bin/activate
```

---

## 📦 5. Install Python Dependencies

Update `requirements.txt` to:

```txt
streamlit
cryptography
python-dotenv
boto3>=1.26,<1.35
tenacity
```

Then run:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 6. Configure `.env` for AWS Bedrock

Create a `.env` file:

```bash
nano .env
```

Paste:

```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

Replace values with your real credentials.

---

## 🌍 7. Allow Web Access to Port 8501

1. Go to **AWS EC2 Console**
2. Click your instance → Security Groups → Inbound Rules → Edit
3. Add a rule:
   - Type: **Custom TCP**
   - Port: `8501`
   - Source: **0.0.0.0/0** (or "My IP")

---

## ▶️ 8. Run the App

```bash
cd ~/Medical-Ai-Scheduler
source venv/bin/activate
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Visit:

```bash
http://<your-ec2-public-ip>:8501
```

---

## 🔄 Optional: Auto-start Script

Create a shell script named `start.sh`:

```bash
#!/bin/bash
cd ~/Medical-Ai-Scheduler
source venv/bin/activate
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Make it executable:

```bash
chmod +x start.sh
```

To run after reboot, you can add it to `crontab` or `rc.local`.

---

## 🧹 Tips

- Always use `http://` not `https://`
- Use `screen` or `tmux` if you want it to keep running after you close SSH
- Protect your `.env` and `.pem` files

---

✅ You're live!