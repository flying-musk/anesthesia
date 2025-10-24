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
import { anesthesiaAPI } from '../services/api';

const GuidelineDetails = () => {
  const { t } = useTranslation();
  const { id } = useParams();

  const { data: guideline, isLoading, error } = useQuery(
    ['guideline', id],
    () => anesthesiaAPI.getGuideline(id).then(res => res.data)
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

  if (!guideline) {
    return (
      <Alert severity="warning">
        {t('errors.notFound')}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('anesthesia.guidelineDetails')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                {guideline.surgery_name}
              </Typography>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <Chip 
                  label={t(`anesthesia.types.${guideline.anesthesia_type}`)} 
                  color="primary"
                />
                <Chip 
                  label={new Date(guideline.surgery_date).toLocaleDateString()} 
                  variant="outlined"
                />
              </Box>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                {t('anesthesia.fields.surgeonName')}: {guideline.surgeon_name}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {t('anesthesia.fields.anesthesiologistName')}: {guideline.anesthesiologist_name}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.anesthesiaTypeInfo')}
              </Typography>
              <Typography variant="body1" paragraph>
                {guideline.anesthesia_type_info}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.surgeryProcess')}
              </Typography>
              <Typography variant="body1">
                {guideline.surgery_process}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.expectedSensations')}
              </Typography>
              <Typography variant="body1">
                {guideline.expected_sensations}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.potentialRisks')}
              </Typography>
              <Typography variant="body1">
                {guideline.potential_risks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.preSurgeryInstructions')}
              </Typography>
              <Typography variant="body1">
                {guideline.pre_surgery_instructions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.fastingInstructions')}
              </Typography>
              <Typography variant="body1">
                {guideline.fasting_instructions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.medicationInstructions')}
              </Typography>
              <Typography variant="body1">
                {guideline.medication_instructions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.commonQuestions')}
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {guideline.common_questions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.content.postSurgeryCare')}
              </Typography>
              <Typography variant="body1">
                {guideline.post_surgery_care}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default GuidelineDetails;
