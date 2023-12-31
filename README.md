# Valorant Transcription App

This is a Streamlit application that transcribes audio or video files using the OpenAI Whisper API. The application allows users to upload files, enter their API key, and specify custom words to be emphasized in the transcription.

This is a work in progress to help creators lower their costs to produce accessible content. I will continue to improve the app as a side project over time. At the moment we're limited to 25mb files until I've built a splitter for longer clips. The audio of a 10-minute vid should be around 25 MB.

## Requirements

- Python 3.10
- OpenAI API key -> https://platform.openai.com/ to create an account and set up your own API key.

## Features

- Upload audio or video files for transcription
- Enter custom words to improve transcription accuracy
- View transcription results directly in the app

## Installation

1. Clone this repository: ```git clone https://github.com/Peakz/vid-subs.git```

2. Navigate to the project directory: ```cd location/vid-subs```

3. Create a virtual environment and activate it:
   - On Windows:
     - ```python -m venv venv```
     - ```.\venv\Scripts\activate```
   - On Unix or MacOS:
     - ```python3 -m venv venv```
     - ```source venv/bin/activate```

4. Install the required packages: ```pip install -r requirements.txt```

## Usage

1. Start the Streamlit app: ```streamlit run main.py```

2. Open your web browser and go to `http://localhost:8501` to view the app.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
