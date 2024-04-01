# AI-Driven Social Media Friend Recommendation System

This repository contains the code for an AI-driven social media friend recommendation system that analyzes user messages, labels emotions, and recommends friends based on a rule-based system.

## System Structure

![Structure of the System](Structure%20of%20the%20system.png)

*Figure 1: Structure of the System*

## Frontend

The frontend is built with React and allows users to interact with the system. Screenshots of the homepage and friends page are shown below.

### Homepage

![Homepage Screenshot](Homepage.png)

*Figure 2: Screenshot of Website Homepage*

### Friends Page

![Friends Page Screenshot](FriendsPage.png)

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

Detailed instructions on how to set up and run the project locally would be provided here.

## Contributions

We welcome contributions. Please fork the repository, create a feature branch, and submit your pull requests for review.

## License

Specify the license under which this project is available.
