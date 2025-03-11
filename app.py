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
Task: Collect authentic user reviews for {user_query} from major e-commerce websites.

Instructions for GPT Researcher:
1. Gather reviews from at least 3 Indian e-commerce sites (Amazon India + Tata Cliq, Snapdeal, Flipkart, Reliance Digital) and optionally Best Buy, Walmart, or other relevant platforms.
2. Collect at least 10 reviews per year from the last five years per rating (5★, 4★, 3★, 2★, 1★) per platform for balanced representation.
3. Include:
    - Star rating (out of 5)
    - Summary of common themes per rating
    - Top 3 individual reviews under each rating per platform
    - Tags summarizing key points for individual reviews (e.g., "Great battery life," "Poor durability")
    - Mentions of specific features, durability, value for money, customer service
4. Report must include Amazon + **at least 3** Indian platforms
5. Summarise all reviews under each rating heading separating them by retailer name.
6. For each source website, note the overall product rating and total number of reviews.
7. Must format the exact OUTPUT FORMAT given below.

Instructions for Tavily/Search:
1. Use advanced web scraping to access user review data from Amazon, Indian e-commerce sites, and other relevant platforms.
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
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
3 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
### [Indian E-commerce Site 1] (e.g., Tata Cliq, Flipkart, etc.)
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 5-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
3 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
### [Indian E-commerce Site 2] (e.g., Tata Cliq, Flipkart, etc.)
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 5-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  
3 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews ([Number] reviews)
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
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
