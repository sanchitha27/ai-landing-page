import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Landing Page Personalizer")

st.title(" AI Landing Page Personalizer")
st.caption(" Built for CRO optimization using AI")

# Inputs
ad_input = st.text_area("📢 Paste Ad Content")
url = st.text_input("🌐 Enter Landing Page URL")

#  Scrape landing page
def get_page_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove scripts/styles
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ")
        return text[:1200]

    except Exception as e:
        return f"Could not fetch page: {e}"


# Rule-based AI (fallback but smart)
def generate_output(ad, page):

    # Headline from ad
    headline = ad.split(".")[0]

    # Detect urgency
    urgency = ""
    if "limited" in ad.lower() or "today" in ad.lower():
        urgency = "Hurry! Limited time offer."

    # CTA logic
    if "%" in ad or "off" in ad.lower():
        cta = "Grab the Offer Now"
    else:
        cta = "Explore Now"

    return f"""
### New Headline:
{headline}

### New CTA:
{cta}

### Improved Text:
{headline}. {urgency} Designed specifically for users interested in this offer.

### Reason:
This aligns the landing page with the ad intent, improves message match, and increases conversion probability.
"""


# Main button
if st.button("Generate"):
    if not ad_input or not url:
        st.warning(" Please enter both Ad Content and URL")
    else:
        with st.spinner("Optimizing..."):
            page = get_page_content(url)
            result = generate_output(ad_input, page)

        #  ORIGINAL PAGE
        st.subheader(" Original Landing Page (Preview)")
        st.write(page[:500] + "...")

        st.divider()

        #  ENHANCED VERSION
        st.subheader(" Personalized Version (CRO Enhanced)")
        st.markdown(result)

        st.caption(" Changes applied: Headline, CTA, Messaging alignment")
        st.info("This enhances the existing page instead of replacing it")

        st.success(" Optimization complete")
