
# PBN Content Generation Script

## Overview
This script is designed to facilitate the generation of high-quality, SEO-optimized articles for Private Blog Networks (PBNs) or sites where expired domain names have been acquired. By leveraging OpenAI's GPT-4o model, the script generates relevant and professional articles that help bridge the gap between the history of the acquired domain and the new site's purpose. The content is structured to be coherent, avoid redundancy, and maximize SEO impact.

## Purpose
The script automates the creation of content for the new site after acquiring an expired domain. This helps ensure that the historical context of the old domain is preserved while aligning with the business goals of the new site. It focuses on generating articles with optimized titles, meta descriptions, and content sections, making the site ready for SEO indexing and boosting search rankings.

## Key Features
- **Generate SEO-Friendly Titles and Descriptions**: The script generates 10 unique article topics based on the history of the expired domain and the new site's context. It also generates SEO-optimized titles and meta descriptions based on the first 500 words of each article.
- **Unique Articles**: Each article generated is at least 1900 words, ensuring rich, in-depth content.
- **Global Context for Coherence**: A `global_context` is introduced in the script to ensure all articles are aligned and coherent with each other, avoiding content overlap or redundancy.
- **HTML Structure**: The generated articles are stored as HTML files with structured elements like `<h1>`, `<h2>`, and `<strong>` to ensure proper formatting for web display and SEO optimization.
- **Customization**: The script allows customization of the historical context, destination, and global content strategy to generate unique articles tailored to the new website's needs.

## Workflow and Logic

1. **Generate Article Titles**: 
   - The script uses the historical context of the expired domain (`history_context`) and the new site’s context (`destination_context`) to generate article titles.
   - 80% of the titles are related directly to the new site’s services, while 20% take a more general approach to attract a wider audience.

2. **Generate Articles**: 
   - For each generated title, a detailed article is created using OpenAI's GPT-4o model.
   - Each article is structured with an introductory `<h1>` tag, followed by informative sections using `<h2>` tags.
   - The content is SEO-optimized, using `<strong>` tags to emphasize key points.

3. **Generate SEO Titles and Meta Descriptions**: 
   - Based on the article’s first 500 words, the script creates SEO-friendly titles and meta descriptions.
   - These metadata elements help improve search engine ranking for the articles.

4. **Save Articles as HTML**: 
   - Each article is saved in an individual HTML file, making it easy to integrate with a CMS or deploy directly to the website.

## Usage Instructions

1. **Install Dependencies**: 
   You need to have Python installed along with OpenAI's Python client. Ensure you install required packages using:
   ```
   pip install openai
   ```

2. **Set OpenAI API Key**: 
   Place your OpenAI API key in the specified file path `/Users/your_user/PBN-TEST/keys.txt`. The key must be stored in the format `OPENAI_API_KEY=your-api-key`.

3. **Modify the Script**: 
   Update the `history_context`, `destination_context`, and `global_context` variables as per your requirements.

4. **Run the Script**: 
   To generate the articles, simply run the script:
   ```
   python script.py
   ```

## Customization
- You can modify the number of articles to generate by changing the `num_articles` parameter.
- To adjust the tone and style of the articles, you can modify the prompts in the `generate_article_html` function.
- The script can be extended to integrate directly with a CMS or automated publishing tool.

## Why This Matters
Generating fresh, relevant, and SEO-optimized content is critical when relaunching a website on an expired domain. The historical authority of the domain combined with new, targeted content allows you to regain search engine ranking quickly. This script helps automate the content creation process and ensures that each article is aligned with both SEO best practices and the business goals of the new website.

## Conclusion
This content generation script is a powerful tool for PBN owners, SEOs, and developers looking to scale content production efficiently. By bridging the gap between an expired domain’s history and the new site’s future, this script helps maintain continuity while driving long-term SEO growth.

