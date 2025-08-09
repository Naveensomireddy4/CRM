# Client Relationship Management System (CRM)
A **Full-Stack Web Application** built with **Django REST Framework**, **React**, and **PostgreSQL** that enables organizations to manage client relationships, assign leads, and track progress in real-time.

## 📌 Overview
This CRM application is designed for **small to medium-sized organizations** to efficiently manage **Organizers** (organization heads), **Agents** (field employees), and **Leads** (clients).  
It provides **role-based access**, a **real-time dashboard**, and tools for **categorizing leads** based on work type or industry.

## 🚀 Features
### Authentication & Roles
- **Role-based Access Control** with three distinct user types:
  - **Organizer** – Organization head with full access
  - **Agent** – Field employee who manages assigned leads
  - **Lead** – Client information stored for tracking
- Secure **JWT Authentication** (Django REST Framework)

### Lead Management
- Organizers can:
  - Create **agents** and **leads**
  - Assign leads to specific agents
  - Classify leads into **custom categories**
- Agents can:
  - View assigned leads
  - Update lead status in real-time

### Real-Time Dashboard
- Displays **current status** of all leads
- Tracks **lead progress updates** instantly for both organizers and agents

### Tech Stack
- **Backend** – Django REST Framework (API)
- **Frontend** – React.js (UI)
- **Database** – PostgreSQL
- **Authentication** – JWT
- **Deployment** – Docker (optional)

## 📂 Project Structure
```
crm-system/
│
├── backend/                 # Django REST Framework API
│   ├── crm/                 # Core application
│   ├── users/               # User authentication and roles
│   ├── leads/               # Lead management
│   ├── requirements.txt     # Backend dependencies
│
├── frontend/                # React frontend
│   ├── src/                 # React components, pages, hooks
│   ├── package.json         # Frontend dependencies
│
├── docker-compose.yml       # Multi-container setup (optional)
└── README.md
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/crm-system.git
cd crm-system
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Backend runs at: **http://localhost:8000**

### 3️⃣ Frontend Setup
```bash
cd ../frontend
npm install
npm start
```
Frontend runs at: **http://localhost:3000**

## 🧪 Usage
1. **Login** as an Organizer or Agent.
2. **Organizers** can:
   - Create agents & leads
   - Assign leads to agents
   - Categorize leads
3. **Agents** can:
   - View assigned leads
   - Update status
4. **Dashboard** updates in real-time.

## 🔐 Authentication
- JWT-based authentication for secure login
- Role-based permissions for different user types

## 📸 Screenshots
*(Add relevant screenshots of login page, dashboard, lead management, etc.)*

## 🛠 Future Enhancements
- Email notifications for lead status changes
- Drag-and-drop Kanban view for leads
- Analytics dashboard with charts
- Mobile-responsive improvements

## 👨‍💻 Author
**Somireddy Naveen Kumar Reddy**  
📧 [naveensomireddy2112@gmail.com](mailto:naveensomireddy2112@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/naveen-kumar-reddy-somi-reddy-1b1ab2246/) | [GitHub](https://github.com/Naveensomireddy4)
