import React from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery } from 'react-query';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { anesthesiaAPI } from '../services/api';

const AnesthesiaGuidelines = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const { data: guidelines = [], isLoading, error } = useQuery(
    'guidelines',
    () => anesthesiaAPI.getGuidelines().then(res => res.data)
  );

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

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

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          {t('anesthesia.title')}
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/guidelines/generate')}
        >
          {t('anesthesia.generateGuideline')}
        </Button>
      </Box>

      <Grid container spacing={3}>
        {guidelines.map((guideline) => (
          <Grid item xs={12} md={6} lg={4} key={guideline.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {guideline.surgery_name}
                </Typography>
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <Chip 
                    label={t(`anesthesia.types.${guideline.anesthesia_type}`)} 
                    size="small"
                    color="primary"
                  />
                  <Chip 
                    label={formatDate(guideline.surgery_date)} 
                    size="small"
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
              <Box display="flex" justifyContent="flex-end" p={2}>
                <IconButton
                  size="small"
                  onClick={() => navigate(`/guidelines/${guideline.id}`)}
                  title={t('app.view')}
                >
                  <VisibilityIcon />
                </IconButton>
                <IconButton
                  size="small"
                  title={t('app.edit')}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  size="small"
                  title={t('app.delete')}
                  color="error"
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>

      {guidelines.length === 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" align="center" color="textSecondary">
              {t('messages.noResults')}
            </Typography>
            <Box display="flex" justifyContent="center" mt={2}>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => navigate('/guidelines/generate')}
              >
                {t('anesthesia.generateGuideline')}
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AnesthesiaGuidelines;
