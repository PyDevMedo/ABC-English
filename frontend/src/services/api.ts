const API_HOST = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
const API_BASE = `${API_HOST}/api/v1`;

export const getAuthToken = () => localStorage.getItem('token');
export const setAuthToken = (token: string) => localStorage.setItem('token', token);
export const removeAuthToken = () => localStorage.removeItem('token');

const getHeaders = (isFormData: boolean = false) => {
  const token = getAuthToken();
  const headers: Record<string, string> = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }
  return headers;
};

// Play audio helper with fallback to SpeechSynthesis
export const playAudio = (audioUrl?: string, fallbackText?: string) => {
  if (audioUrl) {
    const audio = new Audio(audioUrl);
    audio.play().catch(() => {
      if (fallbackText && 'speechSynthesis' in window) {
        speakText(fallbackText);
      }
    });
  } else if (fallbackText && 'speechSynthesis' in window) {
    speakText(fallbackText);
  }
};

export const speakText = (text: string, options?: { volume?: number; rate?: number; pitch?: number }) => {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US';
  utterance.volume = options?.volume ?? 1.0; // Maximum volume
  utterance.rate = options?.rate ?? 0.80; // clear, deliberate child pace
  utterance.pitch = options?.pitch ?? 1.05;

  // Try selecting the highest clarity English voice
  try {
    const voices = window.speechSynthesis.getVoices();
    const bestVoice = voices.find(v => 
      v.lang.startsWith('en') && (
        v.name.includes('Google') || 
        v.name.includes('Natural') || 
        v.name.includes('Samantha') || 
        v.name.includes('David') || 
        v.name.includes('US')
      )
    );
    if (bestVoice) {
      utterance.voice = bestVoice;
    }
  } catch {
    // fallback to default
  }

  window.speechSynthesis.speak(utterance);
};

export const api = {
  // Auth
  async register(data: { full_name: string; phone_number: string; password: string; avatar?: string }) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل في إنشاء الحساب');
    }
    return res.json();
  },

  async login(data: { phone_number: string; password: string }) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل في تسجيل الدخول');
    }
    const tokenData = await res.json();
    setAuthToken(tokenData.access_token);
    return tokenData;
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders()
    });
    if (!res.ok) throw new Error('Unauthenticated');
    return res.json();
  },

  // Curriculum
  async getLevels() {
    const res = await fetch(`${API_BASE}/curriculum/levels`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async getLevelDetail(levelId: number) {
    const res = await fetch(`${API_BASE}/curriculum/levels/${levelId}`, {
      headers: getHeaders()
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل تحميل المستوى');
    }
    return res.json();
  },

  async completeLesson(lessonId: number) {
    const res = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}/complete`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  // Pronunciation Evaluation
  async evaluatePronunciation(targetText: string, audioBlob?: Blob, simulatedSpeech?: string) {
    const formData = new FormData();
    formData.append('target_text', targetText);
    if (audioBlob) {
      formData.append('audio_file', audioBlob, 'recording.wav');
    }
    if (simulatedSpeech) {
      formData.append('simulated_speech', simulatedSpeech);
    }
    const res = await fetch(`${API_BASE}/pronunciation/evaluate`, {
      method: 'POST',
      headers: getHeaders(true),
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل في تقييم النطق');
    }
    return res.json();
  },

  // Adaptive Learning
  async getLearningPlan() {
    const res = await fetch(`${API_BASE}/adaptive/plan`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async completeAdaptiveExercise(exerciseId: number, score: number = 100) {
    const res = await fetch(`${API_BASE}/adaptive/exercises/${exerciseId}/complete?score=${score}`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  // Assignments
  async getAssignments() {
    const res = await fetch(`${API_BASE}/assignments/`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async getMySubmissions() {
    const res = await fetch(`${API_BASE}/assignments/my-submissions`, {
      headers: getHeaders()
    });
    if (!res.ok) throw new Error('فشل جلب سجل تسليمات الواجبات');
    return res.json();
  },

  async getAssignmentByLevel(levelId: number) {
    const res = await fetch(`${API_BASE}/assignments/by-level/${levelId}`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async submitHandwritingPhoto(assignmentId: number, imageBlob: Blob) {
    const formData = new FormData();
    formData.append('assignment_id', assignmentId.toString());
    formData.append('submission_type', 'handwriting_photo');
    formData.append('image_file', imageBlob, 'notebook_homework.jpg');

    const res = await fetch(`${API_BASE}/assignments/submit`, {
      method: 'POST',
      headers: getHeaders(true),
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل في رفع صورة الواجب');
    }
    return res.json();
  },

  async submitAssignment(assignmentId: number, submissionType: string, textContent?: string, audioBlob?: Blob) {
    const formData = new FormData();
    formData.append('assignment_id', assignmentId.toString());
    formData.append('submission_type', submissionType);
    if (textContent) formData.append('text_content', textContent);
    if (audioBlob) formData.append('audio_file', audioBlob, 'assignment.mp3');

    const res = await fetch(`${API_BASE}/assignments/submit`, {
      method: 'POST',
      headers: getHeaders(true),
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'فشل في تسليم الواجب');
    }
    return res.json();
  },

  // Quizzes
  async getLevelQuiz(levelId: number) {
    const res = await fetch(`${API_BASE}/quizzes/${levelId}`, {
      headers: getHeaders()
    });
    if (!res.ok) throw new Error('فشل تحميل الاختبار');
    return res.json();
  },

  async submitQuiz(quizId: number, answers: Record<string, any>) {
    const res = await fetch(`${API_BASE}/quizzes/submit`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ quiz_id: quizId, answers })
    });
    if (!res.ok) throw new Error('فشل تصحيح الاختبار');
    return res.json();
  },

  // Gamification & Dashboard
  async getGamificationDashboard() {
    const res = await fetch(`${API_BASE}/gamification/dashboard`, {
      headers: getHeaders()
    });
    return res.json();
  },

  // Telegram Link Code
  async generateTelegramLink() {
    const res = await fetch(`${API_BASE}/telegram/generate-link-code`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  }
};
