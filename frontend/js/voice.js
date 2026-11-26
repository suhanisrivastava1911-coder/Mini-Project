/**
 * Web Speech API module: Speech Recognition & Text-to-Speech Synthesis
 * Fully supports Hindi and English with graceful fallback.
 */

class VoiceAssistant {
  constructor() {
    this.recognition = null;
    this.synthesis = window.speechSynthesis;
    this.isRecording = false;
    this.ttsEnabled = true;
    this.initSpeechRecognition();
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'hi-IN'; // Default to Hindi-India, falls back to en-IN
    } else {
      console.warn('Web Speech Recognition API not supported in this browser. Fallback to text input active.');
    }
  }

  startListening(onResult, onStatusChange) {
    if (!this.recognition) {
      alert('Voice recognition is not supported in your browser. Please type your message.');
      return;
    }

    const currentLang = localStorage.getItem('sahayak_lang') || 'hi';
    this.recognition.lang = currentLang === 'en' ? 'en-IN' : 'hi-IN';

    this.recognition.onstart = () => {
      this.isRecording = true;
      if (onStatusChange) onStatusChange(true);
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (onResult) onResult(transcript);
    };

    this.recognition.onerror = (err) => {
      console.error('Speech recognition error:', err);
      this.isRecording = false;
      if (onStatusChange) onStatusChange(false);
    };

    this.recognition.onend = () => {
      this.isRecording = false;
      if (onStatusChange) onStatusChange(false);
    };

    try {
      this.recognition.start();
    } catch (e) {
      console.warn('Speech recognition already active:', e);
    }
  }

  stopListening() {
    if (this.recognition && this.isRecording) {
      this.recognition.stop();
      this.isRecording = false;
    }
  }

  speak(text, lang = 'hi-IN') {
    if (!this.ttsEnabled || !this.synthesis) return;
    this.synthesis.cancel(); // Cancel any ongoing speech

    // Clean markdown before speaking
    const cleanText = text.replace(/[*_#`~[\]]/g, '').replace(/https?:\/\/\S+/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang;
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    this.synthesis.speak(utterance);
  }
}

window.voiceAssistant = new VoiceAssistant();
