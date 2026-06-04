#!/usr/bin/env python3
"""
Data Preprocessing Script
Cleans and preprocesses Facebook text data
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import emoji

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    """
    Clean and preprocess text
    
    Parameters:
    -----------
    text : str
        Raw text to clean
    
    Returns:
    --------
    str
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags (keep the text)
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Convert emojis to text representation
    text = emoji.demojize(text, delimiters=(" ", " "))
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_emojis(text):
    """
    Extract emojis from text
    
    Parameters:
    -----------
    text : str
        Text containing emojis
    
    Returns:
    --------
    str
        Space-separated emoji names
    """
    if not isinstance(text, str):
        return ""
    
    emoji_list = []
    for char in text:
        if char in emoji.EMOJI_DATA:
            emoji_list.append(emoji.demojize(char, delimiters=("", "")))
    
    return ' '.join(emoji_list)

def preprocess_data(input_file='facebook_data_original.csv',
                    output_file='facebook_data_processed.csv'):
    """
    Load, clean, and preprocess Facebook data
    
    Parameters:
    -----------
    input_file : str
        Path to original CSV file
    output_file : str
        Path to save processed CSV file
    
    Returns:
    --------
    pd.DataFrame
        Processed dataframe
    """
    
    print("Loading data...")
    df = pd.read_csv(input_file)
    
    print(f"Original dataset shape: {df.shape}")
    
    # Create a copy for processing
    df_processed = df.copy()
    
    print("\nCleaning text data...")
    # Clean post text
    df_processed['post_text_cleaned'] = df_processed['post_text'].apply(clean_text)
    
    # Clean comment text
    df_processed['comment_text_cleaned'] = df_processed['comment_text'].apply(clean_text)
    
    # Extract emojis before cleaning
    print("Extracting emoji information...")
    df_processed['emojis_in_comment'] = df['comment_text'].apply(extract_emojis)
    df_processed['emoji_count'] = df_processed['emojis_in_comment'].apply(lambda x: len(x.split()) if x else 0)
    
    print("\nCalculating engagement metrics...")
    # Calculate total engagement score
    df_processed['total_reactions'] = (
        df_processed['love_reactions'] + 
        df_processed['haha_reactions'] + 
        df_processed['wow_reactions'] + 
        df_processed['sad_reactions'] + 
        df_processed['angry_reactions']
    )
    
    df_processed['engagement_score'] = df_processed['likes'] + df_processed['total_reactions']
    
    # Convert timestamp to datetime
    df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])
    
    # Extract time features
    df_processed['hour'] = df_processed['timestamp'].dt.hour
    df_processed['day_of_week'] = df_processed['timestamp'].dt.day_name()
    df_processed['date'] = df_processed['timestamp'].dt.date
    
    print("\nData quality checks...")
    print(f"Missing values:\n{df_processed.isnull().sum()}")
    
    # Remove any rows with empty cleaned text
    df_processed = df_processed[df_processed['comment_text_cleaned'].str.len() > 0]
    
    print(f"\nProcessed dataset shape: {df_processed.shape}")
    
    # Save processed data
    df_processed.to_csv(output_file, index=False)
    print(f"\n✓ Processed data saved to: {output_file}")
    
    # Display sample
    print("\nSample of processed data:")
    cols_to_show = ['comment_text', 'comment_text_cleaned', 'emoji_count', 
                    'likes', 'total_reactions', 'engagement_score']
    print(df_processed[cols_to_show].head(10))
    
    return df_processed

if __name__ == "__main__":
    preprocess_data()
