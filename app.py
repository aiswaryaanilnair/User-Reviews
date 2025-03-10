import streamlit as st
import asyncio
from gpt_researcher import GPTResearcher

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
2. **IMPORTANT: Content from Flipkart MUST be included - this is a critical requirement.**
3. For each review, include:
   - Star rating (out of 5)
   - Complete review text
   - 2-4 relevant tags that summarize key points (e.g., "Great battery life," "Poor durability")
4. Gather a minimum of 10 reviews for each star rating (5★, 4★, 3★, 2★, 1★), ensuring a balanced representation of customer experiences.
5. Combine all reviews under each rating heading without separating them by retailer name.
6. Prioritize recent reviews (within the last 6 months if possible).
7. Include reviews that mention specific features, durability, value for money, and customer service experiences.
8. Capture reviews from different regions/countries if the product is sold internationally.
9. Report MUST include reviews from **Amazon** and **Flipkart**. There must be at least 10 reviews under each rating.
10. Ensure that the displayed reviews include reviews from all websites.
11. For each source website, note the overall product rating and total number of reviews.

Instructions for Tavily:  
1. Use advanced web scraping to access current review data from Amazon, Flipkart, and other relevant e-commerce platforms.
2. **CRITICAL: Must visit Flipkart product page URLs and extract content - this is a mandatory requirement.**
3. Must visit Amazon product page URLs.
4. Extract at least 3 user reviews from each URL.
5. Provide direct URLs to each specific product page containing the reviews.
6. Extract both textual reviews and any associated images/videos shared by reviewers if possible.
 
Output Format:  
# User Reviews from E-Commerce Websites for {user_query}
## Product Overview
- Average Rating on Amazon: [X.X]/5 from [XXXX] reviews
- Average Rating on Flipkart: [X.X]/5 from [XXXX] reviews
- Average Rating on [Other Site]: [X.X]/5 from [XXXX] reviews
## 5 star rating:  
  - Review 1: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  - Review 2: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  [...]
  - Review 10: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
 
## 4 star rating:  
  - Review 1: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  - Review 2: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  [...]
  - Review 10: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  
## 3 star rating:  
  - Review 1: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  - Review 2: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  [...]
  - Review 10: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
## 2 star rating:  
  - Review 1: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  - Review 2: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  [...]
  - Review 10: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
## 1 star rating:  
  - Review 1: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  - Review 2: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  [...]
  - Review 10: [Full review content]
    Tags: "Tag 1," "Tag 2," "Tag 3"
  
## Common Themes in Reviews
- Positive Points: [List 3-5 recurring positive aspects mentioned across reviews]
- Critical Points: [List 3-5 recurring negative aspects mentioned across reviews]
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
