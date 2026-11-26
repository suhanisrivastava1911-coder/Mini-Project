/**
 * Conversational AI Assistant Module
 * Connects speech/text input with backend NLP entity extraction, missing-field clarification,
 * and live matched scheme updates.
 */

document.addEventListener('DOMContentLoaded', () => {
  const messagesContainer = document.getElementById('chat-messages-container');
  const textInput = document.getElementById('chat-text-input');
  const btnSend = document.getElementById('btn-send-message');
  const btnVoice = document.getElementById('btn-voice-input');
  const voiceIndicator = document.getElementById('voice-status-indicator');
  const btnTts = document.getElementById('btn-toggle-tts');
  const btnReset = document.getElementById('btn-reset-chat');
  const langSelect = document.getElementById('chat-lang-select');
  const activeLangStatus = document.getElementById('active-lang-status');

  // Side Tab controls
  const tabProfileBtn = document.getElementById('tab-profile-btn');
  const tabMatchesBtn = document.getElementById('tab-matches-btn');
  const tabProfileContent = document.getElementById('tab-profile-content');
  const tabMatchesContent = document.getElementById('tab-matches-content');
  const btnSaveExtracted = document.getElementById('btn-save-extracted-profile');
  const btnTriggerMatch = document.getElementById('btn-trigger-match');

  let sessionId = localStorage.getItem('sahayak_chat_session') || 'sess_' + Date.now();
  localStorage.setItem('sahayak_chat_session', sessionId);

  let currentExtractedProfile = {};

  // Tab switching
  tabProfileBtn?.addEventListener('click', () => {
    tabProfileBtn.classList.add('active');
    tabMatchesBtn.classList.remove('active');
    tabProfileContent.classList.add('active');
    tabMatchesContent.classList.remove('active');
  });

  tabMatchesBtn?.addEventListener('click', () => {
    tabMatchesBtn.classList.add('active');
    tabProfileBtn.classList.remove('active');
    tabMatchesContent.classList.add('active');
    tabProfileContent.classList.remove('active');
  });

  // Language status
  langSelect?.addEventListener('change', (e) => {
    const lang = e.target.value;
    activeLangStatus.textContent = `Speaking: ${lang.toUpperCase()}`;
    if (window.i18n) window.i18n.setLanguage(lang);
  });

  // Voice toggle
  let ttsActive = true;
  btnTts?.addEventListener('click', () => {
    ttsActive = !ttsActive;
    window.voiceAssistant.ttsEnabled = ttsActive;
    btnTts.textContent = ttsActive ? '🔊' : '🔇';
    btnTts.title = ttsActive ? 'Voice enabled' : 'Voice muted';
  });

  // Voice recording button
  btnVoice?.addEventListener('click', () => {
    if (window.voiceAssistant.isRecording) {
      window.voiceAssistant.stopListening();
    } else {
      window.voiceAssistant.startListening(
        (transcript) => {
          textInput.value = transcript;
          sendMessage();
        },
        (isRecording) => {
          if (isRecording) {
            voiceIndicator.classList.remove('hidden');
            btnVoice.classList.add('recording');
          } else {
            voiceIndicator.classList.add('hidden');
            btnVoice.classList.remove('recording');
          }
        }
      );
    }
  });

  // Send message handler
  async function sendMessage() {
    const message = textInput.value.trim();
    if (!message) return;

    // Append user message to UI
    appendMessage('user', message);
    textInput.value = '';
    textInput.style.height = 'auto';

    // Show bot typing indicator
    const typingId = appendTypingIndicator();

    try {
      const res = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: message,
          language: langSelect ? langSelect.value : 'hi'
        })
      });

      removeTypingIndicator(typingId);

      if (res.ok) {
        const data = await res.json();
        const botReply = data.reply || 'धन्यवाद। आपकी जानकारी नोट कर ली गई है।';
        appendMessage('bot', botReply);

        // TTS voice readout
        if (ttsActive && window.voiceAssistant) {
          const ttsLang = (langSelect && langSelect.value === 'en') ? 'en-IN' : 'hi-IN';
          window.voiceAssistant.speak(botReply, ttsLang);
        }

        // Update extracted profile fields
        if (data.extracted_profile) {
          updateExtractedProfileForm(data.extracted_profile);
        }

        // Update live matches if any
        if (data.matched_schemes && data.matched_schemes.length > 0) {
          renderLiveMatches(data.matched_schemes);
        }
      } else {
        appendMessage('bot', 'क्षमा करें, संदेश प्रोसेस करने में समस्या हुई। कृपया दोबारा प्रयास करें।');
      }
    } catch (err) {
      removeTypingIndicator(typingId);
      appendMessage('bot', 'कनेक्शन में त्रुटि हुई। कृपया नेटवर्क जांचें।');
    }
  }

  btnSend?.addEventListener('click', sendMessage);
  textInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Quick prompt chips
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      textInput.value = chip.getAttribute('data-prompt');
      sendMessage();
    });
  });

  // Clear chat
  btnReset?.addEventListener('click', () => {
    sessionId = 'sess_' + Date.now();
    localStorage.setItem('sahayak_chat_session', sessionId);
    messagesContainer.innerHTML = `
      <div class="chat-msg bot-msg">
        <div class="msg-avatar">🤖</div>
        <div class="msg-bubble">
          <p><strong>नमस्ते!</strong> बातचीत रीसेट हो गई है। अपने व्यवसाय के बारे में बताएं।</p>
        </div>
      </div>
    `;
    currentExtractedProfile = {};
    document.getElementById('extracted-profile-form')?.reset();
    document.getElementById('live-matches-list').innerHTML = '<p class="text-muted text-xs p-3">Schemes will appear here in real time.</p>';
    document.getElementById('live-match-count').textContent = '0';
  });

  // Save extracted profile to account
  btnSaveExtracted?.addEventListener('click', async () => {
    syncFormToProfile();
    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentExtractedProfile)
      });
      if (res.ok) {
        alert('Extracted profile saved successfully to your account!');
      } else {
        alert('Please log in to persist profile to account, or continue in guest mode.');
      }
    } catch (e) {
      alert('Failed to save profile.');
    }
  });

  // Trigger match button
  btnTriggerMatch?.addEventListener('click', async () => {
    syncFormToProfile();
    await fetchMatchesForProfile(currentExtractedProfile);
    tabMatchesBtn?.click();
  });

  function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}-msg`;
    msgDiv.innerHTML = `
      <div class="msg-avatar">${sender === 'bot' ? '🤖' : '👤'}</div>
      <div class="msg-bubble">${formatChatMessage(text)}</div>
    `;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendTypingIndicator() {
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'chat-msg bot-msg';
    div.innerHTML = `
      <div class="msg-avatar">🤖</div>
      <div class="msg-bubble">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
  }

  function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function formatChatMessage(text) {
    if (!text) return '';
    return text.replace(/\n/g, '<br>');
  }

  function updateExtractedProfileForm(extracted) {
    currentExtractedProfile = { ...currentExtractedProfile, ...extracted };
    if (extracted.gender) document.getElementById('field-gender').value = extracted.gender;
    if (extracted.social_category) document.getElementById('field-category').value = extracted.social_category;
    if (extracted.state) document.getElementById('field-state').value = extracted.state;
    if (extracted.district) document.getElementById('field-district').value = extracted.district;
    if (extracted.business_sector) document.getElementById('field-sector').value = extracted.business_sector;
    if (extracted.business_stage) document.getElementById('field-stage').value = extracted.business_stage;
    if (extracted.funding_requirement) document.getElementById('field-funding').value = extracted.funding_requirement;
  }

  function syncFormToProfile() {
    currentExtractedProfile.gender = document.getElementById('field-gender').value;
    currentExtractedProfile.social_category = document.getElementById('field-category').value;
    currentExtractedProfile.state = document.getElementById('field-state').value;
    currentExtractedProfile.district = document.getElementById('field-district').value;
    currentExtractedProfile.business_sector = document.getElementById('field-sector').value;
    currentExtractedProfile.business_stage = document.getElementById('field-stage').value;
    currentExtractedProfile.funding_requirement = parseFloat(document.getElementById('field-funding').value) || 0;
  }

  async function fetchMatchesForProfile(profile) {
    try {
      const res = await fetch('/api/matching/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_data: profile })
      });
      if (res.ok) {
        const data = await res.json();
        renderLiveMatches(data.recommendations || []);
      }
    } catch (e) {
      console.warn('Match trigger error:', e);
    }
  }

  function renderLiveMatches(matches) {
    const list = document.getElementById('live-matches-list');
    const badgeCount = document.getElementById('live-match-count');
    badgeCount.textContent = matches.length;

    if (matches.length === 0) {
      list.innerHTML = '<p class="text-muted text-xs p-3">No matching schemes for this exact profile.</p>';
      return;
    }

    list.innerHTML = matches.map(m => `
      <div class="scheme-match-card p-2 mb-2">
        <div class="flex-between">
          <strong class="text-navy text-xs">${escapeHtml(m.scheme_name)}</strong>
          <span class="match-score-badge text-xs">${Math.round(m.match_score || 0)}%</span>
        </div>
        <p class="text-xs text-muted mt-1">${escapeHtml((m.reasons || [])[0] || 'Eligible under ministry guidelines')}</p>
        <div class="flex-between align-center mt-2">
          <span class="text-xs font-bold text-navy">₹${formatCurrency(m.max_benefit_amount)}</span>
          <a href="/pages/scheme_details.html?id=${m.scheme_id}" class="btn btn-xs btn-outline">Details &rarr;</a>
        </div>
      </div>
    `).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[m]));
  }

  function formatCurrency(val) {
    if (!val) return 'Varies';
    const num = Number(val);
    if (num >= 10000000) return (num / 10000000).toFixed(1) + ' Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + ' Lakh';
    return num.toLocaleString('en-IN');
  }
});
