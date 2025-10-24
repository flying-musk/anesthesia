import React from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery } from 'react-query';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  People as PeopleIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { patientAPI, anesthesiaAPI } from '../services/api';

const Dashboard = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const { data: patients = [], isLoading: patientsLoading } = useQuery(
    'patients',
    () => patientAPI.getPatients().then(res => res.data)
  );

  const { data: guidelines = [], isLoading: guidelinesLoading } = useQuery(
    'guidelines',
    () => anesthesiaAPI.getGuidelines().then(res => res.data)
  );

  const stats = [
    {
      title: t('patient.title'),
      count: patients.length,
      icon: <PeopleIcon />,
      color: 'primary',
      action: () => navigate('/patients'),
    },
    {
      title: t('anesthesia.title'),
      count: guidelines.length,
      icon: <AssignmentIcon />,
      color: 'secondary',
      action: () => navigate('/guidelines'),
    },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('navigation.dashboard')}
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      {stat.title}
                    </Typography>
                    <Typography variant="h4">
                      {stat.count}
                    </Typography>
                  </Box>
                  <Box color={`${stat.color}.main`}>
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={stat.action}>
                  {t('app.create')}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('patient.patientList')}
              </Typography>
              {patientsLoading ? (
                <LinearProgress />
              ) : (
                <Box>
                  {patients.slice(0, 5).map((patient) => (
                    <Box key={patient.id} display="flex" justifyContent="space-between" alignItems="center" py={1}>
                      <Typography variant="body2">
                        {patient.full_name}
                      </Typography>
                      <Chip 
                        label={t(`patient.genders.${patient.gender}`)} 
                        size="small"
                        color={patient.gender === 'M' ? 'primary' : patient.gender === 'F' ? 'secondary' : 'default'}
                      />
                    </Box>
                  ))}
                  {patients.length > 5 && (
                    <Typography variant="caption" color="textSecondary">
                      +{patients.length - 5} {t('app.more')}
                    </Typography>
                  )}
                </Box>
              )}
            </CardContent>
            <CardActions>
              <Button size="small" onClick={() => navigate('/patients')}>
                {t('app.viewAll')}
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('anesthesia.guidelineList')}
              </Typography>
              {guidelinesLoading ? (
                <LinearProgress />
              ) : (
                <Box>
                  {guidelines.slice(0, 5).map((guideline) => (
                    <Box key={guideline.id} display="flex" justifyContent="space-between" alignItems="center" py={1}>
                      <Typography variant="body2">
                        {guideline.surgery_name}
                      </Typography>
                      <Chip 
                        label={t(`anesthesia.types.${guideline.anesthesia_type}`)} 
                        size="small"
                        color="primary"
                      />
                    </Box>
                  ))}
                  {guidelines.length > 5 && (
                    <Typography variant="caption" color="textSecondary">
                      +{guidelines.length - 5} {t('app.more')}
                    </Typography>
                  )}
                </Box>
              )}
            </CardContent>
            <CardActions>
              <Button size="small" onClick={() => navigate('/guidelines')}>
                {t('app.viewAll')}
              </Button>
            </CardActions>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
