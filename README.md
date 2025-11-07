# 🎓 Thinkora - AI-Powered Smart Study Assistant

<div align="center">

![Thinkora Logo](frontend/public/thinkora-logo.png)

**Transform how you prepare for exams with intelligent analysis, personalized quizzes, and comprehensive learning insights.**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/thinkora)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

[Live Demo](#) | [Documentation](DEPLOYMENT_GUIDE.md) | [Quick Start](#-quick-start)

</div>

---

## ✨ Features

### 📚 Smart Document Analysis

- Upload PDFs, DOCX, notes, and past papers
- AI extracts questions with actual marks
- Identifies patterns and important topics
- Categorizes by frequency and importance

### 🧠 AI-Powered Quizzes

- **20 unique questions** per quiz attempt
- **Different questions** every time
- Real answers extracted from your materials
- Unlimited attempts with variety
- **Downloadable question banks** (CSV)

### 💡 Intelligent Explanations

- Step-by-step detailed explanations
- Interactive visual diagrams
- Exam tips and memory techniques
- Marks breakdown and time allocation

### 📊 Learning Analytics

- AI feedback on mastery level
- Performance tracking by topic
- Identifies strong and weak areas
- Progress monitoring over time
- **Personalized recommendations**

### 📈 Progress Tracking

- Complete quiz history
- Improvement trend analysis
- Best score and average tracking
- Session-based organization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/thinkora.git
cd thinkora
```

2. **Start Backend:**

```bash
cd backend
pip install -r requirements.txt
python start.py
```

3. **Start Frontend:**

```bash
cd frontend
npm install
npm run dev
```

4. **Open:** http://localhost:5173

---

## 🌐 Deployment

### Deploy to Vercel + Render (Free)

**Quick Deploy (15 minutes):**

1. Push code to GitHub
2. Deploy backend to [Render](https://render.com)
3. Deploy frontend to [Vercel](https://vercel.com)
4. Update environment variables

**Detailed Guide:** See [DEPLOY_NOW.md](DEPLOY_NOW.md)

---

## 🛠️ Tech Stack

### Frontend

- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - API calls

### Backend

- **FastAPI** - Python web framework
- **Python 3.11** - Programming language
- **scikit-learn** - ML algorithms
- **PyPDF2** - PDF processing
- **python-docx** - Document processing

### AI/ML

- **NLP Analysis** - Question extraction
- **TF-IDF** - Text analysis
- **Question Classification** - Smart categorization
- **AI Question Generation** - Quiz creation

---

## 📁 Project Structure

```
thinkora/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   └── App.jsx          # Main app component
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── ai_engine/           # AI/ML modules
│   │   ├── question_generator.py
│   │   ├── question_classifier.py
│   │   └── nlp_analysis.py
│   ├── routes/              # API endpoints
│   │   ├── analysis.py
│   │   ├── quiz.py
│   │   └── explanations.py
│   ├── models/              # Data models
│   ├── utils/               # Utilities
│   └── main.py              # FastAPI app
│
├── DEPLOYMENT_GUIDE.md      # Comprehensive deployment guide
├── DEPLOY_NOW.md            # Quick deployment steps
└── README.md                # This file
```

---

## 🎯 How It Works

1. **Upload Documents** → Upload PDFs, notes, past papers
2. **AI Analysis** → Extracts questions, identifies patterns
3. **Smart Categorization** → Frequent, Moderate, Important, Predicted
4. **Get Explanations** → Detailed AI-powered explanations with diagrams
5. **Take Quizzes** → 20 questions, different every time
6. **Track Progress** → AI feedback, performance analytics
7. **Download** → Export questions as CSV for offline study

---

## 🎨 Screenshots

### Home Page

![Home](docs/screenshots/home.png)

### Question Analysis

![Analysis](docs/screenshots/analysis.png)

### Quiz Interface

![Quiz](docs/screenshots/quiz.png)

### AI Feedback

![Feedback](docs/screenshots/feedback.png)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ for students worldwide
- Powered by AI and machine learning
- Inspired by the need for smarter study tools

---

## 📞 Contact

**Project Link:** https://github.com/yourusername/thinkora

**Live Demo:** https://thinkora.vercel.app

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/thinkora&type=Date)](https://star-history.com/#yourusername/thinkora&Date)

---

<div align="center">

**Made with 🧠 by Thinkora Team**

[Website](#) • [Documentation](DEPLOYMENT_GUIDE.md) • [Report Bug](#) • [Request Feature](#)

</div>

---

## Thinkora – Your Smart Study Aura

**Tagline:** "Think Smarter. Study Better."

## 🎯 Project Overview

Thinkora is an intelligent study assistant that helps students prepare for exams by analyzing their study materials and generating smart question sets.

## 🚀 Features

- Subject-specific AI assistance
- Upload and analyze PYQs, notes, and syllabus
- Smart question categorization (Frequent, Moderate, Important, Predicted)
- AI-powered explanations and short notes
- Modern React + Tailwind UI

## 🛠️ Tech Stack

- **Frontend:** React + Tailwind CSS
- **Backend:** Python FastAPI
- **Database:** MongoDB
- **AI:** OpenAI API integration
- **NLP:** spaCy, NLTK

## 📦 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment (recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download spaCy model:

```bash
python -m spacy download en_core_web_sm
```

5. Setup environment variables:

```bash
cp .env.example .env
# Edit .env file with your MongoDB URL and OpenAI API key
```

6. Start the server:

```bash
python start.py
# or
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm run dev
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🎨 Brand Colors

- Primary Blue: #3B82F6
- Primary Purple: #8B5CF6
- Gradient theme throughout the app

---

**Powered by Thinkora AI**

## 🔧 Configuration

### Environment Variables (.env)

```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=thinkora
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True
LOG_LEVEL=INFO
```

## 📁 Project Structure

```
thinkora/
├── backend/
│   ├── ai_engine/
│   │   ├── question_classifier.py
│   │   └── nlp_analysis.py
│   ├── database/
│   │   └── db_connection.py
│   ├── models/
│   │   └── schemas.py
│   ├── routes/
│   │   ├── subjects.py
│   │   ├── analysis.py
│   │   └── explanations.py
│   ├── main.py
│   ├── start.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚀 Features in Detail

### AI-Powered Question Classification

- **Frequent Questions**: Common questions that appear regularly
- **Moderate Questions**: Standard difficulty questions
- **Important Questions**: High-weightage exam questions
- **Predicted Questions**: AI-predicted future exam questions

### Document Analysis

- Upload PYQs, notes, and syllabus in text format
- Automatic question extraction using NLP
- Similarity analysis and clustering
- Topic and difficulty assessment

### Smart Explanations

- Detailed AI-generated explanations
- Key points extraction
- Exam-specific tips and strategies
- Context-aware responses based on subject

## 🔮 Future Enhancements

- [ ] Support for PDF and Word documents
- [ ] Advanced question difficulty prediction
- [ ] Progress tracking and analytics
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Collaborative study features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## 🔧 Troubleshooting

### Common Issues

1. **spaCy model not found**

   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **MongoDB connection error**

   - Ensure MongoDB is running
   - Check MONGODB_URL in .env file

3. **OpenAI API errors**

   - Verify API key in .env file
   - Check API quota and billing

4. **Frontend build errors**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
