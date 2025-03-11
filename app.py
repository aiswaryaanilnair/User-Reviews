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
1. Collect authentic user reviews for {user_query} from at least 5 major e-commerce websites: Amazon, Tata Cliq, Snapdeal, Flipkart, Reliance Digital and other relevant platforms like Best Buy, Walmart, Target, or category-specific retailers.
2. For each review, include:
   - Star rating (out of 5)
   - Complete review text
   - 2-4 relevant tags that summarize key points (e.g., "Great battery life," "Poor durability")
3. Must gather a minimum of 10 reviews for each star rating (5★, 4★, 3★, 2★, 1★), ensuring a balanced representation of customer experiences.
4. Combine all reviews under each rating heading without separating them by retailer name.
5. Include reviews that mention specific features, durability, value for money, and customer service experiences.
6. Report must include reviews from Amazon and at least one Indian e-commerce platform (preferably Tata Cliq, Snapdeal, Flipkart, Reliance Digital or Amazon India). There must be at least 10 reviews under each rating.
7. For each source website, note the overall product rating and total number of reviews.

Instructions for Tavily/Search:  
1. Use advanced web scraping to access current review data from Amazon, Indian e-commerce sites, and other relevant platforms.
2. Please prioritize Tata Cliq, Snapdeal, Flipkart, Reliance Digital and Amazon India for Indian market reviews.
3. Provide direct URLs to each specific product page containing the reviews.
4. If Flipkart access remains problematic, ignore it.
 
Output Format:  
# User Reviews from E-Commerce Websites for {user_query}
## Product Overview
### Amazon
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 5-star reviews]

Review 1: [Full review content]
Tags: "Tag 1," "Tag 2," "Tag 3"
Review 2: [Full review content]
Tags: "Tag 1," "Tag 2," "Tag 3"
[Additional reviews...]

4 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 4-star reviews]

Review 1: [Full review content]
Tags: "Tag 1," "Tag 2," "Tag 3"
Review 2: [Full review content]
Tags: "Tag 1," "Tag 2," "Tag 3"
[Additional reviews...]

3 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 3-star reviews]
[Review listings...]
2 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 2-star reviews]
[Review listings...]
1 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 1-star reviews]
[Review listings...]

### [Indian E-commerce Site] (e.g., Tata Cliq, Flipkart, etc.)
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 5-star reviews]
[Review listings...]
4 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 4-star reviews]
[Review listings...]
[Continue with 3-star, 2-star, and 1-star reviews following the same format]

### [Additional Website] (e.g., Best Buy, Walmart, etc.)
[Follow same format as above]

## Common Themes in Reviews
- Positive Points: [List 3-5 recurring positive aspects mentioned across reviews]
- Critical Points: [List 3-5 recurring negative aspects mentioned across reviews]
## Sources
- Amazon: [Direct link to product page]
- [Indian E-commerce Site]: [Direct link to product page]
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
