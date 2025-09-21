# XploreCardano - Cardano Leads Scraper Agent

## 1. Project Name
**XploreCardano** - An AI-powered agent that scrapes Cardano-related X.com (Twitter) profiles for a given topic or niche.

---

## 2. Project Description

XploreCardano is designed to automate the discovery of Cardano communities, influencers, and enthusiasts on X.com. Users enter a topic (e.g., DeFi Builders, Cardano Developers, or AI + Blockchain Educators), and the agent scrapes relevant profiles, extracting:

- Name  
- Username  
- Handle  
- Bio/Description  
- Follower count  

The results are automatically stored in a Google Sheet for easy access by the team.

**Frontend Interface:**  
- React – UI components  
- Tailwind CSS – Styling & layout  

This allows non-technical users to submit topics without running Python scripts.  

**Outcome:**  
A structured, Cardano-focused lead database for marketers, projects, researchers, and communities.

---

## 3. Problem We’re Solving

Discovering Cardano-specific communities and influencers is challenging, especially in niches like:

- DeFi  
- Developers  
- Education  
- Governance  
- Blockchain  
- AI + Web3  

Manual searching is slow, non-scalable, and no single tool exists for organizing leads efficiently.

**Solution:**  
An AI agent that automates search, parses relevant data, and stores it in Google Sheets — making Cardano ecosystem mapping fast and scalable.

## 4. Tech Stack

**Backend / Agent**  
- Python 3  
- APIs: Apify Google Search Scraper, Google Sheets API (Service Account)  
- Libraries: `requests`, `gspread`, `google-auth`, `python-dotenv`  

**Frontend**  
- React  
- Tailwind CSS  

**Collaboration / Database**  
- Google Sheets  

---

## 5. Demo

### CLI Agent
```bash
python cardano_x_leads_to_sheets.py --topic "hiring a cardano dev"
```
Scrapes Cardano-related X profiles for the given topic.
Appends results into a Google Sheet with columns:
Timestamp | Topic | Name | Username | Handle | Description | Followers


Frontend Interface

Built with React + Tailwind CSS.

Users submit topics via a simple form.

Data is scraped and stored in Google Sheets in real-time.

Frontend Demo:

# XploreCardano User Flow (How to Use the App)

# 1. Sign Up / Login
User creates an account or logs in using Google OAuth or email/password.
This authenticates the user and allows access to the app’s features.

<img width="1870" height="785" alt="Screenshot (475)" src="https://github.com/user-attachments/assets/57eeceeb-4107-4d5a-9614-4019ffa09fa8" />

<img width="1867" height="767" alt="Screenshot (476)" src="https://github.com/user-attachments/assets/6b53f7d2-6da0-4664-99b1-b78424762894" />

# 2. Connect Google Sheet

User selects an existing Google Sheet or creates a new one.
This sheet will store all the Cardano leads scraped by the app.
The connection is secure, and the app only writes new rows.

<img width="1892" height="789" alt="Screenshot (477)" src="https://github.com/user-attachments/assets/b6963ae0-694b-4aa2-a35f-3bce43c2f1b3" />
<img width="1885" height="790" alt="Screenshot (478)" src="https://github.com/user-attachments/assets/771e3f14-eb06-4373-a680-9cdcbaea87cc" />


# 3 Enter a Topic

User types a niche or topic they want leads for (e.g., “Hiring Cardano Developers” or “AI + Blockchain products”).
This topic is used to search for relevant profiles on X.com.

<img width="1870" height="806" alt="Screenshot (480)" src="https://github.com/user-attachments/assets/e1f639cf-4306-4dc1-ba5b-b3fc01beafe4" />


# 4 Scrape Leads

User clicks the Scrape Leads button to trigger the backend agent.
The app automatically searches X.com for Cardano-related profiles matching the topic.
Relevant data is collected: Name, Username, Handle, Bio/Description, Follower count.

<img width="1891" height="806" alt="Screenshot (481)" src="https://github.com/user-attachments/assets/f8b5c8fe-f8b6-479c-90da-3267ffff3127" />


# 5 Store Leads in Google Sheet

The scraped leads are automatically appended to the connected Google Sheet.
User receives a confirmation that the scrape was successful.

<img width="1920" height="695" alt="Screenshot (485)" src="https://github.com/user-attachments/assets/f358d239-012d-4034-8879-c3f66af02d70" />
<img width="1874" height="802" alt="Screenshot (482)" src="https://github.com/user-attachments/assets/93489a56-e548-4cbe-a713-45ba313439da" />

# 6 Repeat Process

User can enter a new topic anytime to scrape more leads.
The app continues appending results to the same Google Sheet.


# 6. Deployment

Agent: Run locally using Python
python cardano_x_leads_to_sheets.py --topic "nft artists"

Frontend: Coming Soon 

# 7. PPT

<img width="891" height="780" alt="Screenshot (487)" src="https://github.com/user-attachments/assets/7f0c4737-42f2-40a9-9a2b-ef094a26d15d" />

<img width="867" height="745" alt="Screenshot (488)" src="https://github.com/user-attachments/assets/f0280d1d-612c-4e7f-8692-6b7fcbc87f19" />

<img width="874" height="794" alt="Screenshot (489)" src="https://github.com/user-attachments/assets/a30277e7-6583-4e11-842c-186f12d0ec70" />

<img width="916" height="738" alt="Screenshot (490)" src="https://github.com/user-attachments/assets/019cd2f6-471f-469b-bcde-7fce9e36fb2a" />

<img width="854" height="733" alt="Screenshot (491)" src="https://github.com/user-attachments/assets/78919515-ea06-4e24-a4f9-bba5f1678b7b" />

<img width="849" height="737" alt="Screenshot (492)" src="https://github.com/user-attachments/assets/a1646d44-4e5c-4dda-891b-53ccbf054267" />


# 8. Team Members

Amaan Khan – Full Stack Developer | AI Agent Builder
