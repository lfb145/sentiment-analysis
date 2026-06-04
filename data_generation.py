#!/usr/bin/env python3
"""
Facebook Data Generation Script
Generates simulated Facebook dataset for sentiment analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_facebook_data(n_posts=100, n_comments_per_post=8):
    """
    Generate simulated Facebook dataset
    
    Parameters:
    -----------
    n_posts : int
        Number of posts to generate
    n_comments_per_post : int
        Average number of comments per post
    
    Returns:
    --------
    pd.DataFrame
        Generated Facebook dataset
    """
    
    # Sample posts about climate change
    post_templates = [
        "Just read about the latest climate report. We need urgent action!",
        "Climate change is affecting our communities. What can we do?",
        "New renewable energy breakthrough announced today!",
        "Scientists warn about extreme weather events increasing",
        "Our planet's future depends on climate action now",
        "Carbon emissions reached new record levels this year",
        "Supporting clean energy initiatives in our region",
        "Climate crisis demands immediate policy changes",
        "Green technology is the solution for our future",
        "Environmental protection should be our priority",
    ]
    
    # Sample comments
    positive_comments = [
        "This is great news! More renewable energy please",
        "Finally some positive action on climate!",
        "We need more initiatives like this",
        "Great step forward for our planet",
        "I'm optimistic about these solutions",
        "Love the focus on sustainability",
        "This gives me hope for the future!",
        "Excellent point about climate action",
        "Supporting this 100%!",
        "We need more of this!"
    ]
    
    negative_comments = [
        "This won't make any real difference",
        "Too little too late",
        "I don't believe these numbers",
        "This is just political nonsense",
        "Nothing will change anyway",
        "This is a waste of time and money",
        "I'm tired of hearing about this",
        "Nobody really cares",
        "This is overblown hysteria",
        "It's not that serious"
    ]
    
    neutral_comments = [
        "Interesting information",
        "Thanks for sharing",
        "I need to read more about this",
        "What are the details?",
        "Can you share the source?",
        "When did this happen?",
        "More context please",
        "This is noteworthy",
        "Definitely something to consider",
        "Let me think about this"
    ]
    
    data = []
    base_date = datetime.now() - timedelta(days=180)
    
    for post_id in range(1, n_posts + 1):
        # Generate post
        post_text = random.choice(post_templates)
        post_timestamp = base_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        post_likes = np.random.poisson(50)
        
        # Generate comments for this post
        n_comments = max(1, np.random.poisson(n_comments_per_post))
        
        for comment_id in range(1, n_comments + 1):
            # Choose comment sentiment
            sentiment = np.random.choice(
                ['positive', 'negative', 'neutral'],
                p=[0.4, 0.3, 0.3]
            )
            
            if sentiment == 'positive':
                comment_text = random.choice(positive_comments)
            elif sentiment == 'negative':
                comment_text = random.choice(negative_comments)
            else:
                comment_text = random.choice(neutral_comments)
            
            # Add some variation to comments
            if random.random() > 0.7:
                comment_text += " 😊" if sentiment == 'positive' else (" 😠" if sentiment == 'negative' else " 🤔")
            
            comment_timestamp = post_timestamp + timedelta(
                hours=random.randint(0, 72),
                minutes=random.randint(0, 59)
            )
            
            # Generate engagement metrics
            comment_likes = np.random.poisson(15)
            comment_length = len(comment_text.split())
            
            # Generate reactions (correlated with sentiment)
            if sentiment == 'positive':
                love_reactions = np.random.poisson(8)
                haha_reactions = np.random.poisson(3)
                wow_reactions = np.random.poisson(2)
                sad_reactions = np.random.poisson(1)
                angry_reactions = np.random.poisson(0)
            elif sentiment == 'negative':
                love_reactions = np.random.poisson(1)
                haha_reactions = np.random.poisson(1)
                wow_reactions = np.random.poisson(3)
                sad_reactions = np.random.poisson(5)
                angry_reactions = np.random.poisson(6)
            else:
                love_reactions = np.random.poisson(3)
                haha_reactions = np.random.poisson(2)
                wow_reactions = np.random.poisson(3)
                sad_reactions = np.random.poisson(2)
                angry_reactions = np.random.poisson(2)
            
            data.append({
                'post_id': post_id,
                'post_text': post_text,
                'comment_id': comment_id,
                'comment_text': comment_text,
                'likes': comment_likes,
                'love_reactions': love_reactions,
                'haha_reactions': haha_reactions,
                'wow_reactions': wow_reactions,
                'sad_reactions': sad_reactions,
                'angry_reactions': angry_reactions,
                'timestamp': comment_timestamp,
                'comment_length': comment_length
            })
    
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    print("Generating Facebook dataset...")
    
    # Generate data
    df = generate_facebook_data(n_posts=100, n_comments_per_post=8)
    
    # Save to CSV
    output_file = 'facebook_data_original.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Dataset generated successfully!")
    print(f"\nDataset Statistics:")
    print(f"  Total rows: {len(df)}")
    print(f"  Unique posts: {df['post_id'].nunique()}")
    print(f"  Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"\nColumn information:")
    print(df.info())
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nSaved to: {output_file}")
