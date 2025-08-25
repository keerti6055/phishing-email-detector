let currentEmailId = null;

// --- ADVANCED FEATURE: PERSONAL TRUST LIST ---

// Function to get the user's personal trust list from browser storage.
async function getTrustList() {
  const data = await chrome.storage.local.get('trustList');
  // If the list doesn't exist yet, return an empty array.
  return data.trustList || [];
}

// Function to add a new sender's domain to the trust list.
async function trustSender(senderDomain) {
  const trustList = await getTrustList();
  if (!trustList.includes(senderDomain)) {
    trustList.push(senderDomain);
    await chrome.storage.local.set({ trustList: trustList });
    console.log(`✅ ${senderDomain} has been added to your personal trust list.`);
  }
}

// Function to check if a sender is on the user's personal trust list.
async function isSenderTrusted(sender) {
  const senderDomain = sender.substring(sender.lastIndexOf("@") + 1);
  const trustList = await getTrustList();
  return trustList.includes(senderDomain);
}


// --- CORE LOGIC (with updates) ---

async function getPhishingVerdict(emailText) {
  // No changes here, it still just talks to the Python server.
  try {
    const response = await fetch('http://127.0.0.1:5000/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email_text: emailText }),
    });
    const data = await response.json();
    return data.result;
  } catch (error) {
    console.error('Error contacting API:', error);
    return 'API_ERROR';
  }
}

function displayVerdictBanner(verdict, parentElement, sender) {
  const oldBanner = document.getElementById('phishing-verdict-banner');
  if (oldBanner) oldBanner.remove();

  const banner = document.createElement('div');
  banner.id = 'phishing-verdict-banner';

  let backgroundColor, icon, message;
  
  // Set banner content based on verdict
  switch (verdict) {
    case 'SAFE':
      backgroundColor = '#d4edda'; icon = '✅'; message = 'This email seems safe.'; break;
    case 'CAUTION':
      backgroundColor = '#fff3cd'; icon = '⚠️'; message = 'CAUTION: This email contains suspicious words.'; break;
    case 'SPAM':
      backgroundColor = '#f8d7da'; icon = '🚨'; message = 'DANGER: This is likely a phishing attempt!'; break;
    default:
      backgroundColor = '#e2e3e5'; icon = '🔌'; message = 'Error: Could not connect to the analysis server.';
  }
  
  banner.style.cssText = `background-color: ${backgroundColor}; padding: 15px; text-align: center; font-size: 16px; border-radius: 8px; margin-bottom: 15px; font-weight: bold;`;
  banner.textContent = `${icon} ${message}`;
  
  // --- ADVANCED FEATURE: ADD THE "TRUST SENDER" BUTTON ---
  if (verdict === 'CAUTION' || verdict === 'SPAM') {
    const trustButton = document.createElement('button');
    trustButton.textContent = '✔️ Always Trust This Sender';
    trustButton.style.cssText = `margin-left: 20px; padding: 5px 10px; border: 1px solid #333; border-radius: 5px; cursor: pointer; background-color: #fff;`;
    
    trustButton.onclick = async () => {
      const senderDomain = sender.substring(sender.lastIndexOf("@") + 1);
      await trustSender(senderDomain);
      // Give instant feedback by changing the banner to SAFE.
      displayVerdictBanner('SAFE', parentElement, sender);
    };
    
    banner.appendChild(trustButton);
  }
  
  parentElement.prepend(banner);
}

async function scanEmail() {
  const emailView = document.querySelector('.hP');
  if (!emailView) return;

  const emailIdentifier = emailView.innerText.substring(0, 100);
  if (emailIdentifier === currentEmailId) return;
  
  currentEmailId = emailIdentifier;
  console.log("📧 New email detected! Scanning...");
  
  const senderElement = document.querySelector('span.gD');
  const senderEmailElement = document.querySelector('span.go');
  const sender = senderEmailElement ? senderEmailElement.innerText.replace(/[<>]/g, '') : (senderElement ? senderElement.getAttribute('email') : 'unknown');

  // --- ADVANCED FEATURE: CHECK PERSONAL TRUST LIST FIRST ---
  if (await isSenderTrusted(sender)) {
    console.log(`👍 Sender ${sender} is on your personal trust list. Marking as SAFE.`);
    displayVerdictBanner('SAFE', emailView, sender);
    return; // Stop further scanning
  }

  const subjectElement = document.querySelector('h2.hP');
  const bodyElement = document.querySelector('div.adn');

  if (subjectElement && bodyElement) {
    const fullEmailText = `Subject: ${subjectElement.innerText}\n\n${bodyElement.innerText}`;
    const verdict = await getPhishingVerdict(fullEmailText);
    console.log(`🚨 API Verdict for sender '${sender}': ${verdict}`);
    displayVerdictBanner(verdict, emailView, sender);
  }
}

setInterval(scanEmail, 2000);