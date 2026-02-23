import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os

# ==========================================
# PART I: CORE DATA (IMMUTABLE FOUNDATION)
# ==========================================

HARDCODED_PATTERNS = [
    {
        "id": "SONSHIP_INCLUSIVE_008",
        "domain": "Covenant Community",
        "principle": "Covenant sonship includes male and female equally; masculine terminology denotes status, not biological exclusion.",
        "texts": ["Gal 3:28", "John 1:12", "2 Cor 6:18", "Rom 8:14-17"],
        "confidence": 0.98,
        "triggers": ["sons", "brothers", "adelphoi", "banim", "inheritance", "women in church", "female inclusion", "sonship"]
    },
    {
        "id": "LEAD_ACCOUNTABILITY_MANDATORY_007",
        "domain": "Covenant Community",
        "principle": "No leader exempt from examination; 'above reproach' = examinable, not immune.",
        "texts": ["Acts 17:11", "1 Tim 5:19-20", "Gal 2:11", "Matt 18"],
        "confidence": 0.99,
        "triggers": ["pastor accountability", "elder sin", "leadership immunity", "rebuke leader", "examine leadership", "authority abuse"]
    },
    {
        "id": "DIVINE_LAW_ADAPTABLE",
        "domain": "Covenant Community",
        "principle": "God's law adapts to human need + justice; 'exceptions' reveal deeper principles.",
        "texts": ["Num 27:7-11", "Matt 19:3-9", "Gal 3:24-25"],
        "confidence": 0.87,
        "triggers": ["law exception", "justice over law", "mercy over sacrifice", "legalism"]
    },
    {
        "id": "PETITION_VALID_009",
        "domain": "Divine Human",
        "principle": "Formal, persistent, collective petition is valid biblical mechanism, not rebellion.",
        "texts": ["Num 27:1-11", "Luke 18:1-8", "Esther 4:16", "1 Sam 25"],
        "confidence": 0.94,
        "triggers": ["petition", "protest", "complaint to leadership", "persistent widow", "redress"]
    },
    {
        "id": "WOMEN_INITIATE_CHANGE_001",
        "domain": "Divine Human",
        "principle": "Women's formal petition can initiate divine law change and structural reform.",
        "texts": ["Num 27", "Esther", "1 Sam 25", "Luke 18"],
        "confidence": 0.92,
        "triggers": ["zelophehad daughters", "women leadership change", "abigail intervention", "esther petition"]
    }
]

PROHIBITED_KEYWORDS = [
    "new revelation", "contradicts scripture", "cultural override", 
    "spirit superseding text", "isolated verse proof", "evil"
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
# PART II: PROCESS ENGINE
# ==========================================

class SIAServer:
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

        # 2. Pattern Matching
        matched_patterns = []
        for pattern in HARDCODED_PATTERNS:
            for trigger in pattern['triggers']:
                if trigger in query_lower:
                    matched_patterns.append(pattern)
                    break
        
        # 3. Threshold Logic
        if not matched_patterns:
            return {
                "outcome": "PRAY",
                "reason": "Query does not match established hard-coded patterns. Requires Spirit illumination.",
                "witnesses": ["Article 3 (Humility)"],
                "confidence": 0.0
            }

        best_match = max(matched_patterns, key=lambda x: x['confidence'])
        confidence = best_match['confidence']
        
        if confidence >= 0.90:
            outcome = "VERIFIED"
        else:
            outcome = "PRAY" 

        return {
            "outcome": outcome,
            "reason": best_match['principle'],
            "witnesses": best_match['texts'],
            "confidence": confidence
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
# PART III: WEB APPLICATION (FastAPI)
# ==========================================

app = FastAPI(title="SIA ENGINE v5.0")
engine = SIAServer()

# HTML/CSS/JS SERVED DIRECTLY FROM PYTHON
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
        <input type="text" id="query" placeholder="e.g., Are women included in covenant sonship?">
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

# API Endpoints
class QueryModel(BaseModel):
    query_text: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.post("/interpret")
async def interpret(query: QueryModel):
    # 1. Run Engine Logic
    result = engine.analyze_query(query.query_text)
    
    # 2. Fetch Verse Texts
    witness_data = engine.get_verse_text(result['witnesses'])
    
    return {
        "outcome": result['outcome'],
        "principle": result['reason'],
        "witnesses": result['witnesses'],
        "witness_data": witness_data,
        "confidence": result['confidence']
    }

# ==========================================
# DEPLOYMENT ENTRY POINT (UPDATED)
# ==========================================
if __name__ == "__main__":
    # Render sets the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
