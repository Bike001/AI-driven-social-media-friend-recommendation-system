# AI-Driven Social Media Friend Recommendation System

This repository contains the code for an AI-driven social media friend recommendation system that analyzes user messages, labels emotions, and recommends friends based on a rule-based system.

## System Structure

![Structure of the System](Structure%20of%20the%20system.png)

*Figure 1: Structure of the System*

## Frontend

The frontend is built with React and allows users to interact with the system. Screenshots of the homepage and friends page are shown below.

### Homepage

<img width="720" alt="image" src="https://github.com/Bike001/AI-driven-social-media-friend-recommendation-system/assets/114451652/fc1f9bad-8688-42c5-82e4-9f82c565db1f">

*Figure 2: Screenshot of Website Homepage*

### Friends Page

<img width="730" alt="image" src="https://github.com/Bike001/AI-driven-social-media-friend-recommendation-system/assets/114451652/b97531d5-8688-4ead-b885-aec202ede4f7">


*Figure 3: Screenshot of Friend Recommendation Page*

## Backend

The backend is developed in Python Django. It handles sentiment analysis, data management, and the rule-based logic for friend recommendation.

### Sentiment Analysis Result

![Sentiment Analysis Result](Sentiment%20Analysis%20Result.png)

*Figure 4: Screenshot of Sentiment Analysis Result*

## Pretrained Model

We use a pretrained model for sentiment analysis from Hugging Face, capable of detecting various emotions in text.

**Model URL**: [Roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions)

**Emotions Detected**:

- Admiration
- Amusement
- Anger
- Annoyance
- ... (and so on for all labels)

## How to Use

1. **Clone the Repository:**
git clone https://github.com/Bike001/AI-driven-social-media-friend-recommendation-system-.git
2. **Navigate to the Project Directory:**
3. **Extract All Zip Files (if any are present):**
Make sure all the required zip files are extracted.
4. **Frontend Setup:**
- Open a terminal window and navigate to the `my-social-media-app` directory:
  ```
  cd my-social-media-app
  ```
- Install the npm packages:
  ```
  npm install
  ```
- Start the frontend server:
  ```
  npm start
  ```

5. **Backend Setup:**
- Open another terminal window and navigate to the `social_media_backend` directory:
  ```
  cd social_media_backend
  ```
- Set up a virtual environment (optional but recommended):
  ```
  python3 -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
- Install the required Python packages:
  ```
  pip install -r requirements.txt
  ```
- Start the backend server:
  ```
  python manage.py runserver
  ```
5. **Prolog Setup:**
- Download Prolog

- Start the Prolog server:
 swipl emotions_api_server.pl

Now you have three servers running: the React frontend on the default port 3000 , the Django backend on port 8000 and the Prolog server for Rule-based system.

## Contributions

Currently, the project is managed by me, and I am not looking for external contributions. However, if you have suggestions or feedback, please feel free to reach out.

## License

MIT License

Copyright (c) [2024] [Bike001]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---
