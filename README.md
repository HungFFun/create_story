# Story Video Generator

> Ứng dụng tự động chuyển đổi nội dung từ Google Docs thành video với text-to-speech và background image.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📑 Mục lục
- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#%EF%B8%8F-cài-đặt)
- [Cấu trúc Project](#-cấu-trúc-project)
- [Cách sử dụng](#-cách-sử-dụng)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [License](#-license)

## 🌟 Tính năng

- Đọc và xử lý nội dung từ Google Docs
- Tự động chia nhỏ văn bản tối ưu (4000 ký tự/đoạn)
- Chuyển đổi text thành speech với OpenAI TTS
- Tạo video từ audio và background image
- Monitoring hiệu suất và logging chi tiết

## 💻 Yêu cầu hệ thống

- Python 3.8+
- FFmpeg
- Disk space: 1GB+
- RAM: 4GB+
- Google Cloud Project (Docs API enabled)
- OpenAI API key

## ⚙️ Cài đặt

1. Clone repository:
bash
git clone https://github.com/your-username/story-video-generator.git
cd story-video-generator

2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo và cấu hình file .env:
```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
OPENAI_API_KEY=your-api-key
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=4000
VIDEO_FPS=24
```

## 📁 Cấu trúc Project

```
story_processor/
├── src/
│   ├── services/           # Core services
│   │   ├── google_docs_service.py
│   │   ├── text_processor.py
│   │   ├── tts_service.py
│   │   └── video_processor.py
│   └── utils/             # Utility functions
│       ├── logger.py
│       ├── file_helper.py
│       ├── validation_helper.py
│       └── performance_monitor.py
├── assets/                # Static resources
├── output/               # Generated files
├── logs/                # Application logs
├── tests/               # Test files
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Cách sử dụng

1. Basic Usage:
```python
from src.main import StoryVideoGenerator

generator = StoryVideoGenerator()
video_path = generator.process_story(
    doc_id='your-google-doc-id',
    background_image='path/to/background.jpg'
)
```

2. Output Structure:
```
output/
└── [Story_Name]/
    ├── text/         # Split text files
    ├── audio/        # Generated audio files
    ├── segments/     # Video segments
    └── final/        # Final video
```

## 🔍 Troubleshooting

### Common Issues

1. Google Docs API Errors:
- Kiểm tra credentials path và permissions
- Verify Document ID và access rights
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
ls -l $GOOGLE_APPLICATION_CREDENTIALS
```

2. OpenAI API Errors:
- Verify API key
- Check quota và billing
- Monitor rate limits

3. Video Processing Errors:
- Install FFmpeg:
```bash
# Ubuntu/Debian
apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Logs
- Location: `logs/`
- Format: `{time} | {level} | {message}`
- Rotation: 10MB per file

## 🛠 Development

1. Running Tests:
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_video_processor.py

# With coverage
pytest --cov=src tests/
```

2. Code Style:
```bash
# Check style
flake8 src/

# Format code
black src/
```

3. Pre-commit:
```bash
pre-commit install
pre-commit run --all-files
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Support

- Issues: GitHub Issues
- Email: your.email@example.com