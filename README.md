# 🏛️ CivicConnect - AI-Powered Municipal Issue Reporting System

CivicConnect is a web-based platform that allows citizens to report municipal issues by uploading photos. The system uses AI to automatically categorize issues into different departments (Roads, Water, Electricity, Waste, Safety, Other) for faster response times.

![CivicConnect Homepage](https://github.com/user-attachments/assets/bda8ee58-b51c-494b-bc87-34268b494af5)

## ✨ Features

- **AI-Powered Classification**: Automatically categorizes uploaded images using a trained ResNet-50 model
- **User-Friendly Interface**: Clean, responsive web design with drag-and-drop functionality
- **Real-time Analysis**: Instant feedback with category prediction and next steps
- **Mobile-Responsive**: Works seamlessly across desktop and mobile devices
- **Error Handling**: Comprehensive error handling and user feedback

## 🏗️ Architecture

- **Frontend**: HTML/CSS/JavaScript with responsive design
- **Backend**: Node.js/Express server for API proxy and static file serving
- **ML Model**: Python/PyTorch ResNet-50 model with FastAPI endpoint
- **Categories**: Roads, Water, Electricity, Waste, Safety, Other

## 🚀 Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- Python 3.8+ with pip
- At least 4GB RAM for model training

### 1. Install ML Dependencies

```bash
cd model
pip install -r requirements_clean.txt
```

### 2. Train the Model (First time only)

```bash
cd model
python model.py
```

This will:
- Download the pre-trained ResNet-50 model
- Train on the provided dataset
- Save the model as `issue_reporting_model.pth`

### 3. Start ML API Server

```bash
cd model
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Install Backend Dependencies

```bash
cd backend
npm install
```

### 5. Start Web Server

```bash
cd backend
npm start
```

The application will be available at http://localhost:3000

## 📱 Usage

1. **Upload Image**: Drag and drop or click to browse for an image of a municipal issue
2. **Analyze**: Click "Analyze Issue" to get AI classification
3. **View Results**: See the predicted category, assessment, and next steps
4. **Report Another**: Click "Report Another Issue" to submit more reports

![Analysis Results](https://github.com/user-attachments/assets/63352f7c-b4cf-4456-8974-8428c51610ff)

## 🗂️ Project Structure

```
├── backend/          # Node.js Express server
│   ├── package.json  # Backend dependencies
│   └── server.js     # Main server file
├── frontend/         # Web UI files
│   ├── index.html    # Main HTML page
│   ├── styles.css    # CSS styles
│   └── script.js     # JavaScript functionality
├── model/            # ML model and API
│   ├── api.py        # FastAPI server
│   ├── model.py      # Model training script
│   ├── dataset/      # Training dataset
│   └── training/     # Training images and CSV
└── README.md         # This file
```

## 🎯 Issue Categories

| Category | Icon | Examples |
|----------|------|----------|
| Roads | 🛣️ | Potholes, damaged pavement, road signs |
| Water | 💧 | Leaks, drainage issues, water quality |
| Electricity | ⚡ | Power outages, damaged lines, streetlights |
| Waste | 🗑️ | Overflowing bins, illegal dumping |
| Safety | ⚠️ | Damaged equipment, hazardous conditions |
| Other | 📋 | General municipal issues |

## 🔧 Development

### API Endpoints

- `GET /` - Serve frontend application
- `POST /api/predict` - Upload image for classification
- `GET /api/health` - Health check endpoint

### Model Training

The model uses transfer learning with ResNet-50:
1. Initial training on the full dataset (5 epochs)
2. Fine-tuning on individual images
3. Model saved as PyTorch state dict (.pth file)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the complete flow
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- ResNet-50 model from torchvision
- FastAPI for ML API development
- Express.js for web server
- Municipal issue dataset for training

---

Made with ❤️ for better communities through technology.