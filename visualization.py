#!/usr/bin/env python3
"""
Visualization Script
Creates comprehensive visualizations for sentiment analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create visualizations directory
os.makedirs('visualizations', exist_ok=True)

def plot_sentiment_distribution_over_time(df, output_file='visualizations/01_sentiment_distribution_over_time.png'):
    """
    Plot sentiment distribution over time
    """
    print("Creating sentiment distribution over time...")
    
    df_sorted = df.sort_values('timestamp')
    sentiment_by_date = df_sorted.groupby([df_sorted['timestamp'].dt.date, 'sentiment_label']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    sentiment_by_date.plot(ax=ax, marker='o', linewidth=2)
    ax.set_title('Sentiment Distribution Over Time', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Number of Comments', fontsize=12)
    ax.legend(title='Sentiment', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_sentiment_pie_chart(df, output_file='visualizations/02_sentiment_distribution_pie.png'):
    """
    Plot sentiment distribution as pie chart
    """
    print("Creating sentiment distribution pie chart...")
    
    sentiment_counts = df['sentiment_label'].value_counts()
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    ax.set_title('Overall Sentiment Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_wordcloud_by_sentiment(df, output_file_pos='visualizations/03_wordcloud_positive.png',
                               output_file_neg='visualizations/04_wordcloud_negative.png'):
    """
    Generate word clouds for positive and negative comments
    """
    print("Creating word clouds...")
    
    # Positive comments
    positive_text = ' '.join(df[df['sentiment_label'] == 'positive']['comment_text_cleaned'].astype(str))
    if positive_text.strip():
        wordcloud_pos = WordCloud(width=800, height=400, background_color='white',
                                 colormap='Greens').generate(positive_text)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wordcloud_pos, interpolation='bilinear')
        ax.set_title('Word Cloud - Positive Comments', fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(output_file_pos, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file_pos}")
        plt.close()
    
    # Negative comments
    negative_text = ' '.join(df[df['sentiment_label'] == 'negative']['comment_text_cleaned'].astype(str))
    if negative_text.strip():
        wordcloud_neg = WordCloud(width=800, height=400, background_color='white',
                                 colormap='Reds').generate(negative_text)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wordcloud_neg, interpolation='bilinear')
        ax.set_title('Word Cloud - Negative Comments', fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(output_file_neg, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file_neg}")
        plt.close()

def plot_reaction_sentiment_heatmap(df, output_file='visualizations/05_reaction_sentiment_heatmap.png'):
    """
    Create heatmap of reactions vs sentiment
    """
    print("Creating reaction-sentiment heatmap...")
    
    reactions = ['love_reactions', 'haha_reactions', 'wow_reactions', 'sad_reactions', 'angry_reactions']
    reaction_names = ['Love', 'Haha', 'Wow', 'Sad', 'Angry']
    
    heatmap_data = []
    for reaction in reactions:
        row = []
        for sentiment in ['positive', 'negative', 'neutral']:
            avg = df[df['sentiment_label'] == sentiment][reaction].mean()
            row.append(avg)
        heatmap_data.append(row)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', 
                xticklabels=['Positive', 'Negative', 'Neutral'],
                yticklabels=reaction_names, cbar_kws={'label': 'Average Reactions'},
                ax=ax)
    ax.set_title('Average Reactions by Sentiment', fontsize=16, fontweight='bold')
    ax.set_ylabel('Reaction Type', fontsize=12)
    ax.set_xlabel('Sentiment', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_top_engaged_posts(df, output_file='visualizations/06_top_engaged_posts.png', top_n=10):
    """
    Plot top engaged posts
    """
    print(f"Creating top {top_n} engaged posts visualization...")
    
    top_posts = df.groupby('post_id').agg({\n        'engagement_score': 'sum',
        'sentiment_label': lambda x: (x == 'positive').sum() / len(x) if len(x) > 0 else 0
    }).nlargest(top_n, 'engagement_score').reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.RdYlGn(top_posts['sentiment_label'].values)
    ax.barh(range(len(top_posts)), top_posts['engagement_score'].values, color=colors)
    ax.set_yticks(range(len(top_posts)))
    ax.set_yticklabels([f"Post {pid}" for pid in top_posts['post_id'].values])
    ax.set_xlabel('Total Engagement Score', fontsize=12)
    ax.set_title(f'Top {top_n} Most Engaged Posts', fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_comment_length_vs_sentiment(df, output_file='visualizations/07_comment_length_vs_sentiment.png'):
    """
    Plot comment length vs sentiment
    """
    print("Creating comment length vs sentiment plot...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sentiments = df['sentiment_label'].unique()
    colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
    
    for sentiment in sentiments:
        data = df[df['sentiment_label'] == sentiment]['comment_length']
        ax.scatter([sentiment] * len(data), data, alpha=0.5, s=50, 
                  label=sentiment, color=colors.get(sentiment, 'gray'))
    
    ax.set_ylabel('Comment Length (words)', fontsize=12)
    ax.set_xlabel('Sentiment', fontsize=12)
    ax.set_title('Comment Length by Sentiment', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_temporal_activity_pattern(df, output_file='visualizations/08_temporal_activity_pattern.png'):
    """
    Plot activity patterns by hour of day
    """
    print("Creating temporal activity pattern visualization...")
    
    hourly_activity = df.groupby(['hour', 'sentiment_label']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    hourly_activity.plot(ax=ax, marker='o', linewidth=2)
    ax.set_title('Comment Activity by Hour of Day', fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Number of Comments', fontsize=12)
    ax.legend(title='Sentiment', fontsize=10)
    ax.set_xticks(range(0, 24))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def plot_emoji_frequency(df, output_file='visualizations/09_emoji_frequency.png', top_n=10):
    """
    Plot emoji frequency
    """
    print(f"Creating top {top_n} emoji frequency visualization...")
    
    # Get all emojis
    all_emojis = []
    for emojis_str in df['emojis_in_comment'].dropna():
        if emojis_str:
            all_emojis.extend(emojis_str.split())
    
    if all_emojis:
        emoji_counts = Counter(all_emojis).most_common(top_n)
        emojis, counts = zip(*emoji_counts)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(range(len(emojis)), counts, color='skyblue')
        ax.set_xticks(range(len(emojis)))
        ax.set_xticklabels([str(e) for e in emojis], fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'Top {top_n} Most Frequent Emojis', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

def plot_sentiment_metrics_dashboard(df, output_file='visualizations/10_sentiment_metrics_dashboard.png'):
    """
    Create a dashboard with key metrics
    """
    print("Creating sentiment metrics dashboard...")
    
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Sentiment distribution bar
    ax1 = fig.add_subplot(gs[0, 0])
    sentiment_counts = df['sentiment_label'].value_counts()
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    ax1.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
    ax1.set_title('Sentiment Count', fontweight='bold')
    ax1.set_ylabel('Count')
    for i, v in enumerate(sentiment_counts.values):
        ax1.text(i, v + 5, str(v), ha='center', fontweight='bold')
    
    # 2. Engagement by sentiment
    ax2 = fig.add_subplot(gs[0, 1])
    engagement_by_sentiment = df.groupby('sentiment_label')['engagement_score'].mean()
    ax2.bar(engagement_by_sentiment.index, engagement_by_sentiment.values, color=colors)
    ax2.set_title('Average Engagement Score', fontweight='bold')
    ax2.set_ylabel('Score')
    
    # 3. Polarity distribution
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(df['sentiment_polarity'], bins=20, color='steelblue', edgecolor='black')
    ax3.set_title('Sentiment Polarity Distribution', fontweight='bold')
    ax3.set_xlabel('Polarity Score')
    ax3.set_ylabel('Frequency')
    ax3.axvline(df['sentiment_polarity'].mean(), color='red', linestyle='--', label='Mean')
    ax3.legend()
    
    # 4. Comment length by sentiment
    ax4 = fig.add_subplot(gs[1, 1])
    length_by_sentiment = df.groupby('sentiment_label')['comment_length'].mean()
    ax4.bar(length_by_sentiment.index, length_by_sentiment.values, color=colors)
    ax4.set_title('Average Comment Length', fontweight='bold')
    ax4.set_ylabel('Words')
    
    # 5. Likes vs Sentiment
    ax5 = fig.add_subplot(gs[2, 0])
    likes_by_sentiment = df.groupby('sentiment_label')['likes'].mean()
    ax5.bar(likes_by_sentiment.index, likes_by_sentiment.values, color=colors)
    ax5.set_title('Average Likes by Sentiment', fontweight='bold')
    ax5.set_ylabel('Likes')
    
    # 6. Emoji count by sentiment
    ax6 = fig.add_subplot(gs[2, 1])
    emoji_by_sentiment = df.groupby('sentiment_label')['emoji_count'].mean()
    ax6.bar(emoji_by_sentiment.index, emoji_by_sentiment.values, color=colors)
    ax6.set_title('Average Emoji Usage', fontweight='bold')
    ax6.set_ylabel('Emoji Count')
    
    plt.suptitle('Sentiment Analysis Metrics Dashboard', fontsize=18, fontweight='bold', y=0.995)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def create_all_visualizations(input_file='facebook_data_with_sentiment.csv'):
    """
    Create all visualizations
    
    Parameters:
    -----------
    input_file : str
        Path to analyzed data file
    """
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60 + "\n")
    
    # Load data
    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create all visualizations
    plot_sentiment_distribution_over_time(df)
    plot_sentiment_pie_chart(df)
    plot_wordcloud_by_sentiment(df)
    plot_reaction_sentiment_heatmap(df)
    plot_top_engaged_posts(df)
    plot_comment_length_vs_sentiment(df)
    plot_temporal_activity_pattern(df)
    plot_emoji_frequency(df)
    plot_sentiment_metrics_dashboard(df)
    
    print("\n" + "="*60)
    print("✓ ALL VISUALIZATIONS CREATED SUCCESSFULLY")
    print("="*60)
    print("\nVisualizations saved in: visualizations/")

if __name__ == "__main__":
    create_all_visualizations()
