import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useMutation } from 'react-query';
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
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { patientAPI } from '../services/api';

const schema = yup.object({
  health_insurance_number: yup.string().required(),
  full_name: yup.string().required(),
  date_of_birth: yup.date().required(),
  gender: yup.string().required(),
  phone_number: yup.string().required(),
  emergency_contact_name: yup.string().required(),
  emergency_contact_relationship: yup.string().required(),
  emergency_contact_phone: yup.string().required(),
});

const CreatePatient = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const createPatientMutation = useMutation(
    (data) => patientAPI.createPatient(data).then(res => res.data),
    {
      onSuccess: (data) => {
        navigate(`/patients/${data.id}`);
      },
      onError: (error) => {
        console.error('Creation failed:', error);
      },
    }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      health_insurance_number: '',
      full_name: '',
      date_of_birth: '',
      gender: '',
      phone_number: '',
      emergency_contact_name: '',
      emergency_contact_relationship: '',
      emergency_contact_phone: '',
    },
  });

  const onSubmit = (data) => {
    createPatientMutation.mutate(data);
  };

  const genders = [
    { value: 'M', label: t('patient.genders.M') },
    { value: 'F', label: t('patient.genders.F') },
    { value: 'O', label: t('patient.genders.O') },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('patient.createPatient')}
      </Typography>

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Controller
                  name="health_insurance_number"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.healthInsuranceNumber')}
                      error={!!errors.health_insurance_number}
                      helperText={errors.health_insurance_number?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="full_name"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.fullName')}
                      error={!!errors.full_name}
                      helperText={errors.full_name?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="date_of_birth"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      type="date"
                      label={t('patient.fields.dateOfBirth')}
                      error={!!errors.date_of_birth}
                      helperText={errors.date_of_birth?.message}
                      InputLabelProps={{ shrink: true }}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="gender"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      fullWidth
                      label={t('patient.fields.gender')}
                      error={!!errors.gender}
                      helperText={errors.gender?.message}
                    >
                      {genders.map((gender) => (
                        <MenuItem key={gender.value} value={gender.value}>
                          {gender.label}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="phone_number"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.phoneNumber')}
                      error={!!errors.phone_number}
                      helperText={errors.phone_number?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="emergency_contact_name"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.emergencyContactName')}
                      error={!!errors.emergency_contact_name}
                      helperText={errors.emergency_contact_name?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="emergency_contact_relationship"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.emergencyContactRelationship')}
                      error={!!errors.emergency_contact_relationship}
                      helperText={errors.emergency_contact_relationship?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="emergency_contact_phone"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label={t('patient.fields.emergencyContactPhone')}
                      error={!!errors.emergency_contact_phone}
                      helperText={errors.emergency_contact_phone?.message}
                    />
                  )}
                />
              </Grid>
            </Grid>

            <Box display="flex" justifyContent="flex-end" gap={2} mt={3}>
              <Button
                variant="outlined"
                onClick={() => navigate('/patients')}
              >
                {t('app.cancel')}
              </Button>
              <Button
                type="submit"
                variant="contained"
                disabled={createPatientMutation.isLoading}
              >
                {createPatientMutation.isLoading ? (
                  <CircularProgress size={20} />
                ) : (
                  t('app.save')
                )}
              </Button>
            </Box>
          </form>

          {createPatientMutation.error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {t('errors.serverError')}: {createPatientMutation.error.message}
            </Alert>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default CreatePatient;
