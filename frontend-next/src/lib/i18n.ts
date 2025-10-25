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
    
    // Status
    guidelineNotFound: 'Guideline not found',
    noGuidelineContent: 'No guideline content available',
    
    // Dashboard
    welcomeMessage: 'Welcome to the Anesthesia Management System',
    totalPatients: 'Total Patients',
    totalGuidelines: 'Total Guidelines',
    viewAll: 'View all',
    recentPatients: 'Recent Patients',
    recentGuidelines: 'Recent Guidelines',
    
    // Patients
    managePatients: 'Manage patient information and records',
    searchPlaceholder: 'Search by name or insurance number...',
    insuranceNumber: 'Insurance Number',
    fullName: 'Full Name',
    dateOfBirth: 'Date of Birth',
    gender: 'Gender',
    phone: 'Phone',
    actions: 'Actions',
    view: 'View',
    edit: 'Edit',
    delete: 'Delete',
    male: 'Male',
    female: 'Female',
    
    // Create Patient
    addNewPatient: 'Add a new patient to the system',
    patientInformation: 'Patient Information',
    healthInsuranceNumber: 'Health Insurance Number',
    dateOfBirthPlaceholder: 'dd/mm/yyyy',
    selectGender: 'Select gender',
    emergencyContact: 'Emergency Contact (Optional)',
    emergencyContactName: 'Emergency Contact Name',
    emergencyContactRelationship: 'Relationship',
    emergencyContactPhone: 'Emergency Contact Phone',
    cancel: 'Cancel',
    create: 'Create',
    
    // Generate Guideline
    generateGuidelineDescription: 'AI-powered guideline generation for anesthesia procedures',
    selectPatient: 'Select Patient',
    surgeryDetails: 'Surgery Details',
    review: 'Review',
    choosePatient: 'Choose a patient',
    surgeryName: 'Surgery Name',
    surgeonName: 'Surgeon Name',
    anesthesiologistName: 'Anesthesiologist Name',
    selectType: 'Select type',
    previous: 'Previous',
    next: 'Next',
    generate: 'Generate',
    
    // Patient Information Display
    patientInfo: 'Patient Information',
    name: 'Name',
    insurance: 'Insurance',
    
    // Surgery Information Display
    surgeryInfo: 'Surgery Information',
    surgery: 'Surgery',
    type: 'Type',
    date: 'Date',
    
    // Anesthesia Types
    general: 'General',
    local: 'Local',
    regional: 'Regional',
    sedation: 'Sedation',
    
    // AI Generation
    aiPoweredGeneration: 'AI-Powered Generation',
    aiGenerationDescription: 'Our AI will generate comprehensive anesthesia guidelines based on the patient information and surgery details provided.',
    
    // Patient Details Page
    patientNotFound: 'Patient not found',
    backToPatients: 'Back to Patients',
    details: 'Details',
    medicalHistory: 'Medical History',
    surgeries: 'Surgeries',
    phoneNumber: 'Phone Number',
    relationship: 'Relationship',
    notAvailable: 'N/A',
    allergies: 'Allergies',
    chronicConditions: 'Chronic Conditions',
    currentMedications: 'Current Medications',
    previousSurgeries: 'Previous Surgeries',
    familyHistory: 'Family History',
    noMedicalHistory: 'No medical history available',
    surgeryRecords: 'Surgery Records',
    noSurgeryRecords: 'No surgery records available',
    noGuidelinesAvailable: 'No guidelines available for this patient',
    other: 'Other',
    addSurgeryRecord: 'Add Surgery Record',
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
    
    // Status
    guidelineNotFound: '未找到指南',
    noGuidelineContent: '無可用指南內容',
    
    // Dashboard
    welcomeMessage: '歡迎使用麻醉管理系統',
    totalPatients: '總患者數',
    totalGuidelines: '總指南數',
    viewAll: '查看全部',
    recentPatients: '最近患者',
    recentGuidelines: '最近指南',
    
    // Patients
    managePatients: '管理患者信息和記錄',
    searchPlaceholder: '按姓名或保險號搜索...',
    insuranceNumber: '保險號',
    fullName: '姓名',
    dateOfBirth: '出生日期',
    gender: '性別',
    phone: '電話',
    actions: '操作',
    view: '查看',
    edit: '編輯',
    delete: '刪除',
    male: '男性',
    female: '女性',
    
    // Create Patient
    addNewPatient: '向系統添加新患者',
    patientInformation: '患者信息',
    healthInsuranceNumber: '健康保險號',
    dateOfBirthPlaceholder: '日/月/年',
    selectGender: '選擇性別',
    emergencyContact: '緊急聯繫人（可選）',
    emergencyContactName: '緊急聯繫人姓名',
    emergencyContactRelationship: '關係',
    emergencyContactPhone: '緊急聯繫人電話',
    cancel: '取消',
    create: '創建',
    
    // Generate Guideline
    generateGuidelineDescription: 'AI 驅動的麻醉程序指南生成',
    selectPatient: '選擇患者',
    surgeryDetails: '手術詳情',
    review: '審查',
    choosePatient: '選擇患者',
    surgeryName: '手術名稱',
    surgeonName: '外科醫生姓名',
    anesthesiologistName: '麻醉師姓名',
    selectType: '選擇類型',
    previous: '上一步',
    next: '下一步',
    generate: '生成',
    
    // Patient Information Display
    patientInfo: '患者信息',
    name: '姓名',
    insurance: '保險',
    
    // Surgery Information Display
    surgeryInfo: '手術信息',
    surgery: '手術',
    type: '類型',
    date: '日期',
    
    // Anesthesia Types
    general: '全身麻醉',
    local: '局部麻醉',
    regional: '區域麻醉',
    sedation: '鎮靜麻醉',
    
    // AI Generation
    aiPoweredGeneration: 'AI 驅動生成',
    aiGenerationDescription: '我們的 AI 將根據提供的患者信息和手術詳情生成全面的麻醉指南。',
    
    // Patient Details Page
    patientNotFound: '未找到患者',
    backToPatients: '返回患者列表',
    details: '詳情',
    medicalHistory: '醫療病史',
    surgeries: '手術',
    phoneNumber: '電話號碼',
    relationship: '關係',
    notAvailable: '無',
    allergies: '過敏',
    chronicConditions: '慢性疾病',
    currentMedications: '目前用藥',
    previousSurgeries: '既往手術',
    familyHistory: '家族病史',
    noMedicalHistory: '無醫療病史',
    surgeryRecords: '手術記錄',
    noSurgeryRecords: '無手術記錄',
    noGuidelinesAvailable: '該患者無可用指南',
    other: '其他',
    addSurgeryRecord: '添加手術記錄',
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
    
    // Status
    guidelineNotFound: 'Directive non trouvée',
    noGuidelineContent: 'Aucun contenu de directive disponible',
    
    // Dashboard
    welcomeMessage: 'Bienvenue dans le Système de Gestion d\'Anesthésie',
    totalPatients: 'Total des Patients',
    totalGuidelines: 'Total des Directives',
    viewAll: 'Voir tout',
    recentPatients: 'Patients Récents',
    recentGuidelines: 'Directives Récentes',
    
    // Patients
    managePatients: 'Gérer les informations et dossiers des patients',
    searchPlaceholder: 'Rechercher par nom ou numéro d\'assurance...',
    insuranceNumber: 'Numéro d\'Assurance',
    fullName: 'Nom Complet',
    dateOfBirth: 'Date de Naissance',
    gender: 'Sexe',
    phone: 'Téléphone',
    actions: 'Actions',
    view: 'Voir',
    edit: 'Modifier',
    delete: 'Supprimer',
    male: 'Homme',
    female: 'Femme',
    
    // Create Patient
    addNewPatient: 'Ajouter un nouveau patient au système',
    patientInformation: 'Informations du Patient',
    healthInsuranceNumber: 'Numéro d\'Assurance Maladie',
    dateOfBirthPlaceholder: 'jj/mm/aaaa',
    selectGender: 'Sélectionner le sexe',
    emergencyContact: 'Contact d\'Urgence (Optionnel)',
    emergencyContactName: 'Nom du Contact d\'Urgence',
    emergencyContactRelationship: 'Relation',
    emergencyContactPhone: 'Téléphone du Contact d\'Urgence',
    cancel: 'Annuler',
    create: 'Créer',
    
    // Generate Guideline
    generateGuidelineDescription: 'Génération de directives d\'anesthésie alimentée par IA',
    selectPatient: 'Sélectionner un Patient',
    surgeryDetails: 'Détails de la Chirurgie',
    review: 'Révision',
    choosePatient: 'Choisir un patient',
    surgeryName: 'Nom de la Chirurgie',
    surgeonName: 'Nom du Chirurgien',
    anesthesiologistName: 'Nom de l\'Anesthésiste',
    selectType: 'Sélectionner le type',
    previous: 'Précédent',
    next: 'Suivant',
    generate: 'Générer',
    
    // Patient Information Display
    patientInfo: 'Informations du Patient',
    name: 'Nom',
    insurance: 'Assurance',
    
    // Surgery Information Display
    surgeryInfo: 'Informations sur la Chirurgie',
    surgery: 'Chirurgie',
    type: 'Type',
    date: 'Date',
    
    // Anesthesia Types
    general: 'Général',
    local: 'Local',
    regional: 'Régional',
    sedation: 'Sédation',
    
    // AI Generation
    aiPoweredGeneration: 'Génération Alimentée par IA',
    aiGenerationDescription: 'Notre IA générera des directives d\'anesthésie complètes basées sur les informations du patient et les détails de la chirurgie fournis.',
    
    // Patient Details Page
    patientNotFound: 'Patient non trouvé',
    backToPatients: 'Retour aux Patients',
    details: 'Détails',
    medicalHistory: 'Antécédents Médicaux',
    surgeries: 'Chirurgies',
    phoneNumber: 'Numéro de Téléphone',
    relationship: 'Relation',
    notAvailable: 'N/A',
    allergies: 'Allergies',
    chronicConditions: 'Affections Chroniques',
    currentMedications: 'Médicaments Actuels',
    previousSurgeries: 'Chirurgies Précédentes',
    familyHistory: 'Antécédents Familiaux',
    noMedicalHistory: 'Aucun antécédent médical disponible',
    surgeryRecords: 'Dossiers de Chirurgie',
    noSurgeryRecords: 'Aucun dossier de chirurgie disponible',
    noGuidelinesAvailable: 'Aucune directive disponible pour ce patient',
    other: 'Autre',
    addSurgeryRecord: 'Ajouter un Dossier de Chirurgie',
  },
};

export function getTranslations(language: Language) {
  return translations[language];
}

export type TranslationKeys = keyof typeof translations.en;
