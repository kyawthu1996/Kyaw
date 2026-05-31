```react
import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Volume2, 
  Settings, 
  Mic, 
  Sparkles, 
  Download, 
  Info, 
  Trash2, 
  Loader2, 
  FileText, 
  Sliders, 
  AlertTriangle,
  Compass,
  ExternalLink
} from 'lucide-react';

const apiKey = ""; 
const MODEL_NAME = "gemini-2.5-flash-preview-tts";

const VOICE_OPTIONS = [
  { name: "Algenib", style: "Gravelly", description: "အက်ကွဲကွဲနှင့် ကြမ်းတမ်းဆတ်ဆတ် (ဒေါသထွက်သံ သို့မဟုတ် ဆဲဆိုရန်တွေ့သံအတွက် အကောင်းဆုံး)", previewText: "[angry] Listen to me! What on earth are you doing with my phone?! Put it down!" },
  { name: "Gacrux", style: "Mature/Deep", description: "အသံနက်နက် ကြီးကြီး (အသက်ဝင်ပြီး လေးနက်သော လေသံအတွက် သင့်လျော်သည်)", previewText: "[serious] Stop right there. Do not make another move." },
  { name: "Erinome", style: "Clear", description: "စူးရှပြတ်သားပြီး ခနဲ့တဲ့တဲ့ (ရန်တွေ့သံ သို့မဟုတ် အပြစ်တင်သံအတွက် သင့်လျော်သည်)", previewText: "[sarcastically] Oh, beautiful! Just brilliant! You dropped my phone again." },
  { name: "Enceladus", style: "Breathy", description: "အသံနက်နက် နှေးနှေး (တိုးတိုးရေရွတ်သံ သို့မဟုတ် လျှို့ဝှက်သံအတွက် သင့်လျော်သည်)", previewText: "[whispers] Hello. I deliver deep, breathy, and slow emotional reads." }
];

const SCENE_PRESETS = [
  {
    id: "furious",
    name: "Heated Argument (ရန်ဖြစ်နေသောအခင်းအကျင်း)",
    notes: "Style: [angry] Very loud, fast, aggressive pacing, gravelly undertones with gasps of air."
  },
  {
    id: "sarcastic",
    name: "Sarcastic Confrontation (ခနဲ့တဲ့တဲ့ ရန်တွေ့ခြင်း)",
    notes: "Style: [sarcastically] Painfully slow words, mocking tone, sighing heavily between sentences."
  }
];

const POPULAR_TAGS = [
  { tag: "[excitedly]", desc: "စိတ်လှုပ်ရှားသံ" },
  { tag: "[whispers]", desc: "တိုးတိုးပြောသံ" },
  { tag: "[sighs]", desc: "သက်ပြင်းချသံ" },
  { tag: "[laughs]", desc: "ရယ်မောသံ" },
  { tag: "[gasp]", desc: "အံ့သြသံ" },
  { tag: "[shouting]", desc: "အော်ဟစ်သံ" },
  { tag: "[angry]", desc: "ဒေါသတကြီး" },
  { tag: "[sarcastically]", desc: "ခနဲ့တဲ့တဲ့" }
];

export default function App() {
  const [ttsMode, setTtsMode] = useState("single");
  const [customScene, setCustomScene] = useState("An extremely angry, chaotic, and dramatic Burmese rant with heavy breathing and swearing");
  const [singleVoice, setSingleVoice] = useState("Algenib");
  const [multiSpeakers, setMultiSpeakers] = useState([
    { name: "Speaker1", voice: "Algenib" },
    { name: "Speaker2", voice: "Gacrux" }
  ]);

  // Live Logger
  const [logs, setLogs] = useState([]);

  const addLog = (msg) => {
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`].slice(-8));
  };
  
  const [promptText, setPromptText] = useState(
    `# THE SCENE: Extremely angry, chaotic, and dramatic Burmese rant with heavy breathing\n# DIRECTOR'S NOTES: [angry] Gravelly voice, emotional, shouting, sighing and laughing naturally.\n\n[excitedly] ဟျောင့် ခဏလေး... [laughs] ငါလိုးမသားလား။ အမလေး... [sighs] ဖေဖေ ငါလိုးမသားသားတွေရာ... ဖုန်းကို ကမ်းခြေက အခင်းပေါ်မှာ ဒီတိုင်း ပစ်ထားခဲ့ရင်... [shouting] ငါလိုးမသား သူခိုးက ခိုးသွားမှာပေါ့ကွ! [laughs] ဟီး... အဲ့လိုမဖြစ်အောင် နည်းလမ်းကောင်းတစ်ခု ပေးမယ်... အရင်ဆုံး ဂေါ်ပြားတစ်ချောင်းယူ... ပြီးရင် လက်တစ်ချောင်းစာလောက်နက်အောင် တူးပြီး စွတ်တိုးပစ်လိုက်... ပြီးမှ ဖုန်းကို အောက်ခြေထဲ ပစ်ချထားလိုက်ဦးမယ်... ဒါပေမဲ့ နေဦး... ဒါနဲ့တင် စိတ်မချရသေးဘူးကွာ... [whispers] ဂေါ်ပြားကို သဲပေါ်မှာ ဒီတိုင်း ပစ်ထားခဲ့ရင်... [shouting] ငါလိုးမသား တစ်ခုက အချောင်ရပြီး အဲ့ဒီဂေါ်ပြားနဲ့ပဲ ပြန်တူးသွားမှာပေါ့ ငါလိုးမသားရဲ့! [sighs] ဟေး... အဲ့ဒါကြောင့် ဖုန်းအပေါ်ကနေပြီး ဂေါ်ပြားကိုပါ ထပ်မြှုပ်ပစ်လိုက်ကွာ... ပြီးရင်တော့ သဲတွေကို လက်နဲ့ပဲ ကုပ်ကပ်ပြီး ပြန်ဖုံး... အပေါ်ကနေ အခင်းလေး ပြန်ခင်းထားလိုက်ကွာ... ကဲ... အားလုံး အိုကေပြီ... ဒါပေမဲ့ မင်းကိုယ်တိုင် ဖုန်းပြန်သုံးချင်တဲ့အချိန်ကျရင်... [gasp] ဂေါ်ပြားမရှိဘဲ ဘယ်လိုပြန်တူးလဲဆိုတာကတော့... ခေါင်းအေးအေးလေးနဲ့ စဉ်းစားလိုက်တော့ကွာ... [laughs] follow လုပ်သွားတဲ့ ငါလိုးမသားတွေ အားလုံး အိုဂျီ ဒီပေါက် နိဗ္ဗာန် ရောက်ပါစေကွာ...`
  );
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [previewingVoiceName, setPreviewingVoiceName] = useState(null); 
  const [errorMsg, setErrorMsg] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const audioRef = useRef(null);
  const previewAudioRef = useRef(null);
  const [previewAudioUrl, setPreviewAudioUrl] = useState(null);
  const [isPreviewPlaying, setIsPreviewPlaying] = useState(false);

  // Force reload audio when url updates
  useEffect(() => {
    if (audioRef.current && audioUrl) {
      addLog("အဓိက အသံဖိုင်ကို ပြန်လည်စတင် တင်သွင်းနေပါသည်...");
      audioRef.current.load();
    }
  }, [audioUrl]);

  useEffect(() => {
    if (previewAudioRef.current && previewAudioUrl) {
      addLog("နမူနာ အသံဖိုင်ကို ပြန်လည်စတင် တင်သွင်းနေပါသည်...");
      previewAudioRef.current.load();
    }
  }, [previewAudioUrl]);

  const handleCustomSceneChange = (newScene) => {
    setCustomScene(newScene);
    setPromptText(prev => {
      const hasSceneHeader = prev.includes("# THE SCENE:");
      if (hasSceneHeader) {
        return prev.replace(/^# THE SCENE:[^\n]*/m, `# THE SCENE: ${newScene}`);
      } else {
        return `# THE SCENE: ${newScene}\n${prev}`;
      }
    });
  };

  const applyPresetScene = (preset) => {
    setCustomScene(preset.name);
    setPromptText(prev => {
      const textWithoutHeader = prev.replace(/^# THE SCENE:.*?\n# DIRECTOR'S NOTES:.*?\n/s, "");
      return `# THE SCENE: ${preset.name}\n# DIRECTOR'S NOTES: ${preset.notes}\n${textWithoutHeader}`;
    });
    addLog(`အခင်းအကျင်း ပြောင်းလဲလိုက်ပါသည်: ${preset.name}`);
  };

  // Base64 အသံလှိုင်းဒေတာကို Playable WAV အဖြစ်ပြောင်းလဲပေးသည့်စနစ်
  const pcmToWavBlobUrl = (pcmBase64, sampleRate = 24000) => {
    try {
      const cleanBase64 = pcmBase64.replace(/\s/g, '');
      const binaryString = window.atob(cleanBase64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const buffer = bytes.buffer;
      
      const wavHeader = new ArrayBuffer(44);
      const view = new DataView(wavHeader);
      
      const writeString = (view, offset, string) => {
        for (let i = 0; i < string.length; i++) {
          view.setUint8(offset + i, string.charCodeAt(i));
        }
      };

      writeString(view, 0, 'RIFF');
      view.setUint32(4, 36 + buffer.byteLength, true);
      writeString(view, 8, 'WAVE');
      writeString(view, 12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true);
      view.setUint16(22, 1, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * 2, true);
      view.setUint16(32, 2, true);
      view.setUint16(34, 16, true);
      writeString(view, 36, 'data');
      view.setUint32(40, buffer.byteLength, true);
      
      const blob = new Blob([wavHeader, buffer], { type: 'audio/wav' });
      addLog("WAV အသံဖိုင်ဒေတာ တည်ဆောက်မှု အောင်မြင်ပါသည်။");
      return URL.createObjectURL(blob);
    } catch (e) {
      console.error("PCM transformation error:", e);
      addLog(`Error: အသံဖိုင်ဒေတာပြောင်းလဲရန် မအောင်မြင်ပါ (${e.message})`);
      throw new Error("WAV အဖြစ်ပြောင်းလဲရန် မအောင်မြင်ပါ။");
    }
  };

  // ရွေးချယ်ထားသောအသံကို စမ်းသပ်နားထောင်ခြင်း
  const handlePreviewVoice = async (voiceName) => {
    if (previewingVoiceName === voiceName && isPreviewPlaying) {
      if (previewAudioRef.current) {
        previewAudioRef.current.pause();
        setIsPreviewPlaying(false);
      }
      return;
    }

    setPreviewingVoiceName(voiceName);
    setIsPreviewPlaying(false);
    setErrorMsg(null);
    addLog(`နမူနာစမ်းသပ်မှု စတင်နေပါသည် (Voice: ${voiceName})...`);

    const voiceInfo = VOICE_OPTIONS.find(v => v.name === voiceName);
    const textToSpeak = voiceInfo ? voiceInfo.previewText : "Testing voice preset.";

    const payload = {
      contents: [{ parts: [{ text: textToSpeak }] }],
      generationConfig: {
        responseModalities: ["AUDIO"],
        speechConfig: {
          voiceConfig: {
            prebuiltVoiceConfig: {
              voiceName: voiceName
            }
          }
        }
      }
    };

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${apiKey}`;

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`နမူနာအသံ တောင်းဆိုမှု မအောင်မြင်ပါ (Status: ${res.status})`);
      }

      const result = await res.json();
      const pcmData = result.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;

      if (!pcmData) {
        throw new Error("အသံလှိုင်းဒေတာ အလွတ်ဖြစ်နေပါသည်။");
      }

      const generatedUrl = pcmToWavBlobUrl(pcmData, 24000);
      setPreviewAudioUrl(generatedUrl);

      setTimeout(() => {
        if (previewAudioRef.current) {
          previewAudioRef.current.play()
            .then(() => {
              setIsPreviewPlaying(true);
              addLog("နမူနာအသံ ဖွင့်နေပါသည်...");
            })
            .catch(err => {
              addLog("Error: Browser မှ အသံဖွင့်ခြင်းကို တားဆီးထားပါသည်။");
              console.log("Audio play blocked", err);
            });
        }
      }, 150);

    } catch (e) {
      setErrorMsg(e.message);
      addLog(`Error: ${e.message}`);
      setPreviewingVoiceName(null);
    }
  };

  // အသံအမှန်ပြောင်းလဲခြင်း လုပ်ဆောင်ချက်
  const executeTtsGeneration = async () => {
    setIsGenerating(true);
    setErrorMsg(null);
    setAudioUrl(null);
    addLog("Gemini API သို့ အသံပြောင်းလဲရန် တောင်းဆိုနေပါသည်...");
    
    let speechConfig = {};
    if (ttsMode === "single") {
      speechConfig = {
        voiceConfig: {
          prebuiltVoiceConfig: {
            voiceName: singleVoice
          }
        }
      };
    } else {
      speechConfig = {
        multiSpeakerVoiceConfig: {
          speakerVoiceConfigs: multiSpeakers.map(sp => ({
            speaker: sp.name,
            voiceConfig: {
              prebuiltVoiceConfig: {
                voiceName: sp.voice
              }
            }
          }))
        }
      };
    }

    const payload = {
      contents: [{ parts: [{ text: promptText }] }],
      generationConfig: {
        responseModalities: ["AUDIO"],
        speechConfig: speechConfig
      }
    };

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${apiKey}`;

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errorDetail = await res.json().catch(() => ({}));
        throw new Error(errorDetail.error?.message || `ချိတ်ဆက်မှု မအောင်မြင်ပါ (Status: ${res.status})`);
      }

      const result = await res.json();
      const pcmData = result.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;

      if (!pcmData) {
        throw new Error("အသံဖိုင်ထုတ်လုပ်၍မရပါ။ စာသားကို ပြန်လည်စစ်ဆေးပါ။");
      }
      
      const generatedWavUrl = pcmToWavBlobUrl(pcmData, 24000);
      setAudioUrl(generatedWavUrl);
      addLog("အသံဖိုင် ပြောင်းလဲမှု ပြီးဆုံးပါပြီ။");
    } catch (e) {
      setErrorMsg(e.message);
      addLog(`Error: ${e.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  // Programmatic Robust Download Function
  const handleDownload = () => {
    if (!audioUrl) return;
    try {
      addLog("အသံဖိုင် တိုက်ရိုက်ဒေါင်းလုတ်ဆွဲရန် ကြိုးစားနေပါသည်...");
      
      const link = document.createElement('a');
      link.href = audioUrl;
      link.download = `gemini-voice-${Date.now()}.wav`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      addLog("တိုက်ရိုက်ဒေါင်းလုတ်ဆွဲယူခြင်းကို တောင်းဆိုလိုက်ပါပြီ။");
    } catch (e) {
      addLog(`Error: ဒေါင်းလုတ်ဆွဲရာတွင် ပြဿနာရှိနေပါသည် (${e.message})`);
      setErrorMsg("ဒေါင်းလုတ်ပြုလုပ်ရန် မအောင်မြင်ပါ။ အောက်ပါ 'ဝင်းဒိုးအသစ်တွင်ဖွင့်ပြီး သိမ်းဆည်းပါ' ခလုတ်ကို သုံးကြည့်ပါ။");
    }
  };

  // Alternative Open in New Tab for Safe Download Fallback
  const handleOpenInNewTab = () => {
    if (!audioUrl) return;
    addLog("အသံဖိုင်အား တဘ်အသစ်တွင် ဖွင့်လှစ်နေပါသည်...");
    window.open(audioUrl, '_blank');
    addLog("ဖွင့်လှစ်ပြီးပါက အသံဖွင့်စက်ပေါ်တွင် ညာဘက်ကလစ်နှိပ်ပြီး 'Save Audio As...' ဖြင့် သိမ်းဆည်းနိုင်ပါသည်။");
  };

  const insertTag = (tag) => {
    setPromptText(prev => prev + " " + tag + " ");
  };

  const updateSpeaker = (idx, field, value) => {
    const next = [...multiSpeakers];
    next[idx][field] = value;
    setMultiSpeakers(next);
  };

  const handleAudioPlayback = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play()
        .then(() => addLog("အဓိက အသံဖိုင်ကို ဖွင့်နေပါသည်..."))
        .catch(err => addLog(`Error: အသံဖွင့်ရန် မအောင်မြင်ပါ (${err.message})`));
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Header Banner */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-tr from-purple-600 to-indigo-600 rounded-xl text-white shadow-lg">
            <Mic className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight">Gemini Voice Studio</h1>
            <p className="text-xs text-slate-400">စာသားမှ အသံပြောင်းလဲပေးသော စနစ် (အလိုအလျောက် Key ချိတ်ဆက်ထားပါသည်)</p>
          </div>
        </div>
      </header>

      {/* Hidden audio tag for voice previews */}
      <audio 
        ref={previewAudioRef} 
        src={previewAudioUrl} 
        onPlay={() => setIsPreviewPlaying(true)}
        onPause={() => setIsPreviewPlaying(false)}
        onEnded={() => {
          setIsPreviewPlaying(false);
          setPreviewingVoiceName(null);
        }}
        className="hidden"
      />

      <main className="flex-1 max-w-5xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Input Panel */}
        <div className="lg:col-span-8 flex flex-col gap-6">

          {/* Scene Selector Board (Custom Text Input) */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-1.5 border-b border-slate-800 pb-3 mb-3">
              <Compass className="w-4 h-4 text-indigo-400" />
              Scene အခင်းအကျင်း နောက်ခံသတ်မှတ်ချက်
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">အသံနောက်ခံ အခြေအနေကို စိတ်ကြိုက်ရေးသားရန်</label>
                <input
                  type="text"
                  value={customScene}
                  onChange={(e) => handleCustomSceneChange(e.target.value)}
                  placeholder="ဥပမာ- Angry fight, shouting, high tension..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>
              <div>
                <span className="block text-[10px] text-slate-500 uppercase tracking-wider font-bold mb-2">ရန်ပွဲ/ခနဲ့သံ ပုံစံနမူနာများ</span>
                <div className="flex flex-wrap gap-2">
                  {SCENE_PRESETS.map((preset) => (
                    <button
                      key={preset.id}
                      onClick={() => applyPresetScene(preset)}
                      className="px-2.5 py-1 text-xs bg-slate-950 border border-slate-800 rounded-lg hover:border-indigo-500 hover:text-indigo-400 transition"
                    >
                      {preset.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Speakers */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-4">
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-1.5">
                <Settings className="w-4 h-4 text-indigo-400" />
                အသံရွေးချယ်ရန် (အသံဖိုင်နှင့် တူညီသော အသံများကို ဦးစားပေးထားပါသည်)
              </h2>
              
              <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
                <button 
                  onClick={() => setTtsMode("single")}
                  className={`px-3 py-1.5 text-xs rounded-md transition-all ${ttsMode === 'single' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
                >
                  အသံတစ်ဦးတည်း
                </button>
                <button 
                  onClick={() => setTtsMode("multi")}
                  className={`px-3 py-1.5 text-xs rounded-md transition-all ${ttsMode === 'multi' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
                >
                  အသံနှစ်ဦး (အလှည့်ကျ)
                </button>
              </div>
            </div>

            {ttsMode === "single" ? (
              <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
                <div className="md:col-span-4 flex gap-2">
                  <select 
                    value={singleVoice}
                    onChange={(e) => {
                      setSingleVoice(e.target.value);
                      addLog(`အဓိက အသံရှင် ပြောင်းလဲလိုက်သည်: ${e.target.value}`);
                    }}
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none"
                  >
                    {VOICE_OPTIONS.map(v => (
                      <option key={v.name} value={v.name}>{v.name} ({v.style})</option>
                    ))}
                  </select>
                  <button
                    onClick={() => handlePreviewVoice(singleVoice)}
                    className={`px-3 py-2 text-xs font-bold rounded-xl flex items-center gap-1 transition-all ${
                      previewingVoiceName === singleVoice && isPreviewPlaying 
                        ? 'bg-rose-600 hover:bg-rose-500 text-white' 
                        : 'bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-400 border border-indigo-500/30'
                    }`}
                  >
                    {previewingVoiceName === singleVoice && isPreviewPlaying ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ရပ်မည်
                      </>
                    ) : (
                      <>
                        <Play className="w-3 h-3 fill-current" />
                        နမူနာ
                      </>
                    )}
                  </button>
                </div>
                <div className="md:col-span-8 bg-slate-950 rounded-xl p-3 border border-slate-850 flex items-center justify-between">
                  <p className="text-[11px] text-slate-400">
                    {VOICE_OPTIONS.find(v => v.name === singleVoice)?.description}
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {multiSpeakers.map((speaker, idx) => (
                    <div key={idx} className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex flex-col gap-2">
                      <div className="flex justify-between items-center">
                        <span className="text-xs font-bold text-slate-300">အသံပိုင်ရှင် {idx + 1}</span>
                        <button
                          onClick={() => handlePreviewVoice(speaker.voice)}
                          className={`px-2.5 py-1 text-[10px] font-bold rounded-lg flex items-center gap-1.5 transition-all ${
                            previewingVoiceName === speaker.voice && isPreviewPlaying 
                              ? 'bg-rose-600 text-white' 
                              : 'bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-400 border border-indigo-500/30'
                          }`}
                        >
                          {previewingVoiceName === speaker.voice && isPreviewPlaying ? (
                            <>
                              <Loader2 className="w-3.5 h-3 animate-spin" />
                              ရပ်ရန်
                            </>
                          ) : (
                            <>
                              <Play className="w-2.5 h-2.5 fill-current" />
                              အသံနမူနာ
                            </>
                          )}
                        </button>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <input 
                          type="text"
                          value={speaker.name}
                          onChange={(e) => updateSpeaker(idx, "name", e.target.value)}
                          className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-xs text-white"
                          placeholder="အမည်"
                        />
                        <select 
                          value={speaker.voice}
                          onChange={(e) => updateSpeaker(idx, "voice", e.target.value)}
                          className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-xs text-white"
                        >
                          {VOICE_OPTIONS.map(v => (
                            <option key={v.name} value={v.name}>{v.name}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Prompt / Script Area */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <FileText className="w-4.5 h-4.5 text-indigo-400" />
              <h2 className="text-sm font-semibold text-slate-100">ဖတ်စေလိုသော စာသားများ (အောက်ပါ Script အား အသံပြောင်းကြည့်ပါ)</h2>
            </div>

            <textarea
              rows={12}
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-white font-mono leading-relaxed focus:outline-none"
              placeholder="ပြောစေလိုသည့် စာသားများကို ဤနေရာတွင် ရေးသားပါ..."
            />

            {/* Audio tags */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2">အသံအမူအရာ ထည့်သွင်းရန် (Emotional Modifier Tags)</label>
              <div className="flex flex-wrap gap-1.5 p-2 bg-slate-950 border border-slate-850 rounded-xl">
                {POPULAR_TAGS.map((t) => (
                  <button
                    key={t.tag}
                    onClick={() => insertTag(t.tag)}
                    title={t.desc}
                    className="text-[10px] font-mono px-2.5 py-1 bg-slate-900 border border-slate-800 text-slate-300 hover:text-indigo-400 rounded-lg transition"
                  >
                    {t.tag} ({t.desc})
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={executeTtsGeneration}
              disabled={isGenerating || !promptText.trim()}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white font-semibold text-xs tracking-wide uppercase rounded-xl flex items-center justify-center gap-2 shadow-lg hover:brightness-110 active:scale-95 transition-all"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  အသံဖိုင် ဖန်တီးနေဆဲဖြစ်သည်...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  အသံပြောင်းမည်
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Playback Deck */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col items-center justify-center min-h-[220px] relative">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-6">အသံဖွင့်စက်</h3>

            {audioUrl ? (
              <div className="w-full flex flex-col items-center gap-5 z-10">
                <div className="flex items-end justify-center gap-1.5 h-16 w-full max-w-[200px]">
                  {[...Array(10)].map((_, i) => (
                    <div
                      key={i}
                      className={`w-1.5 bg-indigo-500 rounded-full transition-all duration-300 ${isPlaying ? 'animate-pulse' : 'h-2'}`}
                      style={{
                        height: isPlaying ? `${Math.floor(Math.random() * 40) + 10}px` : '6px',
                        animationDelay: `${i * 0.1}s`
                      }}
                    />
                  ))}
                </div>

                <div className="flex flex-col gap-3 w-full">
                  <div className="flex items-center gap-2 w-full">
                    <button
                      onClick={handleAudioPlayback}
                      className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 shadow-lg transition"
                    >
                      {isPlaying ? "ရပ်ရန်" : "နားထောင်ရန်"}
                    </button>
                    
                    {/* Direct Download Button */}
                    <button
                      onClick={handleDownload}
                      className="p-3 bg-emerald-600/20 hover:bg-emerald-600/40 border border-emerald-500/30 text-emerald-400 rounded-xl transition-all flex items-center justify-center"
                      title="တိုက်ရိုက် ဒေါင်းလုတ်ဆွဲရန်"
                    >
                      <Download className="w-5 h-5" />
                    </button>
                  </div>

                  {/* Open in New Tab Fallback Button */}
                  <button
                    onClick={handleOpenInNewTab}
                    className="w-full py-2 bg-slate-800 hover:bg-slate-750 text-slate-300 text-[11px] font-semibold rounded-lg border border-slate-700/50 flex items-center justify-center gap-1.5 transition-all"
                    title="ဒေါင်းလုတ်မရပါက တဘ်အသစ်တွင်ဖွင့်ပြီး သိမ်းဆည်းရန်"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    ဝင်းဒိုးအသစ်တွင်ဖွင့်ပြီး သိမ်းဆည်းရန်
                  </button>
                </div>

                <audio 
                  ref={audioRef} 
                  src={audioUrl} 
                  onPlay={() => setIsPlaying(true)}
                  onPause={() => setIsPlaying(false)}
                  onEnded={() => setIsPlaying(false)}
                  className="hidden" 
                />
              </div>
            ) : (
              <div className="text-center py-4">
                <div className="w-12 h-12 rounded-full bg-slate-950 flex items-center justify-center border border-slate-850 mx-auto mb-3">
                  <Volume2 className="w-5 h-5 text-indigo-500" />
                </div>
                <p className="text-xs text-slate-400 font-medium">အသံဖိုင်မရှိသေးပါ။</p>
                <p className="text-[10px] text-slate-500 mt-1">စာသားရိုက်ထည့်ပြီး အသံပြောင်းပါကို နှိပ်ပါ။</p>
              </div>
            )}
          </div>

          {/* Live Telemetry Logger Console */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col gap-3">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-indigo-400" />
              လုပ်ဆောင်မှု အခြေအနေ (Console)
            </h3>
            <div className="bg-slate-950 border border-slate-850 p-3 rounded-xl h-44 overflow-y-auto font-mono text-[10px] text-slate-400 space-y-1">
              {logs.length === 0 ? (
                <div className="text-slate-600 italic">လုပ်ဆောင်မှု မှတ်တမ်း မရှိသေးပါ။</div>
              ) : (
                logs.map((log, index) => (
                  <div key={index} className="leading-relaxed border-l-2 border-indigo-500/40 pl-2">
                    {log}
                  </div>
                ))
              )}
            </div>
          </div>

          {errorMsg && (
            <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl flex gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
              <div className="text-[11px] text-rose-300">
                <span className="font-bold">Error:</span> {errorMsg}
              </div>
            </div>
          )}
        </div>

      </main>
    </div>
  );
}

```