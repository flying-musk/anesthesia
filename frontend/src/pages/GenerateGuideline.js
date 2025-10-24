import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useMutation, useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  MenuItem,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { anesthesiaAPI, patientAPI } from '../services/api';

const schema = yup.object({
  patient_id: yup.number().required(),
  surgery_name: yup.string().required(),
  anesthesia_type: yup.string().required(),
  surgery_date: yup.date().required(),
  surgeon_name: yup.string().required(),
  anesthesiologist_name: yup.string().required(),
});

const GenerateGuideline = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);

  // Fetch patients for dropdown
  const { data: patients = [] } = useQuery(
    'patients',
    () => patientAPI.getPatients().then(res => res.data)
  );

  // Generate guideline mutation
  const generateGuidelineMutation = useMutation(
    (data) => anesthesiaAPI.generateGuideline(data).then(res => res.data),
    {
      onSuccess: (data) => {
        navigate(`/guidelines/${data.id}`);
      },
      onError: (error) => {
        console.error('Generation failed:', error);
      },
    }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      patient_id: '',
      surgery_name: '',
      anesthesia_type: '',
      surgery_date: '',
      surgeon_name: '',
      anesthesiologist_name: '',
    },
  });

  const onSubmit = (data) => {
    // 確保日期格式正確
    const formattedData = {
      ...data,
      surgery_date: new Date(data.surgery_date).toISOString().split('T')[0] // 轉換為 YYYY-MM-DD 格式
    };
    generateGuidelineMutation.mutate(formattedData);
  };

  const steps = [
    t('patient.personalInfo'),
    t('anesthesia.title'),
    t('app.confirm'),
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const anesthesiaTypes = [
    { value: 'general', label: t('anesthesia.types.general') },
    { value: 'local', label: t('anesthesia.types.local') },
    { value: 'regional', label: t('anesthesia.types.regional') },
    { value: 'sedation', label: t('anesthesia.types.sedation') },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('anesthesia.generateGuideline')}
      </Typography>

      <Card>
        <CardContent>
          <Stepper activeStep={activeStep} orientation="vertical">
            {/* Step 1: Patient Selection */}
            <Step>
              <StepLabel>{steps[0]}</StepLabel>
              <StepContent>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <Controller
                      name="patient_id"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          select
                          fullWidth
                          label={t('anesthesia.fields.patientId')}
                          error={!!errors.patient_id}
                          helperText={errors.patient_id?.message}
                        >
                          {patients.map((patient) => (
                            <MenuItem key={patient.id} value={patient.id}>
                              {patient.full_name} ({patient.health_insurance_number})
                            </MenuItem>
                          ))}
                        </TextField>
                      )}
                    />
                  </Grid>
                </Grid>
                <Box sx={{ mb: 2, mt: 2 }}>
                  <Button
                    variant="contained"
                    onClick={handleNext}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    {t('app.next')}
                  </Button>
                </Box>
              </StepContent>
            </Step>

            {/* Step 2: Surgery Information */}
            <Step>
              <StepLabel>{steps[1]}</StepLabel>
              <StepContent>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Controller
                      name="surgery_name"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label={t('anesthesia.fields.surgeryName')}
                          error={!!errors.surgery_name}
                          helperText={errors.surgery_name?.message}
                        />
                      )}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Controller
                      name="anesthesia_type"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          select
                          fullWidth
                          label={t('anesthesia.fields.anesthesiaType')}
                          error={!!errors.anesthesia_type}
                          helperText={errors.anesthesia_type?.message}
                        >
                          {anesthesiaTypes.map((type) => (
                            <MenuItem key={type.value} value={type.value}>
                              {type.label}
                            </MenuItem>
                          ))}
                        </TextField>
                      )}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Controller
                      name="surgery_date"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          type="date"
                          label={t('anesthesia.fields.surgeryDate')}
                          error={!!errors.surgery_date}
                          helperText={errors.surgery_date?.message}
                          InputLabelProps={{ shrink: true }}
                        />
                      )}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Controller
                      name="surgeon_name"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label={t('anesthesia.fields.surgeonName')}
                          error={!!errors.surgeon_name}
                          helperText={errors.surgeon_name?.message}
                        />
                      )}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Controller
                      name="anesthesiologist_name"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label={t('anesthesia.fields.anesthesiologistName')}
                          error={!!errors.anesthesiologist_name}
                          helperText={errors.anesthesiologist_name?.message}
                        />
                      )}
                    />
                  </Grid>
                </Grid>
                <Box sx={{ mb: 2, mt: 2 }}>
                  <Button
                    variant="contained"
                    onClick={handleNext}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    {t('app.next')}
                  </Button>
                  <Button onClick={handleBack} sx={{ mt: 1, mr: 1 }}>
                    {t('app.previous')}
                  </Button>
                </Box>
              </StepContent>
            </Step>

            {/* Step 3: Confirmation */}
            <Step>
              <StepLabel>{steps[2]}</StepLabel>
              <StepContent>
                <Alert severity="info" sx={{ mb: 2 }}>
                  {t('messages.confirmDelete')} {/* You might want to add a specific confirmation message */}
                </Alert>
                <Box sx={{ mb: 2, mt: 2 }}>
                  <Button
                    variant="contained"
                    onClick={handleSubmit(onSubmit)}
                    disabled={generateGuidelineMutation.isLoading}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    {generateGuidelineMutation.isLoading ? (
                      <CircularProgress size={20} />
                    ) : (
                      t('anesthesia.generateGuideline')
                    )}
                  </Button>
                  <Button onClick={handleBack} sx={{ mt: 1, mr: 1 }}>
                    {t('app.previous')}
                  </Button>
                </Box>
              </StepContent>
            </Step>
          </Stepper>

          {generateGuidelineMutation.error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {t('errors.serverError')}: {generateGuidelineMutation.error.message}
            </Alert>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default GenerateGuideline;
