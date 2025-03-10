import streamlit as st
import asyncio
from gpt_researcher import GPTResearcher
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
# Function to get report from the backend
async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    # Get additional information
    research_context = researcher.get_research_context()
    research_sources = researcher.get_research_sources()
    return report, research_context, research_sources
 
# Streamlit app code
def main():
    st.title("User Review Analysis")
 
    # Input field for user query
    user_query = st.text_input("Enter your query")
    # Button to trigger the research
    if st.button("Get Reviews"):
        if user_query:
            with st.spinner("Processing your request..."):
                # Run the async function to get the report
                query = f"""
User Reviews from E-Commerce Websites for {user_query}
 
Instructions for GPT Researcher:  
1. Collect authentic user reviews for {user_query} from at least 3 major e-commerce websites: Amazon, Flipkart, and other relevant platforms like Best Buy, Walmart, Target, or category-specific retailers.
2. For each review, include:
   - Star rating (out of 5)
   - Complete review text
3. Gather a minimum of 10 reviews for each star rating (5★, 4★, 3★, 2★, 1★), ensuring a balanced representation of customer experiences.
4. Prioritize recent reviews (within the last 6 months if possible).
5. Include reviews that mention specific features, durability, value for money, and customer service experiences.
6. Capture reviews from different regions/countries if the product is sold internationally.
7. For each source website, note the overall product rating and total number of reviews.

Instructions for Tavily:  
1. Use advanced web scraping to access current review data from Amazon, Flipkart, and other relevant e-commerce platforms.
2. Implement sentiment analysis to verify the alignment between star ratings and review content.
3. Prioritize verified purchase reviews when available.
4. Ensure geographic diversity in the review collection.
5. Capture metadata such as helpful votes, and reviewer profiles when available.
6. Provide direct URLs to each specific product page containing the reviews.
7. Extract both textual reviews and any associated images/videos shared by reviewers if possible.
 
Output Format:  
# User Reviews from E-Commerce Websites for {user_query}

## Product Overview
- Average Rating on Amazon: [X.X]/5 from [XXXX] reviews
- Average Rating on Flipkart: [X.X]/5 from [XXXX] reviews
- Average Rating on [Other Site]: [X.X]/5 from [XXXX] reviews

## 5 star rating:  
  - Review 1: [Full review content]
  - Review 2: [Full review content]
  [...]
  - Review 10: [Full review content]
 
## 4 star rating:  
  - Review 1: [Full review content]
  [...]
  - Review 10: [Full review content]
  
[Continue with 3, 2, and 1 star rating sections]

## Common Themes in Reviews
- Positive Points: [List 3-5 recurring positive aspects mentioned across reviews]
- Critical Points: [List 3-5 recurring negative aspects mentioned across reviews]
- Value Considerations: [Summary of price-to-quality observations from reviewers]

## Sources
- Amazon: [Direct link to product page]
- Flipkart: [Direct link to product page]
- [Other sites]: [Direct links to product pages]

"""
                report_type = "research_report"
                report, context, sources = asyncio.run(get_report(query, report_type))
 
                # Display the results
                st.subheader("Review Report:")
                st.write(report)
 
        else:
            st.error("Please enter a valid query.")
 
if __name__ == "__main__":
    main()
