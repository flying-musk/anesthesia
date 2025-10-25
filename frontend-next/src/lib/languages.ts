// 语言配置
export const languages = {
  en: {
    name: 'English',
    flag: '🇺🇸',
    code: 'en'
  },
  zh: {
    name: '中文',
    flag: '🇨🇳', 
    code: 'zh'
  }
};

// 翻译文本
export const translations = {
  en: {
    nav: {
      dashboard: 'Dashboard',
      patients: 'Patients',
      guidelines: 'Guidelines',
      createPatient: 'Create Patient',
      generateGuideline: 'Generate Guideline'
    },
    dashboard: {
      title: 'Dashboard',
      welcome: 'Welcome to the Anesthesia Management System',
      stats: {
        totalPatients: 'Total Patients',
        totalGuidelines: 'Total Guidelines'
      },
      actions: {
        createPatient: 'Create Patient',
        createPatientDesc: 'Add a new patient to the system',
        generateGuideline: 'Generate Guideline',
        generateGuidelineDesc: 'Create AI-powered anesthesia guidelines'
      },
      recent: {
        patients: 'Recent Patients',
        guidelines: 'Recent Guidelines',
        noPatients: 'No patients yet',
        noGuidelines: 'No guidelines yet'
      },
      viewAll: 'View all'
    },
    patients: {
      title: 'Patients',
      description: 'Manage patient information and records',
      createPatient: 'Create Patient',
      search: 'Search by name or insurance number...',
      table: {
        insuranceNumber: 'Insurance Number',
        fullName: 'Full Name',
        dateOfBirth: 'Date of Birth',
        gender: 'Gender',
        phone: 'Phone',
        actions: 'Actions',
        view: 'View'
      },
      noPatients: 'No patients found'
    },
    guidelines: {
      title: 'Guidelines',
      description: 'Manage anesthesia guidelines',
      generateGuideline: 'Generate Guideline',
      search: 'Search guidelines...',
      table: {
        surgeryName: 'Surgery Name',
        surgeryDate: 'Surgery Date',
        anesthesiaType: 'Anesthesia Type',
        actions: 'Actions',
        view: 'View'
      },
      noGuidelines: 'No guidelines found'
    },
    createPatient: {
      title: 'Create Patient',
      description: 'Add a new patient to the system',
      form: {
        insuranceNumber: 'Insurance Number',
        fullName: 'Full Name',
        dateOfBirth: 'Date of Birth',
        gender: 'Gender',
        phoneNumber: 'Phone Number',
        address: 'Address',
        medicalHistory: 'Medical History',
        allergies: 'Allergies',
        currentMedications: 'Current Medications'
      },
      genderOptions: {
        male: 'Male',
        female: 'Female',
        other: 'Other'
      },
      buttons: {
        create: 'Create Patient',
        cancel: 'Cancel',
        back: 'Back'
      },
      success: 'Patient created successfully!',
      error: 'Failed to create patient. Please try again.'
    },
    generateGuideline: {
      title: 'Generate Anesthesia Guideline',
      description: 'Create AI-powered anesthesia guidelines for surgery',
      steps: {
        selectPatient: 'Select Patient',
        surgeryDetails: 'Surgery Details',
        review: 'Review'
      },
      form: {
        selectPatient: 'Select a patient',
        surgeryName: 'Surgery Name',
        surgeryDate: 'Surgery Date',
        anesthesiaType: 'Anesthesia Type',
        surgeryDuration: 'Expected Duration (hours)',
        specialRequirements: 'Special Requirements',
        patientCondition: 'Patient Condition'
      },
      anesthesiaTypes: {
        general: 'General Anesthesia',
        regional: 'Regional Anesthesia',
        local: 'Local Anesthesia',
        sedation: 'Conscious Sedation'
      },
      buttons: {
        generate: 'Generate Guideline',
        back: 'Back',
        next: 'Next',
        previous: 'Previous',
        cancel: 'Cancel'
      },
      generating: 'Generating guideline...',
      success: 'Guideline generated successfully!',
      error: 'Failed to generate guideline. Please try again.'
    },
    common: {
      language: 'Language',
      switchLanguage: 'Switch Language',
      loading: 'Loading...',
      actions: 'Actions',
      view: 'View',
      edit: 'Edit',
      delete: 'Delete',
      save: 'Save',
      cancel: 'Cancel',
      submit: 'Submit',
      back: 'Back',
      next: 'Next',
      previous: 'Previous'
    }
  },
  zh: {
    nav: {
      dashboard: '仪表板',
      patients: '患者',
      guidelines: '指南',
      createPatient: '创建患者',
      generateGuideline: '生成指南'
    },
    dashboard: {
      title: '仪表板',
      welcome: '欢迎使用麻醉管理系统',
      stats: {
        totalPatients: '总患者数',
        totalGuidelines: '总指南数'
      },
      actions: {
        createPatient: '创建患者',
        createPatientDesc: '向系统添加新患者',
        generateGuideline: '生成指南',
        generateGuidelineDesc: '创建AI驱动的麻醉指南'
      },
      recent: {
        patients: '最近患者',
        guidelines: '最近指南',
        noPatients: '暂无患者',
        noGuidelines: '暂无指南'
      },
      viewAll: '查看全部'
    },
    patients: {
      title: '患者',
      description: '管理患者信息和记录',
      createPatient: '创建患者',
      search: '按姓名或保险号搜索...',
      table: {
        insuranceNumber: '保险号',
        fullName: '姓名',
        dateOfBirth: '出生日期',
        gender: '性别',
        phone: '电话',
        actions: '操作',
        view: '查看'
      },
      noPatients: '未找到患者'
    },
    guidelines: {
      title: '指南',
      description: '管理麻醉指南',
      generateGuideline: '生成指南',
      search: '搜索指南...',
      table: {
        surgeryName: '手术名称',
        surgeryDate: '手术日期',
        anesthesiaType: '麻醉类型',
        actions: '操作',
        view: '查看'
      },
      noGuidelines: '未找到指南'
    },
    createPatient: {
      title: '创建患者',
      description: '向系统添加新患者',
      form: {
        insuranceNumber: '保险号',
        fullName: '姓名',
        dateOfBirth: '出生日期',
        gender: '性别',
        phoneNumber: '电话号码',
        address: '地址',
        medicalHistory: '病史',
        allergies: '过敏史',
        currentMedications: '当前用药'
      },
      genderOptions: {
        male: '男',
        female: '女',
        other: '其他'
      },
      buttons: {
        create: '创建患者',
        cancel: '取消',
        back: '返回'
      },
      success: '患者创建成功！',
      error: '创建患者失败，请重试。'
    },
    generateGuideline: {
      title: '生成麻醉指南',
      description: '为手术创建AI驱动的麻醉指南',
      steps: {
        selectPatient: '选择患者',
        surgeryDetails: '手术详情',
        review: '审查'
      },
      form: {
        selectPatient: '选择患者',
        surgeryName: '手术名称',
        surgeryDate: '手术日期',
        anesthesiaType: '麻醉类型',
        surgeryDuration: '预计时长（小时）',
        specialRequirements: '特殊要求',
        patientCondition: '患者状况'
      },
      anesthesiaTypes: {
        general: '全身麻醉',
        regional: '区域麻醉',
        local: '局部麻醉',
        sedation: '清醒镇静'
      },
      buttons: {
        generate: '生成指南',
        back: '返回',
        next: '下一步',
        previous: '上一步',
        cancel: '取消'
      },
      generating: '正在生成指南...',
      success: '指南生成成功！',
      error: '生成指南失败，请重试。'
    },
    common: {
      language: '语言',
      switchLanguage: '切换语言',
      loading: '加载中...',
      actions: '操作',
      view: '查看',
      edit: '编辑',
      delete: '删除',
      save: '保存',
      cancel: '取消',
      submit: '提交',
      back: '返回',
      next: '下一步',
      previous: '上一步'
    }
  }
};

// 获取翻译文本的函数
export function getTranslation(locale: keyof typeof translations, key: string): string {
  const keys = key.split('.');
  let value: any = translations[locale];
  
  for (const k of keys) {
    value = value?.[k];
  }
  
  return value || key;
}
