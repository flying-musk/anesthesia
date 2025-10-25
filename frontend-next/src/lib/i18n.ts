import { Language } from '@/contexts/language-context';

export const translations = {
  en: {
    // Navigation
    dashboard: 'Dashboard',
    patients: 'Patients',
    createPatient: 'Create Patient',
    guidelines: 'Guidelines',
    generateGuideline: 'Generate Guideline',
    languageTest: 'Language Test',
    copyright: '© 2025 Anesthesia System',
    
    // Header
    anesthesiaManagement: 'Anesthesia Management',
    
    // Guidelines
    anesthesiaGuideline: 'Anesthesia Guideline',
    surgeryInformation: 'Surgery Information',
    surgeryDate: 'Surgery Date',
    anesthesiaType: 'Anesthesia Type',
    surgeon: 'Surgeon',
    anesthesiologist: 'Anesthesiologist',
    guidelineDetails: 'Guideline Details',
    anesthesiaTypeInfo: 'Anesthesia Type Information',
    surgeryProcess: 'Surgery Process',
    expectedSensations: 'Expected Sensations',
    potentialRisks: 'Potential Risks',
    preSurgeryInstructions: 'Pre-Surgery Instructions',
    fastingInstructions: 'Fasting Instructions',
    medicationInstructions: 'Medication Instructions',
    commonQuestions: 'Common Questions',
    postSurgeryCare: 'Post-Surgery Care',
    created: 'Created',
    aiGenerated: 'AI Generated',
    
    // Buttons
    backToGuidelines: 'Back to Guidelines',
    view: 'View',
    generate: 'Generate',
    
    // Status
    guidelineNotFound: 'Guideline not found',
    noGuidelineContent: 'No guideline content available',
  },
  zh: {
    // Navigation
    dashboard: '儀表板',
    patients: '患者',
    createPatient: '創建患者',
    guidelines: '指南',
    generateGuideline: '生成指南',
    languageTest: '語言測試',
    copyright: '© 2025 麻醉系統',
    
    // Header
    anesthesiaManagement: '麻醉管理',
    
    // Guidelines
    anesthesiaGuideline: '麻醉指南',
    surgeryInformation: '手術信息',
    surgeryDate: '手術日期',
    anesthesiaType: '麻醉類型',
    surgeon: '外科醫生',
    anesthesiologist: '麻醉師',
    guidelineDetails: '指南詳情',
    anesthesiaTypeInfo: '麻醉類型信息',
    surgeryProcess: '手術過程',
    expectedSensations: '預期感覺',
    potentialRisks: '潛在風險',
    preSurgeryInstructions: '術前指示',
    fastingInstructions: '禁食指示',
    medicationInstructions: '用藥指示',
    commonQuestions: '常見問題',
    postSurgeryCare: '術後護理',
    created: '創建時間',
    aiGenerated: 'AI 生成',
    
    // Buttons
    backToGuidelines: '返回指南',
    view: '查看',
    generate: '生成',
    
    // Status
    guidelineNotFound: '未找到指南',
    noGuidelineContent: '無可用指南內容',
  },
  fr: {
    // Navigation
    dashboard: 'Tableau de Bord',
    patients: 'Patients',
    createPatient: 'Créer un Patient',
    guidelines: 'Directives',
    generateGuideline: 'Générer une Directive',
    languageTest: 'Test de Langue',
    copyright: '© 2025 Système d\'Anesthésie',
    
    // Header
    anesthesiaManagement: 'Gestion d\'Anesthésie',
    
    // Guidelines
    anesthesiaGuideline: 'Directive d\'Anesthésie',
    surgeryInformation: 'Informations sur la Chirurgie',
    surgeryDate: 'Date de Chirurgie',
    anesthesiaType: 'Type d\'Anesthésie',
    surgeon: 'Chirurgien',
    anesthesiologist: 'Anesthésiste',
    guidelineDetails: 'Détails de la Directive',
    anesthesiaTypeInfo: 'Informations sur le Type d\'Anesthésie',
    surgeryProcess: 'Processus de Chirurgie',
    expectedSensations: 'Sensations Attendues',
    potentialRisks: 'Risques Potentiels',
    preSurgeryInstructions: 'Instructions Pré-Chirurgie',
    fastingInstructions: 'Instructions de Jeûne',
    medicationInstructions: 'Instructions de Médicaments',
    commonQuestions: 'Questions Courantes',
    postSurgeryCare: 'Soins Post-Chirurgie',
    created: 'Créé',
    aiGenerated: 'Généré par IA',
    
    // Buttons
    backToGuidelines: 'Retour aux Directives',
    view: 'Voir',
    generate: 'Générer',
    
    // Status
    guidelineNotFound: 'Directive non trouvée',
    noGuidelineContent: 'Aucun contenu de directive disponible',
  },
};

export function getTranslations(language: Language) {
  return translations[language];
}

export type TranslationKeys = keyof typeof translations.en;
