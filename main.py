import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import os
import re
from collections import Counter

# ==========================================
# PART I: CORE DATA (IMMUTABLE FOUNDATION)
# ==========================================

# Keywords are kept for weighted scoring, but the engine will fallback to "any text" if these miss.
HARDCODED_PATTERNS = [
    {
        "id": "SONSHIP_INCLUSIVE_008",
        "domain": "Covenant Community",
        "principle": "Covenant sonship includes male and female equally; masculine terminology denotes status, not biological exclusion.",
        "texts": ["Gal 3:28", "John 1:12", "2 Cor 6:18", "Rom 8:14-17"],
        "confidence": 0.98,
        "keywords": ["women", "woman", "female", "sonship", "sons", "inheritance", "gender", "equal", "brothers", "adelphoi"]
    },
    {
        "id": "LEAD_ACCOUNTABILITY_MANDATORY_007",
        "domain": "Covenant Community",
        "principle": "No leader exempt from examination; 'above reproach' means examinable, not immune. Leaders must be held accountable.",
        "texts": ["Acts 17:11", "1 Tim 5:19-20", "Gal 2:11", "Matt 18"],
        "confidence": 0.99,
        "keywords": ["leader", "pastor", "elder", "accountability", "examine", "authority", "abuse", "immune", "rebuke", "oversight"]
    },
    {
        "id": "DIVINE_LAW_ADAPTABLE",
        "domain": "Covenant Community",
        "principle": "God's law adapts to human need and justice; exceptions reveal deeper principles of mercy over sacrifice.",
        "texts": ["Num 27:7-11", "Matt 19:3-9", "Gal 3:24-25"],
        "confidence": 0.87,
        "keywords": ["law", "justice", "mercy", "exception", "legalism", "rigid", "sabbath", "rule"]
    },
    {
        "id": "PETITION_VALID_009",
        "domain": "Divine Human",
        "principle": "Formal, persistent, collective petition is a valid biblical mechanism for redress, it is not presumptuous rebellion.",
        "texts": ["Num 27:1-11", "Luke 18:1-8", "Esther 4:16", "1 Sam 25"],
        "confidence": 0.94,
        "keywords": ["petition", "protest", "complaint", "redress", "widow", "appeal", "request", "change"]
    },
    {
        "id": "WOMEN_INITIATE_CHANGE_001",
        "domain": "Divine Human",
        "principle": "Women's formal petition can initiate divine law change and structural reform in the community.",
        "texts": ["Num 27", "Esther", "1 Sam 25", "Luke 18"],
        "confidence": 0.92,
        "keywords": ["zelophehad", "daughters", "esther", "abigail", "reform", "structure", "change"]
    }
]

PROHIBITED_KEYWORDS = [
    "new revelation", "contradicts scripture", "cultural override", 
    "spirit superseding text", "evil"
]

SCRIPTURE_DB = {
    "Gal 3:28": "There is neither Jew nor Greek, there is neither slave nor free, there is no male and female, for you are all one in Christ Jesus.",
    "John 1:12": "But to all who did receive him, who believed in his name, he gave the right to become children of God.",
    "Acts 17:11": "Now these Jews were more noble than those in Thessalonica; they received the word with all eagerness, examining the Scriptures daily to see if these things were so.",
    "1 Tim 5:19-20": "Do not admit a charge against an elder except on the evidence of two or three witnesses. As for those who persist in sin, rebuke them in the presence of all.",
    "Num 27:1-11": "Then drew near the daughters of Zelophehad... And the Lord said to Moses, 'The daughters of Zelophehad are right...' This shall be a statute of judgment.",
    "Luke 18:1-8": "And he told them a parable to the effect that they ought always to pray and not lose heart... 'Will not God give justice to his elect, who cry to him day and night?'",
    "Article 3": "We know in part (1 Cor 13:9). Interpretive arrogance is disqualifying.",
    "Article 10": "Reject any approach violating: Scripture coherence, Spirit discernment, humility."
}

# ==========================================
# PART II: PROCESS ENGINE (LIGHTWEIGHT)
# ==========================================

class SIAServer:
    def __init__(self):
        # Pre-process pattern text for flexible matching
        self.corpus = []
        for p in HARDCODED_PATTERNS:
            # Combine principle + keywords into one string for matching
            text_blob = f"{p['principle']} {' '.join(p.get('keywords', []))}"
            self.corpus.append(text_blob.lower())
        
        print("Lightweight Engine Initialized.")

    def tokenize(self, text):
        # Simple cleanup: lowercase, remove punctuation, split into words
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()

    def analyze_query(self, query: str):
        query_lower = query.lower()
        
        # 1. Prohibited Check
        for keyword in PROHIBITED_KEYWORDS:
            if keyword in query_lower:
                return {
                    "outcome": "UNVERIFIED",
                    "reason": f"Violation: Prohibited method detected ('{keyword}') violates Article 10.",
                    "witnesses": ["Article 10"],
                    "confidence": 0.0
                }

        # 2. Flexible Scoring Algorithm
        # We count how many query words appear in the pattern's text blob
        query_words = self.tokenize(query)
        if not query_words:
             return {
                "outcome": "PRAY",
                "reason": "Empty query.",
                "witnesses": ["Article 3"],
                "confidence": 0.0
            }

        best_score = 0
        best_match_index = -1

        for i, pattern_blob in enumerate(self.corpus):
            pattern_words = set(self.tokenize(pattern_blob))
            # Count intersection
            common_words = [w for w in query_words if w in pattern_words]
            score = len(common_words)
            
            # Boost score if keywords appear (optional weighting)
            # But essentially, any matching word increases score
            
            if score > best_score:
                best_score = score
                best_match_index = i

        # 3. Decision Logic
        # If we found at least 1 matching word, we return the best pattern
        if best_match_index >= 0 and best_score > 0:
            match = HARDCODED_PATTERNS[best_match_index]
            # Normalize confidence based on overlap (arbitrary scaling)
            # Max confidence is the pattern's inherent confidence
            calc_conf = min(match['confidence'], 0.5 + (best_score * 0.1)) 
            
            return {
                "outcome": "VERIFIED" if match['confidence'] >= 0.90 else "PRAY",
                "reason": match['principle'],
                "witnesses": match['texts'],
                "confidence": match['confidence'] # Return hard-coded confidence
            }

        # 4. Fallback
        return {
            "outcome": "PRAY",
            "reason": "Query does not match established hard-coded patterns. Requires Spirit illumination.",
            "witnesses": ["Article 3 (Humility)"],
            "confidence": 0.0
        }

    def get_verse_text(self, refs: List[str]) -> List[dict]:
        data = []
        for r in refs:
            data.append({
                "ref": r,
                "text": SCRIPTURE_DB.get(r, "[Full text requires API integration]")
            })
        return data

# ==========================================
# PART III: WEB APPLICATION
# ==========================================

app = FastAPI(title="SIA ENGINE v5.0")
engine = SIAServer()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIA ENGINE v5.0</title>
    <style>
        :root { --primary: #2c3e50; --bg: #f4f4f4; --verified: #27ae60; --unverified: #c0392b; --pray: #f39c12; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: #333; display: flex; justify-content: center; padding-top: 50px; margin: 0; }
        .container { width: 100%; max-width: 600px; background: white; padding: 2rem; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 10px; }
        .subtitle { font-size: 0.9rem; color: #666; margin-bottom: 2rem; }
        input[type="text"] { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; margin-bottom: 10px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; font-weight: bold; }
        button:hover { opacity: 0.9; }
        .output-box { margin-top: 2rem; border-top: 1px solid #eee; padding-top: 1.5rem; display: none; }
        .result-badge { padding: 8px 15px; color: white; font-weight: bold; border-radius: 4px; display: inline-block; margin-bottom: 1rem; font-size: 0.9rem; }
        .VERIFIED { background: var(--verified); }
        .UNVERIFIED { background: var(--unverified); }
        .PRAY { background: var(--pray); }
        .witness-list { list-style: none; padding: 0; margin-top: 1rem; }
        .witness-list li { background: #f9f9f9; border-left: 4px solid #ddd; padding: 10px; margin-bottom: 8px; font-size: 0.9rem; }
        .witness-text { font-size: 0.85rem; color: #555; margin-top: 4px; font-style: italic; }
        .reasoning { color: #555; margin-bottom: 1rem; font-weight: 500; }
        .loader { border: 3px solid #f3f3f3; border-top: 3px solid var(--primary); border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; display: none; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="container">
    <h1>SIA ENGINE v5.0</h1>
    <div class="subtitle">Scripture Interpretation & Application</div>

    <div class="input-section">
        <label for="query"><strong>Enter your query:</strong></label>
        <input type="text" id="query" placeholder="e.g., Can women be leaders?">
        <button onclick="submitQuery()">Submit</button>
    </div>

    <div class="loader" id="loader"></div>

    <div class="output-box" id="outputArea">
        <div id="statusBadge" class="result-badge"></div>
        <div id="reasoningText" class="reasoning"></div>
        
        <div class="scripture-witnesses">
            <strong>Scripture witnesses:</strong>
            <ul id="witnessList" class="witness-list"></ul>
        </div>
    </div>
</div>

<script>
    async function submitQuery() {
        const queryInput = document.getElementById('query').value;
        const outputArea = document.getElementById('outputArea');
        const loader = document.getElementById('loader');
        
        if (!queryInput) return;

        loader.style.display = 'block';
        outputArea.style.display = 'none';

        try {
            const response = await fetch('/interpret', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query_text: queryInput })
            });

            const data = await response.json();

            loader.style.display = 'none';
            outputArea.style.display = 'block';

            const badge = document.getElementById('statusBadge');
            badge.textContent = data.outcome;
            badge.className = 'result-badge ' + data.outcome;

            document.getElementById('reasoningText').innerText = data.principle;

            const list = document.getElementById('witnessList');
            list.innerHTML = '';
            
            data.witness_data.forEach(w => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${w.ref}</strong><div class="witness-text">${w.text}</div>`;
                list.appendChild(li);
            });

        } catch (error) {
            loader.style.display = 'none';
            alert('Engine Connection Failed');
            console.error(error);
        }
    }
</script>
</body>
</html>
"""

class QueryModel(BaseModel):
    query_text: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.post("/interpret")
async def interpret(query: QueryModel):
    result = engine.analyze_query(query.query_text)
    witness_data = engine.get_verse_text(result['witnesses'])
    
    return {
        "outcome": result['outcome'],
        "principle": result['reason'],
        "witnesses": result['witnesses'],
        "witness_data": witness_data,
        "confidence": result['confidence']
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
