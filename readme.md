# 👁️🧠 Diabetic Retinopathy Detection System

An AI-powered web-based system for analyzing **retina fundus images** and managing **patient medical records**, designed to assist in early detection of **diabetic retinopathy**.

---

## 🔗👨‍💻 Team

| Name                  | Roll Number  |
| --------------------- | ------------ |
| Mohammed Siddiq Ahmed | 160922748124 |
| Mohammed Zohaib Adeel | 160922748129 |
| Syed Bilal Quadri     | 160922748154 |
---

## 🖼️ Sample Image Specifications

Ensure all uploaded retinal images meet the following standards:

* 📁 **Formats:** JPEG, PNG, TIFF
* 📐 **Recommended Resolution:** 800×600 to 2000×1500 pixels
* 💾 **File Size:** Less than 10MB
* 🔴 **Content:** Retina fundus images (reddish background with visible blood vessels)

---

## 🧰 Tech Stack

* 🐍 Python 3.11.9
* 🌐 Django 4.2.7
* 🗄 MySQL
* 🎨 Bootstrap 5
* 🤖 OpenCV (Image Processing)
* 📊 Pandas, NumPy, Matplotlib
* 📄 ReportLab & WeasyPrint (Reports)
* ⚙️ Celery + Redis (Async Tasks)

---

## 📦 Requirements

```txt
Django==4.2.7
mysqlclient==2.1.1
Pillow==10.0.1
opencv-python==4.8.1.78
matplotlib==3.7.2
pandas==2.1.1
reportlab==4.0.5
openpyxl==3.1.2
celery==5.3.4
redis==5.0.1
django-crispy-forms==2.0
crispy-bootstrap5==0.7
python-decouple==3.8
weasyprint==61.0
numpy==1.24.3
```

---

## ⚙️ Setup Instructions

### 1️⃣ Open Project Folder

```bash
cd D:\Retina_Project
```

### 2️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Database (MySQL)

```sql
CREATE DATABASE retina_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'retina_user'@'localhost' IDENTIFIED BY 'retina_pass';
GRANT ALL PRIVILEGES ON retina_db.* TO 'retina_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🌐 Access URLs

| Page            | URL                                                                |
| --------------- | ------------------------------------------------------------------ |
| 🔐 Login        | [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)       |
| 📝 Register     | [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/) |
| 📊 Dashboard    | [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)         |
| 🧪 Upload Image | [http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/)     |
| 📄 Reports      | [http://127.0.0.1:8000/reports/](http://127.0.0.1:8000/reports/)   |
| ⚙️ Admin Panel  | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)       |

---

## 👨‍⚕️ Sample Patient Details

### 🧾 Patient 1

* **Patient ID:** PT001
* **Name:** John Smith
* **DOB:** 1985-03-15
* **Gender:** Male

📞 **Contact Info**

* Phone: 8142266301
* Email: [john.smith@email.com](mailto:john.smith@email.com)
* Address: 123 Main St, Cityville

---

### 🩺 Medical History Records

#### 📌 Record 1

* Type 2 Diabetes (Diagnosed: 2018)
* HbA1c: 7.2%
* Medication: Metformin 500mg (Twice Daily)
* No other major conditions

#### 📌 Record 2

* Type 2 Diabetes (Diagnosed: 2010)
* Previous laser treatment (Diabetic Retinopathy)
* Hypertension (Controlled)
* HbA1c: 8.1%

#### 📌 Record 3

* Type 1 Diabetes (Diagnosed: 2005)
* Retinopathy Stage: Mild NPDR
* HbA1c: 6.8%
* Regular insulin therapy

---

## 👥 User Roles

| Role         | Access                                    |
| ------------ | ----------------------------------------- |
| 👑 Admin     | Full control, patient & system management |
| 🧑‍⚕️ Doctor | Upload images, view reports               |
| 👁 Viewer    | Read-only access                          |

---

## 📊 Features

* 👁️ Retina Image Upload & Processing
* 🤖 AI-based Disease Detection
* 🧾 Patient Record Management
* 📄 Automated Report Generation
* 📊 Dashboard Analytics
* 🔒 Secure Authentication System

---

## 🚀 Project Highlights

* Early detection of **Diabetic Retinopathy**
* Integration of **AI + Healthcare**
* Supports real-world retinal imaging formats
* Scalable Django-based architecture

---

## 🛠 Troubleshooting

| Error               | Solution                |
| ------------------- | ----------------------- |
| Database error      | Ensure MySQL is running |
| Module not found    | Install requirements    |
| Image upload fails  | Check format & size     |
| Static files issue  | Run collectstatic       |
| Server not starting | Check environment       |
