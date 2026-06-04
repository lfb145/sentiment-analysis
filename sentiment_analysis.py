#!/usr/bin/env python3
"""
Sentiment Analysis Script
Performs sentiment analysis on Facebook comments
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def analyze_sentiment(text):
    """
    Analyze sentiment of text using TextBlob
    
    Parameters:
    -----------
    text : str
        Text to analyze
    
    Returns:
    --------
    tuple
        (polarity, subjectivity, sentiment_label)
    """
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0, 0, 'neutral'
    
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment
        if polarity > 0.1:
            label = 'positive'
        elif polarity < -0.1:
            label = 'negative'
        else:
            label = 'neutral'
        
        return polarity, subjectivity, label
    except:
        return 0, 0, 'neutral'

def get_sentiment_statistics(df, sentiment_column='sentiment_label'):
    """
    Calculate sentiment statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataframe with sentiment column
    sentiment_column : str
        Name of sentiment column
    
    Returns:
    --------
    dict
        Sentiment statistics
    """
    stats = {
        'total_comments': len(df),
        'positive_count': (df[sentiment_column] == 'positive').sum(),
        'negative_count': (df[sentiment_column] == 'negative').sum(),
        'neutral_count': (df[sentiment_column] == 'neutral').sum(),
        'avg_polarity': df['sentiment_polarity'].mean(),
        'avg_subjectivity': df['sentiment_subjectivity'].mean(),
    }
    
    stats['positive_pct'] = (stats['positive_count'] / stats['total_comments']) * 100
    stats['negative_pct'] = (stats['negative_count'] / stats['total_comments']) * 100
    stats['neutral_pct'] = (stats['neutral_count'] / stats['total_comments']) * 100
    
    return stats

def analyze_engagement_by_sentiment(df):
    """
    Analyze engagement metrics by sentiment
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with sentiment and engagement columns
    
    Returns:
    --------
    pd.DataFrame
        Engagement metrics by sentiment
    """
    engagement_analysis = df.groupby('sentiment_label').agg({
        'engagement_score': ['mean', 'median', 'std'],
        'likes': ['mean', 'median'],
        'love_reactions': 'mean',
        'haha_reactions': 'mean',
        'wow_reactions': 'mean',
        'sad_reactions': 'mean',
        'angry_reactions': 'mean',
        'comment_length': ['mean', 'median'],
        'emoji_count': 'mean',
    }).round(2)
    
    return engagement_analysis

def get_sentiment_by_reaction_type(df):
    """
    Analyze sentiment distribution across reaction types
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataframe
    
    Returns:
    --------
    dict
        Sentiment distribution by reaction type
    """
    reactions = ['love_reactions', 'haha_reactions', 'wow_reactions', 
                 'sad_reactions', 'angry_reactions']
    
    result = {}
    for reaction in reactions:
        # Get comments with this reaction
        df_with_reaction = df[df[reaction] > 0]
        
        if len(df_with_reaction) > 0:
            sentiment_dist = df_with_reaction['sentiment_label'].value_counts(normalize=True) * 100
            result[reaction.replace('_reactions', '')] = sentiment_dist.to_dict()
    
    return result

def perform_sentiment_analysis(input_file='facebook_data_processed.csv',
                              output_file='facebook_data_with_sentiment.csv'):
    """
    Perform complete sentiment analysis
    
    Parameters:
    -----------
    input_file : str
        Path to processed CSV file
    output_file : str
        Path to save file with sentiment analysis
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with sentiment analysis
    """
    
    print("Loading processed data...")
    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print("\nPerforming sentiment analysis on comments...")
    sentiment_results = df['comment_text_cleaned'].apply(analyze_sentiment)
    
    df['sentiment_polarity'] = sentiment_results.apply(lambda x: x[0])
    df['sentiment_subjectivity'] = sentiment_results.apply(lambda x: x[1])
    df['sentiment_label'] = sentiment_results.apply(lambda x: x[2])
    
    print("\n=== SENTIMENT ANALYSIS RESULTS ===")
    stats = get_sentiment_statistics(df)
    
    print(f"\nTotal comments analyzed: {stats['total_comments']}")
    print(f"\nSentiment Distribution:")
    print(f"  Positive: {stats['positive_count']} ({stats['positive_pct']:.1f}%)")
    print(f"  Negative: {stats['negative_count']} ({stats['negative_pct']:.1f}%)")
    print(f"  Neutral:  {stats['neutral_count']} ({stats['neutral_pct']:.1f}%)")
    print(f"\nAverage Metrics:")
    print(f"  Sentiment Polarity: {stats['avg_polarity']:.3f}")
    print(f"  Sentiment Subjectivity: {stats['avg_subjectivity']:.3f}")
    
    print("\n=== ENGAGEMENT METRICS BY SENTIMENT ===")
    engagement_analysis = analyze_engagement_by_sentiment(df)
    print(engagement_analysis)
    
    print("\n=== SENTIMENT BY REACTION TYPE ===")
    sentiment_by_reaction = get_sentiment_by_reaction_type(df)
    for reaction, distribution in sentiment_by_reaction.items():
        print(f"\n{reaction.upper()} reactions:")
        for sentiment, pct in distribution.items():
            print(f"  {sentiment}: {pct:.1f}%")
    
    # Save analyzed data
    df.to_csv(output_file, index=False)
    print(f"\n✓ Analysis saved to: {output_file}")
    
    # Display samples
    print("\n=== SAMPLE COMMENTS BY SENTIMENT ===")
    for sentiment in ['positive', 'negative', 'neutral']:
        sample = df[df['sentiment_label'] == sentiment][['comment_text', 'sentiment_polarity']].head(2)
        print(f"\n{sentiment.upper()} examples:")
        for idx, row in sample.iterrows():
            print(f"  - {row['comment_text'][:60]}... (score: {row['sentiment_polarity']:.2f})")
    
    return df

if __name__ == "__main__":
    perform_sentiment_analysis()
