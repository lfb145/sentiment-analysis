# Facebook Sentiment & Engagement Analysis Project

## 📋 Project Overview

This project performs comprehensive **sentiment analysis** and **engagement analysis** on Facebook posts and comments. It analyzes user behavior patterns including sentiment distribution, emotional reactions, engagement metrics, and temporal patterns.

### 🎯 Objectives

1. **Analyze User Sentiment** - Classify comments as positive, negative, or neutral
2. **Measure Engagement** - Track likes, reactions, and comment activity
3. **Identify Patterns** - Find correlations between sentiment, reactions, and engagement
4. **Visualize Results** - Create professional visualizations and dashboards
5. **Generate Insights** - Provide actionable findings about user behavior

---

## 📁 Project Structure

```
project/
├── data/
│   ├── facebook_data_original.csv          # Original simulated dataset
│   ├── facebook_data_processed.csv         # Cleaned and preprocessed data
│   └── facebook_data_with_sentiment.csv    # Data with sentiment analysis
├── scripts/
│   ├── data_generation.py                 # Generate simulated Facebook data
│   ├── data_preprocessing.py              # Clean and preprocess text
│   ├── sentiment_analysis.py              # Perform sentiment analysis
│   └── visualization.py                   # Create visualizations
├── visualizations/
│   ├── 01_sentiment_distribution_over_time.png
│   ├── 02_sentiment_distribution_pie.png
│   ├── 03_wordcloud_positive.png
│   ├── 04_wordcloud_negative.png
│   ├── 05_reaction_sentiment_heatmap.png
│   ├── 06_top_engaged_posts.png
│   ├── 07_comment_length_vs_sentiment.png
│   ├── 08_temporal_activity_pattern.png
│   ├── 09_emoji_frequency.png
│   ├── 10_sentiment_metrics_dashboard.png
├── Facebook_Sentiment_Analysis.ipynb       # Complete Jupyter notebook
├── Project_Report.md                       # Comprehensive project report
├── requirements.txt                        # Python dependencies
└── README.md                              # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Data Directory

```bash
mkdir data
mkdir visualizations
```

---

## 🚀 How to Run

### Option 1: Run All Scripts in Sequence

```bash
# 1. Generate simulated data
python data_generation.py

# 2. Preprocess the data
python data_preprocessing.py

# 3. Perform sentiment analysis
python sentiment_analysis.py

# 4. Create visualizations
python visualization.py
```

### Option 2: Run Jupyter Notebook

```bash
jupyter notebook Facebook_Sentiment_Analysis.ipynb
```

---

## 📊 What Each Script Does

### `data_generation.py`
**Purpose:** Generate realistic simulated Facebook dataset

**Output:** `facebook_data_original.csv`

**Features:**
- Creates 100 posts about climate change
- Generates ~800 comments with realistic engagement metrics
- Simulates reactions (love, haha, wow, sad, angry)
- Includes timestamps and comment metadata

**Run:**
```bash
python data_generation.py
```

### `data_preprocessing.py`
**Purpose:** Clean and preprocess text data

**Output:** `facebook_data_processed.csv`

**Processing Steps:**
- Remove URLs and email addresses
- Remove mentions and hashtags
- Convert emojis to text representation
- Lowercase text
- Remove special characters
- Tokenization and stopword removal
- Calculate engagement metrics
- Extract temporal features

**Run:**
```bash
python data_preprocessing.py
```

### `sentiment_analysis.py`
**Purpose:** Analyze sentiment of comments

**Output:** `facebook_data_with_sentiment.csv`

**Analysis Performed:**
- Sentiment classification (positive/negative/neutral)
- Polarity score calculation (-1 to 1)
- Subjectivity scoring
- Engagement analysis by sentiment
- Reaction type correlation analysis

**Run:**
```bash
python sentiment_analysis.py
```

### `visualization.py`
**Purpose:** Generate professional visualizations

**Outputs:** 10 PNG files in `visualizations/` directory

**Visualizations Created:**
1. Sentiment Distribution Over Time
2. Sentiment Distribution Pie Chart
3. Word Cloud - Positive Comments
4. Word Cloud - Negative Comments
5. Reaction-Sentiment Heatmap
6. Top Engaged Posts
7. Comment Length vs Sentiment
8. Temporal Activity Pattern
9. Emoji Frequency
10. Metrics Dashboard

**Run:**
```bash
python visualization.py
```

---

## 📈 Key Findings & Metrics

### Sentiment Distribution
- **Positive Comments:** 40-50% of total
- **Negative Comments:** 25-35% of total
- **Neutral Comments:** Remaining percentage

### Engagement Patterns
- Positive comments receive more "love" reactions
- Negative comments receive more "sad" and "angry" reactions
- Comment length has weak correlation with sentiment
- Emoji usage is higher in emotional comments

### Temporal Insights
- Peak activity hours: 10-12 and 19-21
- Sentiment varies throughout the day
- Weekend patterns may differ from weekdays

---

## 📝 Data Columns Explained

### Original Data (`facebook_data_original.csv`)
| Column | Type | Description |
|--------|------|-------------|
| post_id | int | Unique post identifier |
| post_text | str | Content of the Facebook post |
| comment_id | int | Unique comment identifier |
| comment_text | str | Content of the comment |
| likes | int | Number of likes on comment |
| love_reactions | int | Number of love reactions |
| haha_reactions | int | Number of haha reactions |
| wow_reactions | int | Number of wow reactions |
| sad_reactions | int | Number of sad reactions |
| angry_reactions | int | Number of angry reactions |
| timestamp | datetime | When comment was posted |
| comment_length | int | Word count of comment |

### Processed Data (additions)
| Column | Type | Description |
|--------|------|-------------|
| comment_text_cleaned | str | Preprocessed comment text |
| total_reactions | int | Sum of all reaction types |
| engagement_score | int | likes + total_reactions |
| emoji_count | int | Number of emojis used |
| hour | int | Hour of day (0-23) |
| day_of_week | str | Day name |
| date | date | Date of comment |

### Analysis Data (additions)
| Column | Type | Description |
|--------|------|-------------|
| sentiment_polarity | float | Sentiment score (-1 to 1) |
| sentiment_subjectivity | float | Subjectivity score (0 to 1) |
| sentiment_label | str | Classification: positive/negative/neutral |

---

## 🔍 How Sentiment Analysis Works

This project uses **TextBlob**, a simple NLP library that:

1. **Polarity Score** (-1 to 1):
   - -1: Very negative
   - 0: Neutral
   - +1: Very positive

2. **Classification Logic**:
   - Polarity > 0.1 → Positive
   - Polarity < -0.1 → Negative
   - Otherwise → Neutral

3. **Example:**
   - "Great news! Love this!" → Positive (0.75)
   - "This is terrible" → Negative (-0.65)
   - "What is this?" → Neutral (0.0)

---

## 📋 Data Preprocessing Steps

### Text Cleaning
```
Original:  "Check out https://example.com! This is amazing 😊 #ClimateAction"
           ↓
Cleaned:   "check out this is amazing smile climateaction"
```

### Emoji Handling
```
"😊 Love this!" → "smiling face love this"
"😠 Terrible!" → "angry face terrible"
```

### Stopword Removal
```
"we are doing this now" → "doing"
```

---

## 🔒 Ethical Considerations

### This Project:
✅ Uses **simulated data** only  
✅ Does not collect **private user data**  
✅ Respects **user privacy**  
✅ Is for **educational purposes**  

### If using real Facebook data:
⚠️ Always obtain **user consent**  
⚠️ Follow **Facebook Terms of Service**  
⚠️ Anonymize and **aggregate results**  
⚠️ Never store **personal information**  

---

## 📚 Dependencies

- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization
- **seaborn** - Enhanced visualizations
- **textblob** - Sentiment analysis
- **nltk** - Natural language processing
- **wordcloud** - Word cloud generation
- **emoji** - Emoji handling
- **scikit-learn** - Machine learning (optional)

---

## 🎓 Learning Outcomes

After completing this project, you will understand:

1. **Data Collection** - How to gather and simulate social media data
2. **Text Preprocessing** - Cleaning and preparing text for analysis
3. **Sentiment Analysis** - Classification and scoring methods
4. **Data Visualization** - Creating meaningful charts and graphics
5. **Behavioral Analysis** - Identifying patterns in user engagement
6. **Statistical Analysis** - Computing metrics and correlations

---

## 🐛 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: NLTK data not found
The scripts will automatically download required NLTK data on first run.

### Error: No such file or directory
Make sure you have created the `data/` directory:
```bash
mkdir data
```

### Memory issues with large datasets
Reduce `n_posts` parameter in `data_generation.py`

---

## 📞 Support

For issues or questions, check:
1. The Jupyter notebook for step-by-step execution
2. Script docstrings for function documentation
3. The project report for detailed explanations

---

## 📄 License

This is an educational project created for academic purposes.

---

## ✨ Features Highlight

✅ **Complete Pipeline** - From data generation to visualization  
✅ **Well-Documented** - Detailed comments and docstrings  
✅ **Production-Ready Code** - Error handling and validation  
✅ **Professional Visualizations** - 10 high-quality charts  
✅ **Jupyter Notebook** - Interactive analysis environment  
✅ **Comprehensive Report** - Full project documentation  
✅ **Reproducible** - Fixed random seed for consistent results  

---

**Last Updated:** 2024  
**Status:** Complete and Ready for Submission ✓
