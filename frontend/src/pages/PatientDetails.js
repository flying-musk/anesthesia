import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { patientAPI } from '../services/api';

const PatientDetails = () => {
  const { t } = useTranslation();
  const { id } = useParams();

  const { data: patient, isLoading, error } = useQuery(
    ['patient', id],
    () => patientAPI.getPatient(id).then(res => res.data)
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        {t('errors.networkError')}
      </Alert>
    );
  }

  if (!patient) {
    return (
      <Alert severity="warning">
        {t('errors.notFound')}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('patient.patientDetails')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('patient.personalInfo')}
              </Typography>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <Typography variant="h5">{patient.full_name}</Typography>
                <Chip 
                  label={t(`patient.genders.${patient.gender}`)} 
                  color={patient.gender === 'M' ? 'primary' : patient.gender === 'F' ? 'secondary' : 'default'}
                />
              </Box>
              <Typography variant="body2" gutterBottom>
                <strong>{t('patient.fields.healthInsuranceNumber')}:</strong> {patient.health_insurance_number}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>{t('patient.fields.dateOfBirth')}:</strong> {new Date(patient.date_of_birth).toLocaleDateString()}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>{t('patient.fields.phoneNumber')}:</strong> {patient.phone_number}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>{t('patient.fields.emergencyContactName')}:</strong> {patient.emergency_contact_name}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>{t('patient.fields.emergencyContactRelationship')}:</strong> {patient.emergency_contact_relationship}
              </Typography>
              <Typography variant="body2">
                <strong>{t('patient.fields.emergencyContactPhone')}:</strong> {patient.emergency_contact_phone}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {patient.medical_history && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('patient.medicalHistory')}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  <strong>{t('patient.medicalHistoryFields.allergies')}:</strong> {patient.medical_history.allergies || '無'}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  <strong>{t('patient.medicalHistoryFields.chronicConditions')}:</strong> {patient.medical_history.chronic_conditions || '無'}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  <strong>{t('patient.medicalHistoryFields.currentMedications')}:</strong> {patient.medical_history.current_medications || '無'}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  <strong>{t('patient.medicalHistoryFields.previousSurgeries')}:</strong> {patient.medical_history.previous_surgeries || '無'}
                </Typography>
                <Typography variant="body2">
                  <strong>{t('patient.medicalHistoryFields.familyHistory')}:</strong> {patient.medical_history.family_history || '無'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default PatientDetails;
